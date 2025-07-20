"""
Dynamic Input Validation System

This module provides validation functions that work with the input configuration
to validate user inputs dynamically based on field definitions.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
from utils.input_config import get_input_config, get_data_source_config
from utils.helpers import trace_function_call

def validate_field_value(field_name: str, value: Any, context: Dict[str, Any] = None) -> List[str]:
    """
    Validate a single field value based on its configuration.
    
    Args:
        field_name: Name of the field to validate
        value: Value to validate
        context: Additional context (e.g., other field values for cross-validation)
    
    Returns:
        List of error messages (empty if valid)
    """
    field_config = get_input_config(field_name)
    if not field_config:
        return [f"Unknown field: {field_name}"]
    
    errors = []
    validation_rules = field_config.get("validation", {})
    
    # Check if required field is empty
    if field_config.get("required", False) and not value:
        errors.append(f"{field_config['label']} is required")
        return errors
    
    # Skip validation if value is empty and field is optional
    if not value and not field_config.get("required", False):
        return errors
    
    # Validate based on field type
    field_type = field_config.get("type")
    
    if field_type == "text":
        errors.extend(_validate_text_field(field_name, value, validation_rules))
    elif field_type == "date_range":
        errors.extend(_validate_date_range_field(field_name, value, validation_rules, context))
    elif field_type == "select":
        errors.extend(_validate_select_field(field_name, value, field_config))
    
    return errors

def _validate_text_field(field_name: str, value: str, rules: Dict[str, Any]) -> List[str]:
    """Validate text field based on rules."""
    errors = []
    
    if rules.get("numeric", False):
        # Handle comma-separated values
        if rules.get("multiple_values", False):
            separator = rules.get("separator", ",")
            values = [v.strip() for v in str(value).split(separator) if v.strip()]
            
            if not values:
                return errors
            
            for val in values:
                if not val.isdigit():
                    errors.append(f"{field_name.replace('_', ' ').title()} must be numeric")
                    break
        else:
            # Single value validation
            if rules.get("single_value", False):
                values = [v.strip() for v in str(value).split(",") if v.strip()]
                if len(values) > 1:
                    errors.append(f"You can only enter one {field_name.replace('_', ' ')}")
                elif values and not values[0].isdigit():
                    errors.append(f"{field_name.replace('_', ' ').title()} must be numeric")
            elif not str(value).isdigit():
                errors.append(f"{field_name.replace('_', ' ').title()} must be numeric")
    
    if rules.get("min_length") and len(str(value)) < rules["min_length"]:
        errors.append(f"{field_name.replace('_', ' ').title()} is too short")
    
    return errors

def _validate_date_range_field(field_name: str, value: Tuple[date, date], rules: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
    """Validate date range field."""
    errors = []
    
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        errors.append("Invalid date range format")
        return errors
    
    start_date, end_date = value
    
    if not start_date or not end_date:
        errors.append("Both start and end dates are required")
        return errors
    
    # Validate start date is before end date
    if rules.get("start_before_end", False) and start_date > end_date:
        errors.append("Start date cannot be after end date")
    
    # Validate date range limits based on storefront count
    if context and "storefront_ids" in context:
        storefront_input = context["storefront_ids"]
        if storefront_input:
            storefront_list = [s.strip() for s in str(storefront_input).split(",") if s.strip()]
            num_storefronts = len(storefront_list)
            date_range_days = (end_date - start_date).days
            
            field_config = get_input_config(field_name)
            limits = field_config.get("validation", {}).get("date_range_limits", {})
            
            max_days_allowed = limits.get("single_storefront", 60)
            
            if num_storefronts > 1 and num_storefronts <= 2:
                max_days_allowed = limits.get("multiple_storefronts_2", 60)
            elif num_storefronts > 2:
                max_days_allowed = limits.get("multiple_storefronts_3plus", 30)
            
            if date_range_days > max_days_allowed:
                errors.append(
                    f"With {num_storefronts} storefront(s), the maximum allowed period is {max_days_allowed} days. "
                    f"Please select a shorter date range."
                )
    
    return errors

def _validate_select_field(field_name: str, value: str, field_config: Dict[str, Any]) -> List[str]:
    """Validate select field value."""
    errors = []
    
    options = field_config.get("options", [])
    if value and value not in options:
        errors.append(f"Invalid {field_config['label']}: {value}")
    
    return errors

@trace_function_call
def validate_data_source_inputs(data_source: str, input_values: Dict[str, Any]) -> List[str]:
    """
    Validate all inputs for a specific data source.
    
    Args:
        data_source: Data source key (e.g., 'kwl', 'sf')
        input_values: Dictionary of field names to values
    
    Returns:
        List of error messages (empty if all valid)
    """
    config = get_data_source_config(data_source)
    if not config:
        return [f"Unknown data source: {data_source}"]
    
    all_errors = []
    
    # Validate each required input field
    for field_name in config["inputs"]:
        field_value = input_values.get(field_name)
        
        # Special handling for date_range which comes as separate start/end values
        if field_name == "date_range":
            start_date = input_values.get("start_date")
            end_date = input_values.get("end_date")
            if start_date and end_date:
                field_value = (start_date, end_date)
        
        errors = validate_field_value(field_name, field_value, input_values)
        all_errors.extend(errors)
    
    return all_errors

@trace_function_call
def build_sql_params(data_source: str, input_values: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build SQL parameters from input values based on data source configuration.
    
    Args:
        data_source: Data source key
        input_values: Dictionary of field names to values
    
    Returns:
        Dictionary of SQL parameters ready for query execution
    """
    config = get_data_source_config(data_source)
    if not config:
        return {}
    
    sql_params = {}
    
    for field_name in config["inputs"]:
        field_config = get_input_config(field_name)
        if not field_config:
            continue
        
        field_value = input_values.get(field_name)
        
        # Skip empty optional fields (except for 'None' values in selects)
        if not field_value and field_config.get("required", False):
            continue
        
        # Handle different field types
        if field_name == "date_range":
            start_date = input_values.get("start_date")
            end_date = input_values.get("end_date")
            if start_date and end_date:
                sql_params["start_date"] = start_date.strftime('%Y-%m-%d')
                sql_params["end_date"] = end_date.strftime('%Y-%m-%d')
        
        elif field_name == "workspace_id":
            if field_value:
                sql_params["workspace_id"] = int(str(field_value).strip())
        
        else:
            # Handle select fields and other types
            sql_param_name = field_config.get("sql_param")
            if sql_param_name:
                if field_value == "None":
                    sql_params[sql_param_name] = None
                elif field_value:
                    sql_params[sql_param_name] = field_value

    # --- Separate handling for storefront_ids to ensure it's always processed ---
    if "storefront_ids" in input_values and input_values["storefront_ids"]:
        field_value = input_values["storefront_ids"]
        storefront_list = [int(s.strip()) for s in str(field_value).split(",") if s.strip()]
        sql_params["storefront_ids"] = storefront_list
    
    return sql_params

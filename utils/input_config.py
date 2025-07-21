"""
Input Configuration System for Dynamic Form Generation

This module defines all possible input fields and their properties,
enabling dynamic form generation and validation based on configuration.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# --- Constants ---
TODAY = datetime.now().date()
YESTERDAY = TODAY - timedelta(days=1)

# --- Input Field Definitions ---
INPUT_FIELDS = {
    "workspace_id": {
        "type": "text",
        "label": "Workspace ID",
        "required": True,
        "sql_param": "workspace_id",
        "validation": {
            "numeric": True,
            "single_value": True,
            "min_length": 1
        },
        "help_text": "Enter a single workspace ID (numeric only)"
    },
    
    "storefront_ids": {
        "type": "text",
        "label": "Storefront EID",
        "required": True,
        "sql_param": "storefront_ids",
        "validation": {
            "numeric": True,
            "multiple_values": True,
            "separator": ","
        },
        "help_text": "Enter one or more storefront EIDs separated by commas. Leave empty for all storefronts.",
        "performance_tip": "For faster performance with multiple storefronts, select a smaller date range."
    },
    
    "date_range": {
        "type": "date_range",
        "label": "Select time range",
        "required": True,
        "sql_params": ["start_date", "end_date"],
        "validation": {
            "start_before_end": True,
            "max_date": "yesterday"
        },
        "presets": {
            "Last 30 days": {"start": TODAY - timedelta(days=30), "end": YESTERDAY},
            "This month": {"start": TODAY.replace(day=1), "end": YESTERDAY},
            "Last month": {
                "start": (TODAY.replace(day=1) - timedelta(days=1)).replace(day=1),
                "end": TODAY.replace(day=1) - timedelta(days=1)
            },
            "Custom time range": None
        },
        "date_range_limits": {
            "single_storefront": 60,
            "multiple_storefronts_2": 60,
            "multiple_storefronts_3plus": 30
        }
    },
    
    "device_type": {
        "type": "select",
        "label": "Device Type",
        "required": False,
        "sql_param": "device_type",
        "options": ["Mobile", "Desktop", "None"],
        "default": "None",
        "help_text": "Filter by device type or select 'None' for all devices"
    },
    
    "display_type": {
        "type": "select",
        "label": "Display Type",
        "required": False,
        "sql_param": "display_type",
        "options": ["Paid", "Organic", "Top", "None"],
        "default": "None",
        "help_text": "Filter by display type or select 'None' for all types"
    },
    
    "product_position": {
        "type": "select",
        "label": "Product Position",
        "required": False,
        "sql_param": "product_position",
        "options": ["-1", "4", "10", "None"],
        "default": "None",
        "help_text": "Filter by product position or select 'None' for all positions"
    }
}

# --- Data Source Configurations ---
DATA_SOURCE_CONFIGS = {
    "storefront_in_workspace": {
        "name": "Storefront in Workspace",
        "data_logic_module": "storefront_data",
        "inputs": ["workspace_id"],
        "description": "Export a list of all storefronts within a specified workspace."
    },
    
    "keyword_lab": {
        "name": "Keyword Lab",
        "data_logic_module": "keyword_lab_data",
        "inputs": ["workspace_id", "storefront_ids", "date_range"],
        "description": "Export keyword lab data with date filtering"
    },
    
    "keyword_performance": {
        "name": "Keyword Performance",
        "data_logic_module": "keyword_performance_data",
        "inputs": ["workspace_id", "storefront_ids", "date_range", "device_type", "display_type", "product_position"],
        "description": "Export keyword performance data with advanced filtering options"
    },
    
    "product_tracking": {
        "name": "Product Tracking",
        "data_logic_module": "product_tracking_data",
        "inputs": ["workspace_id", "storefront_ids", "date_range"],
        "description": "Export product tracking data"
    },
    
    "competition_landscape": {
        "name": "Competition Landscape",
        "inputs": ["workspace_id", "storefront_ids", "date_range"],
        "description": "Export competition landscape data (placeholder)"
    },
    
    "storefront_optimization": {
        "name": "Storefront Optimization",
        "data_logic_module": "storefront_optimization_data",
        "inputs": ["workspace_id", "storefront_ids", "date_range"],
        "description": "Export storefront optimization data"
    },

    "campaign_optimization": {
        "name": "Campaign Optimization",
        "data_logic_module": "campaign_optimization_data",
        "inputs": ["workspace_id", "storefront_ids", "date_range"],
        "description": "Export campaign optimization data"
    }
}

# --- Helper Functions ---
def get_input_config(field_name: str) -> Optional[Dict[str, Any]]:
    """Get configuration for a specific input field."""
    return INPUT_FIELDS.get(field_name)

def get_data_source_config(data_source: str) -> Optional[Dict[str, Any]]:
    """Get configuration for a specific data source."""
    return DATA_SOURCE_CONFIGS.get(data_source)

def get_required_inputs(data_source: str) -> List[str]:
    """Get list of required input fields for a data source."""
    config = get_data_source_config(data_source)
    if not config:
        return []
    
    required_fields = []
    for field_name in config["inputs"]:
        field_config = get_input_config(field_name)
        if field_config and field_config.get("required", False):
            required_fields.append(field_name)
    
    return required_fields

def get_optional_inputs(data_source: str) -> List[str]:
    """Get list of optional input fields for a data source."""
    config = get_data_source_config(data_source)
    if not config:
        return []
    
    optional_fields = []
    for field_name in config["inputs"]:
        field_config = get_input_config(field_name)
        if field_config and not field_config.get("required", False):
            optional_fields.append(field_name)
    
    return optional_fields

def get_sql_params_mapping(data_source: str) -> Dict[str, str]:
    """Get mapping of input fields to SQL parameters for a data source."""
    config = get_data_source_config(data_source)
    if not config:
        return {}
    
    mapping = {}
    for field_name in config["inputs"]:
        field_config = get_input_config(field_name)
        if field_config:
            if "sql_params" in field_config:
                # Handle fields that map to multiple SQL params (like date_range)
                for i, param in enumerate(field_config["sql_params"]):
                    mapping[f"{field_name}_{i}"] = param
            else:
                mapping[field_name] = field_config["sql_param"]
    
    return mapping

def validate_data_source(data_source: str) -> bool:
    """Check if a data source is valid."""
    return data_source in DATA_SOURCE_CONFIGS

def get_all_data_sources() -> List[str]:
    """Get list of all available data sources."""
    return list(DATA_SOURCE_CONFIGS.keys())

# Internal Data Export Tool - Technical Documentation

## 1. Project Overview

This internal tool provides a self-service data export platform for company employees to access and download formatted datasets without requiring SQL knowledge or developer intervention. The tool eliminates manual export requests and provides 24/7 access to business-critical data.

**Target Users:** Internal company employees (Marketing, Analytics, Business Intelligence teams)

- **Core Technology**: Python 3.13
- **Framework**: Streamlit
- **Database**: SingleStore/MySQL with SQLAlchemy ORM
- **Key Libraries**: Pandas, SingleStoreDB, SQLAlchemy, python-dotenv

---

## 2. Project Structure

The project follows a modular, configuration-driven architecture to minimize code changes when adding new reports.

```
/Export_data
├── .env                    # Environment variables (DB credentials)
├── .gitignore             # Git ignore rules
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── assets/
│   └── style.css          # Custom CSS styling
├── data_logic/            # Data access layer
│   ├── sql/               # Raw SQL query files
│   │   ├── *_data.sql     # Main data queries
│   │   └── *_count.sql    # Row count queries
│   └── *_data.py          # Query execution modules
├── pages/                 # Streamlit pages (auto-discovered)
│   ├── 1_Help.py          # User documentation
│   ├── 2_Storefront_in_Workspace.py
│   ├── 3_Keyword_Lab.py
│   ├── 4_Digital_Shelf_Analytics.py
│   └── 5_Marketing_Automation.py
└── utils/                 # Core system components
    ├── __init__.py
    ├── config.py          # Project configuration
    ├── database.py        # Database connection management
    ├── helpers.py         # Session state and utilities
    ├── input_config.py    # 🧠 Input field definitions and data source configs
    ├── input_validator.py # Dynamic validation engine
    ├── dynamic_ui.py      # Dynamic UI generation
    ├── logic.py           # Business logic and data processing
    └── page_config.py     # Page structure definitions
```

---

## 3. Core Architecture: Configuration-Driven System

The application uses a **configuration-driven architecture** where UI, validation, and data access are automatically generated from declarative configurations. This design minimizes code changes when adding new reports.

### Key Components:

#### **🧠 `utils/input_config.py` - The Configuration Brain**
- **Master configuration file** defining all input fields and data sources
- `INPUT_FIELDS`: Defines reusable input components (text, date_range, select)
- `DATA_SOURCE_CONFIGS`: Maps data sources to their required inputs and modules
- Each field includes validation rules, UI properties, and SQL parameter mappings

#### **🎨 `utils/dynamic_ui.py` - The UI Generator**
- Dynamically renders forms based on input configurations
- Handles form validation, error display, and user interactions
- Manages the complete export workflow (preview → validation → export → download)
- Includes state management for different export stages

#### **⚡ `utils/logic.py` - The Processing Engine**
- **Dynamic module loading**: Imports data modules at runtime based on configuration
- SQL parameter building and query execution
- Row count validation (50k limit enforcement)
- Caching and error handling

#### **🛡️ `utils/input_validator.py` - The Validation Engine**
- Configuration-driven validation rules
- Cross-field validation (e.g., date range limits based on storefront count)
- SQL injection prevention through parameterized queries

#### **📋 `utils/page_config.py` - The Page Structure**
- Defines application pages and tab structures
- Maps pages to data source configurations
- Handles tab state management and navigation

---

## 4. Data Flow Architecture

### Complete User Journey:
```
1. User selects page → 2. Load configuration → 3. Render dynamic form
                ↓
4. User fills form → 5. Validate inputs → 6. Build SQL parameters
                ↓
7. Check row count → 8. Load preview (500 rows) → 9. Display results
                ↓
10. User exports → 11. Load full data → 12. Generate CSV → 13. Download
```

### Technical Data Flow:
```python
# 1. Configuration Resolution
page_config = PAGES["4_Digital_Shelf_Analytics.py"]
data_source = selected_tab.data_source_key  # e.g., "keyword_performance"
config = DATA_SOURCE_CONFIGS[data_source]

# 2. Dynamic Form Generation
for field_name in config["inputs"]:
    field_config = INPUT_FIELDS[field_name]
    render_input_widget(field_config)

# 3. Dynamic Module Loading
module_name = config["data_logic_module"]  # e.g., "keyword_performance_data"
data_module = importlib.import_module(f"data_logic.{module_name}")
get_query_func = getattr(data_module, 'get_query')

# 4. Query Execution
sql_query = get_query_func("data")  # or "count"
result_df = execute_query(sql_query, validated_params)
```

---

## 5. Available Reports

### Current Data Sources:
- **🛍️ Storefront in Workspace**: Lists all storefronts within a workspace
- **🔬 Keyword Lab**: Keyword discovery and performance metrics
- **📈 Keyword Performance**: Advanced keyword analytics with filtering
- **📦 Product Tracking**: Product positioning and sales data
- **🏟️ Competition Landscape**: Competitive analysis and market insights
- **🎯 Storefront Optimization**: Performance optimization metrics
- **🚀 Campaign Optimization**: Campaign performance and ROI analysis

### Input Field Types:
- **Text Fields**: Workspace ID, Storefront EIDs (with validation)
- **Date Ranges**: Preset options (Last 30 days, This month, Custom)
- **Select Fields**: Device Type, Display Type, Product Position
- **Smart Validation**: Cross-field rules, row limits, format checking

---

## 6. Adding New Reports (Zero Core Changes Required)

The configuration-driven architecture allows adding new reports with **no changes to core application logic**.

### Step-by-Step Process:

#### **Step 1: Create SQL Files**
```sql
-- data_logic/sql/new_report_data.sql
SELECT column1, column2, column3
FROM your_table t1
JOIN another_table t2 ON t1.id = t2.foreign_id
WHERE t1.workspace_id = :workspace_id
  AND t1.created_date BETWEEN :start_date AND :end_date
  AND (:storefront_ids IS NULL OR t1.storefront_id IN :storefront_ids)
ORDER BY t1.created_date DESC;

-- data_logic/sql/new_report_count.sql  
SELECT COUNT(1)
FROM (
    -- Same query as above but wrapped in COUNT
) subquery;
```

#### **Step 2: Create Data Module**
```python
# data_logic/new_report_data.py
from utils.config import PROJECT_ROOT
import streamlit as st

def _get_query_from_file(file_path: str) -> str:
    """Helper function to read SQL file safely."""
    path = PROJECT_ROOT / "data_logic" / "sql" / file_path
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError as e:
        st.error(f"Query file not found: {path.resolve()}")
        raise e

query_params = {
    "data": _get_query_from_file("new_report_data.sql"),
    "count": _get_query_from_file("new_report_count.sql")
}

def get_query(query_name: str) -> str:
    """Gets a query by name from the pre-loaded dictionary."""
    return query_params.get(query_name, "")
```

#### **Step 3: Add Configuration**
```python
# utils/input_config.py - Add to DATA_SOURCE_CONFIGS
"new_report": {
    "name": "New Report Name",
    "data_logic_module": "new_report_data",
    "inputs": ["workspace_id", "storefront_ids", "date_range"],
    "description": "Description of what this report provides"
}
```

#### **Step 4: Add Page Structure**
```python
# utils/page_config.py - Add to PAGES dictionary
"6_New_Report.py": Page(
    title="New Report",
    icon="📊",
    tabs=[
        TabPage(title="New Report", data_source_key='new_report')
    ]
)
```

#### **Step 5: Create Page File**
```python
# pages/6_New_Report.py
import streamlit as st
from utils.page_config import render_page
from utils.helpers import initialize_session_state, display_user_message
from utils.page_config import PAGES
import os

initialize_session_state()
display_user_message()

script_name = os.path.basename(__file__)
page_config = PAGES.get(script_name)

if page_config:
    render_page(page_config)
else:
    st.error(f"Page configuration for {script_name} not found.")
```

**Result**: New report automatically includes form generation, validation, preview, export, and error handling!

---

## 7. System Features & Safeguards

### **Built-in Safety Features:**
- **50,000 row limit**: Prevents server overload and accidental massive exports
- **Date range limits**: Configurable based on storefront count (1-2 stores: 60 days, 3+ stores: 30 days)
- **Input validation**: Real-time validation with helpful error messages
- **SQL injection protection**: Parameterized queries throughout
- **Connection pooling**: Limited concurrent database connections (10 max)

### **User Experience Features:**
- **Smart preview**: 500-row preview before full export
- **Progress tracking**: Clear workflow stages (preview → export → download)
- **Error recovery**: Helpful suggestions when things go wrong
- **Tab state persistence**: Maintains user's position when errors occur
- **Session memory**: Remembers form inputs across page navigation

### **Performance Optimizations:**
- **Query caching**: Results cached for 1 hour (configurable)
- **Lazy loading**: Only loads data when requested
- **Memory efficiency**: Streaming CSV generation for large datasets
- **Resource limits**: Automatic cleanup of cached data

---

## 8. Environment Setup & Deployment

### **Development Setup:**

1. **Clone and Setup Environment:**
   ```bash
   git clone [repository-url]
   cd Export_data
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Configuration:**
   ```bash
   # Create .env file with database credentials
   DB_HOST=your_database_host
   DB_PORT=3306
   DB_USER=your_username  
   DB_PASSWORD=your_password
   DB_NAME=your_database_name
   ```

3. **Run Application:**
   ```bash
   streamlit run main.py
   ```

### **Production Deployment:**
- **Platform**: Streamlit Cloud or Docker container
- **Resources**: 2 CPU cores, 4GB RAM (supports ~20 concurrent users)
- **Database**: Read-only connection to production database
- **Storage**: Stateless (no persistent data storage required)

### **Dependencies:**
```python
streamlit                    # Web framework
pandas                      # Data manipulation
singlestoredb              # Database connector
SQLAlchemy                 # ORM and query building
sqlalchemy-singlestoredb   # SingleStore SQLAlchemy dialect
python-dotenv              # Environment variable management
numpy                      # Numerical operations
```

---

## 9. Technical Specifications

### **Architecture Principles:**
- **Configuration-driven**: 90% of changes require only config updates
- **Separation of concerns**: Clear boundaries between UI, logic, and data layers
- **Dynamic loading**: Runtime module imports eliminate hardcoded dependencies
- **Fail-safe design**: Multiple error handling layers with graceful degradation

### **Performance Characteristics:**
- **Startup time**: ~2 seconds
- **Form generation**: <100ms (dynamic rendering)
- **Preview loading**: 1-3 seconds (depends on query complexity)
- **Full export**: 30 seconds - 2 minutes (depends on data size)
- **Memory usage**: ~50MB base + 5-20MB per cached query

### **Security Features:**
- **Read-only database access**: No data modification capabilities
- **Parameterized queries**: Complete SQL injection protection
- **Session-based security**: No persistent authentication tokens
- **Input validation**: Server-side validation of all user inputs
- **Audit capabilities**: All queries and exports can be logged

---

## 10. Troubleshooting & Maintenance

### **Common Issues:**
- **"No data found"**: Check workspace ID, storefront IDs, and date ranges
- **"Data too large"**: Reduce date range or storefront count to stay under 50k rows
- **Database errors**: Check connection pool status and query syntax
- **Performance issues**: Monitor cache hit rates and connection utilization

### **Monitoring Points:**
- Database connection pool utilization
- Query execution times and cache hit rates
- User error rates and common failure patterns
- System resource usage (memory, CPU)

### **Maintenance Tasks:**
- Regular cache cleanup (automatic)
- Database connection health monitoring
- User feedback review and feature requests
- Periodic performance optimization

---

## 11. Support & Documentation

### **For End Users:**
- **Help Page**: Built-in comprehensive user guide (`pages/1_Help.py`)
- **Interactive tooltips**: Contextual help throughout the application
- **Error messages**: Clear, actionable guidance when issues occur

### **For Developers:**
- **This README**: Technical architecture and development guide
- **Code comments**: Comprehensive documentation in critical functions
- **Configuration files**: Self-documenting input and page definitions

### **Internal Support:**
- **Primary Contact**: IrvineCao (tool creator and maintainer)
- **Escalation**: Technical team for infrastructure issues
- **Business Logic**: Data team for query accuracy and new requirements

---

**This tool represents a successful transformation from manual, bottlenecked data exports to a scalable, self-service platform that empowers users while reducing operational overhead.**
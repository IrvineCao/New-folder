# Technical Documentation: Data Export Tool

## 1. Project Overview

This document provides a detailed technical overview of the Data Export Tool. The primary goal of this application is to provide a self-service portal for users to export formatted, clean datasets directly from the database without needing SQL knowledge or developer intervention.

- **Core Technology**: Python
- **Framework**: Streamlit
- **Key Libraries**: Pandas, SQLAlchemy, mysql-connector-python

---

## 2. Project Structure

The project follows a modular structure to separate concerns and improve maintainability.

```
/Export_data
|-- .env                  # Environment variables (DB credentials)
|-- main.py               # Main application entry point
|-- requirements.txt      # Python dependencies
|-- assets/               # CSS styles, images, etc.
|-- data_logic/           # Data access layer
|   |-- sql/              # Raw SQL query files
|   |-- *.py              # Python modules to execute queries
|-- pages/                # UI view files for each Streamlit page
|-- utils/                # Core logic, configuration, and helpers
|   |-- page_config.py    # Defines UI pages and tabs
|   |-- input_config.py   # **CRITICAL**: Defines all inputs and data sources
|   |-- dynamic_ui.py     # Dynamically generates UI components
|   |-- logic.py          # Business logic, validation, and query parameter building
|   |-- input_validator.py# Input validation functions
|   |-- helpers.py        # Session state and other helper functions
|   |-- db_connect.py     # Database connection handler
```

---

## 3. Core Architecture: Configuration-Driven System

The application is built on a **configuration-driven architecture**. The goal is to minimize code changes when adding new reports or input fields. The logic, UI, and validation are all dynamically generated based on a central set of configuration files, primarily `input_config.py`.

### Key Components:

1.  **`utils/input_config.py` (The Brain)**
    - This is the most important file in the architecture.
    - It contains a master dictionary `DATA_SOURCE_CONFIG` that maps a unique `data_source_key` (e.g., `"keyword_lab"`) to its entire configuration.
    - Each configuration specifies:
        - `data_logic_module`: The Python file in `data_logic/` responsible for fetching the data.
        - `inputs`: A list of dictionaries, where each dictionary defines an input field for the UI (e.g., a date range picker, a text input).
        - Each input definition includes its `name`, `label`, `type` (for validation), `required` status, and other UI-related properties.

2.  **`utils/page_config.py` (The Skeleton)**
    - Defines the structure of the application's pages and tabs that appear in the Streamlit sidebar.
    - Each page or tab is mapped to a `data_source_key` from `input_config.py`. This link tells the application which configuration to use for a given page.

3.  **`utils/dynamic_ui.py` (The Face)**
    - Reads the configurations from `page_config.py` and `input_config.py`.
    - It dynamically renders the correct input form based on the `inputs` defined for the current page's `data_source_key`.
    - It also handles the display of preview data and the download button.

4.  **`utils/logic.py` (The Conductor)**
    - Acts as the bridge between the UI and the data layer.
    - It receives user inputs from the form, validates them against the rules in `input_config.py` (using `input_validator.py`), and builds the final parameter dictionary for the SQL query.
    - **Crucially, it dynamically imports the correct `data_logic_module` at runtime based on the configuration in `input_config.py`. This eliminates the need for manual imports or mappings when adding new data sources.**

---

## 4. Data Flow (End-to-End)

Here is the step-by-step data flow for a typical user interaction:

1.  **Page Load**: A user selects a page (e.g., "Marketing Automation"). The corresponding file in `pages/` is run.
2.  **Render Page**: The page file calls `render_page(page_config)`.
3.  **Get Config**: `render_page` identifies the `data_source_key` (e.g., `"storefront_optimization"`) from `page_config.py`.
4.  **Generate UI**: `dynamic_ui.py` uses this key to look up the configuration in `input_config.py` and dynamically renders the required input form.
5.  **User Input**: The user fills out the form and clicks "Preview Data".
6.  **Validation & Param Building**: The inputs are sent to `logic.py`. It validates them and constructs a parameter dictionary (e.g., `{'workspace_id': 123, 'start_date': '2023-01-01', ...}`).
7.  **Data Fetching**: `logic.py` dynamically imports the correct `data_logic_module` (e.g., `storefront_optimization_data`) using the configuration and calls its `get_data` function, passing the parameters.
8.  **SQL Execution**: The `storefront_optimization_data.py` module reads the corresponding SQL query from `data_logic/sql/sf_opt_data.sql`, injects the parameters, and executes it against the database.
9.  **Display Results**: The function returns a Pandas DataFrame, which is stored in the session state and displayed as a preview table by `dynamic_ui.py`.
10. **Download**: If the user clicks "Download Full Report", the same process runs again but without a `LIMIT` clause in the SQL, and the resulting DataFrame is served as a CSV file.

---

## 5. How to Add a New Report (Developer Workflow)

Adding a new data export page is straightforward. Thanks to the dynamic module loading in `utils/logic.py`, **you only need to add/modify configuration and SQL files.** No changes to the core Python logic in `utils/` are necessary.

**Step 1: Create SQL Files**

In `data_logic/sql/`, create two new SQL files for your new data source (e.g., `new_report`).

-   `new_report_data.sql`: The main query. Use named parameters that match the `name` you will define in `input_config.py` (e.g., `:workspace_id`, `:start_date`).
-   `new_report_count.sql`: A query to get the total row count for the preview (e.g., `SELECT count(*) ...`).

**Step 2: Create Data Logic Module**

In `data_logic/`, create a new Python file: `new_report_data.py`.
This file should contain a dictionary that read the SQL files and execute them.

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

**Step 3: Configure the Data Source**

In `utils/input_config.py`, add a new entry to the `DATA_SOURCE_CONFIG` dictionary.

```python
# utils/input_config.py
DATA_SOURCE_CONFIG = {
    # ... other sources
    "new_report": {
        "data_logic_module": "new_report_data",
        "description": "Description for your new report.",
        "inputs": [
            # Define all required and optional inputs here
            # Example:
            {
                "name": "workspace_id",
                "label": "Workspace ID",
                "type": "numeric",
                "required": True,
            },
            {
                "name": "date_range",
                "label": "Select Date Range",
                "type": "date_range",
                "required": True,
            }
        ]
    }
}
```

**Step 4: Add the Page to the UI**

In `utils/page_config.py`, add a new `Page` or `TabPage` object to the `PAGES` dictionary.

```python
# utils/page_config.py
PAGES = {
    # ... other pages
    "new_report_page": Page(
        title="My New Report",
        icon="📊",
        data_source_key="new_report"
    )
}
```

**Step 5: Create the Page File**

In the `pages/` directory, create a new file (e.g., `6_New_Report.py`). The number prefix controls the order in the sidebar.

```python
# pages/6_New_Report.py
import streamlit as st
from utils.page_config import PAGES, render_page

st.set_page_config(layout="wide")

page_config = PAGES["new_report_page"]
render_page(page_config)
```

That's it. The application will now dynamically generate the new page, form, and data export functionality.

---

## 6. Environment Setup

1.  **Clone the repository.**
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables:**
    - Create a `.env` file in the project root by copying `.env.example` (if it exists) or creating it from scratch.
    - Fill in the database connection details:
      ```
      DB_HOST=your_host
      DB_USER=your_user
      DB_PASSWORD=your_password
      DB_NAME=your_database
      ```
5.  **Run the application:**
    ```bash
    streamlit run main.py
    ```

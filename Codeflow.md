# Codeflow

## 1. User Interaction Flow

### 1.1 Application Initialization

```md
main.py
    │
    └──▶ display_main_ui()  # Main UI function that renders the application interface
            │
            ├──▶ Sidebar Navigation
            │       │
            │       ├──▶ 'Keyword Lab' - For exporting keyword lab data
            │       ├──▶ 'Digital Shelf Analytics' - Contains two tabs:
            │       │       ├──▶ 'Keyword Performance' - For keyword performance data
            │       │       └──▶ 'Product Tracking' - For product tracking data
            │       └──▶ 'Please Read' - Help documentation
            │
            │
            ├──▶ create_input_form()
            │       │
            │       ├──▶ Creates a standardized input form with:
            │       │       - Workspace ID (numeric)
            │       │       - Storefront EID (comma-separated, max 5)
            │       │       - Date range picker (default: last 30 days)
            │       │
            │       └──▶ Validates date range (start date cannot be after end date)
            │
            │
            ├──▶ "Get Data" Button Click
            │       │
            │       └──▶ handle_get_data_button()
            │               │
            │               ├──▶ handle_export_process()
            │               │       │
            │               │       ├──▶ validate_inputs()
            │               │       │       - Validates workspace ID format
            │               │       │       - Validates storefront EID format
            │               │       │       - Validates date range
            │               │       │
            │               │       ├──▶ process_storefront_input()
            │               │       │       - Converts comma-separated string to list of integers
            │               │       │
            │               │       └──▶ get_data(query_type="count")
            │               │               - Executes count query to check data volume
            │               │               - Returns number of rows that match the criteria
            │               │
            │               └──▶ Updates session state with:
            │                       - workspace_id
            │                       - storefront_ids
            │                       - date range
            │                       - data_source
            │                       - num_row (from count query)
            │
            └──▶ Page Note ("Please Read Im Begging You") ← Hiển thị file help.md nếu người dùng chọn trang này
```

## 2. Stage Management

### 2.1 Stage: 'waiting_confirmation'

- Triggered when data volume is between 10,000 and 50,000 rows
- Displays a warning message with the row count
- Shows a confirmation checkbox and button

```python
if num_rows > 10000 and num_rows <= 50000:
    st.session_state.stage = 'waiting_confirmation'
```

### 2.2 Stage: 'loading'

- Triggered when data volume is within acceptable limits
- Loads the actual data from the database
- Updates session state with the loaded data

```python
@st.cache_data(show_spinner=False, ttl=3600, persist=True)
def get_data(workspace_id, storefront_id, start_date, end_date, query_type: str, data_source: str)
```

### 2.3 Stage: 'loaded'

- Data has been successfully loaded
- Displays a success message
- Shows a preview of the data (first 500 rows)
- Provides download button for the full dataset
- Validates that the current page matches the loaded data source

## 3. Data Export Process

### 3.1 Input Validation

```python
def validate_inputs(workspace_id, storefront_input, start_date, end_date):
    # Validates all input fields
    # Returns list of error messages if any
    pass
```

### 3.2 Data Volume Check

- Executes a count query to determine result set size
- Implements different behaviors based on row count:
  - 0 rows: Shows "No data found" message
  - 1-10,000 rows: Proceeds with data loading
  - 10,001-50,000 rows: Requires user confirmation
  - 50,000+ rows: Rejects with "Too much data" message

### 3.3 Data Retrieval

- Uses SQLAlchemy for database operations
- Implements connection pooling for better performance
- Caches query results to improve performance
- Handles both count and data retrieval with the same function

## 4. Data Loading and Export

### 4.1 Data Loading Process

```python
def load_and_store_data(data_source: str):
    # Loads data based on the current parameters in session state
    # Handles errors and updates UI state accordingly
    pass
```

### 4.2 Data Export

- Converts pandas DataFrame to CSV format
- Provides a download button for the user
- Implements streaming for large datasets to avoid memory issues

### 4.3 Error Handling

- Validates database connections
- Handles query timeouts
- Provides user-friendly error messages
- Implements proper session state cleanup on errors

## 5. Performance Considerations

### 5.1 Caching

- Uses `@st.cache_data` decorator for expensive computations
- Implements time-based cache invalidation (TTL: 1 hour)
- Caches query results to avoid redundant database calls

### 5.2 Connection Pooling

- Uses SQLAlchemy's QueuePool for database connections
- Configures optimal pool size and timeouts
- Implements connection recycling to prevent stale connections

### 5.3 Data Chunking

- Processes large datasets in chunks
- Implements streaming for data export
- Limits preview data to first 500 rows for better performance

## 6. Security Considerations

### 6.1 Input Validation

- Validates all user inputs
- Sanitizes database queries to prevent SQL injection
- Implements proper error handling

### 6.2 Database Security

- Uses connection pooling with limited connections
- Implements proper credential management
- Restricts database permissions to necessary operations only

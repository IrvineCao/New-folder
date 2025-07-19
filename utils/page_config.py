"""
Page Configuration for the Streamlit App.

This module centralizes the configuration for all pages in the application,
making it easy to add, remove, or modify pages and their tabs without
touching the core rendering logic.

HOW TO ADD A NEW PAGE:
1.  Create a new Python file in the `pages/` directory (e.g., `pages/4_New_Report.py`).
    The number prefix determines the order in the sidebar.
2.  In your new file, add the boilerplate code to render a page using `render_page`.
    ```python
    import os
    from utils.page_manager import render_page
    from utils.page_config import PAGES

    script_name = os.path.basename(__file__)
    page_config = PAGES.get(script_name)

    if page_config:
        render_page(page_config)
    ```
3.  Add a new entry to the `PAGES` dictionary below. The key must match the
    filename you created (e.g., "4_New_Report.py").
4.  Define the `Page` object with its title, icon, and a list of `TabPage` objects.
    - `title`: The title displayed at the top of the page.
    - `icon`: The emoji icon for the page.
    - `tabs`: A list of `TabPage` objects that will appear as tabs on the page.

HOW TO CONFIGURE A TAB:
Each `TabPage` can be configured with the following parameters:
- `title`: The text displayed on the tab.
- `data_source_key`: A unique key (e.g., 'kwl', 'sf') that maps to a specific
  set of SQL queries in the `data_logic` modules. This is required.
- `required_inputs`: A list of input fields that must be filled out for this tab.
  Options: ['workspace_id', 'storefront_id', 'date_range'].
  If not provided, all inputs are considered required by default.
- `show_kw_pfm_options`: Set to `True` to display additional filtering options
  specific to Keyword Performance data.
- `is_placeholder`: Set to `True` to create a disabled tab that serves as a
  placeholder for a future feature.
"""
from utils.page_manager import Page, TabPage

PAGES = {
    "1_Storefront_in_Workspace.py": Page(
        title="Storefront in Workspace",
        icon="🛍️",
        tabs=[
            TabPage(title="Storefront in Workspace", data_source_key='sf', required_inputs=['workspace_id'])
        ]
    ),
    "2_Keyword_Lab.py": Page(
        title="Keyword Lab",
        icon="🔬",
        tabs=[
            TabPage(title="Keyword Lab", data_source_key='kwl')
        ]
    ),
    "3_Digital_Shelf_Analytics.py": Page(
        title="Digital Shelf Analytics",
        icon="📊",
        tabs=[
            TabPage(title="Keyword Performance", data_source_key='kw_pfm', show_kw_pfm_options=True),
            TabPage(title="Product Tracking", data_source_key='pt'),
            TabPage(title="Competition Landscape", data_source_key='cl', is_placeholder=True)
        ]
    )
}

import streamlit as st
from dataclasses import dataclass
from typing import List
from utils.dynamic_ui import (
    create_dynamic_input_form, 
    display_validation_errors, 
    create_action_buttons, 
    display_data_exporter
)
from utils.helpers import display_call_trace

@dataclass
class TabPage:
    title: str
    data_source_key: str
    is_placeholder: bool = False

@dataclass
class Page:
    title: str
    icon: str
    tabs: List[TabPage]

PAGES = {
    "2_Storefront_in_Workspace.py": Page(
        title="Storefront in Workspace",
        icon="🛍️",
        tabs=[
            TabPage(title="Storefront in Workspace", data_source_key='storefront_in_workspace')
        ]
    ),
    "3_Keyword_Lab.py": Page(
        title="Keyword Lab",
        icon="🔬",
        tabs=[
            TabPage(title="Keyword Lab", data_source_key='keyword_lab')
        ]
    ),
    "4_Digital_Shelf_Analytics.py": Page(
        title="Digital Shelf Analytics",
        icon="📊",
        tabs=[
            TabPage(title="Keyword Performance", data_source_key='keyword_performance'),
            TabPage(title="Product Tracking", data_source_key='product_tracking'),
            TabPage(title="Competition Landscape", data_source_key='competition_landscape')
        ]
    ),
    "5_Marketing_Automation.py": Page(
        title="Marketing Automation",
        icon="🤖",
        tabs=[
            TabPage(title="Storefront Optimization", data_source_key='storefront_optimization'),
            TabPage(title="Campaign Optimization", data_source_key='campaign_optimization')
        ]
    ),
}


def get_current_tab_from_data_source(page: Page):
    """
    Determine which tab should be active based on current data_source in session state.
    This helps maintain tab state when errors occur.
    """
    current_data_source = st.session_state.get('params', {}).get('data_source')
    if not current_data_source:
        return 0  # Default to first tab
    
    # Find which tab corresponds to the current data source
    for i, tab in enumerate(page.tabs):
        if tab.data_source_key == current_data_source:
            return i
    
    return 0  # Default to first tab if not found


def get_safe_tab_index(page: Page) -> int:
    """
    Get a safe tab index that's guaranteed to be within bounds.
    """
    page_tab_key = f"tab_index_{page.title.replace(' ', '_').lower()}"
    
    # Initialize tab index if not exists
    if page_tab_key not in st.session_state:
        st.session_state[page_tab_key] = 0
    
    stored_index = st.session_state[page_tab_key]
    max_index = len(page.tabs) - 1
    
    # Validate stored index is within bounds
    if stored_index < 0 or stored_index > max_index:
        st.session_state[page_tab_key] = 0
        return 0
    
    # Check if we need to maintain tab state based on current operation
    current_tab_from_data = get_current_tab_from_data_source(page)
    if current_tab_from_data is not None and 0 <= current_tab_from_data <= max_index:
        st.session_state[page_tab_key] = current_tab_from_data
        return current_tab_from_data
    
    return stored_index


def render_page(page: Page):
    st.set_page_config(page_title=page.title, layout="wide")
    st.title(page.title)

    if len(page.tabs) > 1:
        tab_titles = [tab.title for tab in page.tabs]
        
        # Get safe tab index
        safe_tab_index = get_safe_tab_index(page)
        
        # Create session state key for this specific page's tab
        page_tab_key = f"tab_index_{page.title.replace(' ', '_').lower()}"
        
        # Use radio buttons for better state control
        selected_tab_name = st.radio(
            "📋 Select Report Type:",
            tab_titles,
            index=safe_tab_index,
            key=f"radio_tab_{page.title.replace(' ', '_').lower()}",
            horizontal=True
        )
        
        # Update session state when selection changes
        selected_tab_index = tab_titles.index(selected_tab_name)
        st.session_state[page_tab_key] = selected_tab_index
        
        # Add some styling
        st.markdown("---")
        
        # Render the selected tab content
        if 0 <= selected_tab_index < len(page.tabs):
            selected_tab = page.tabs[selected_tab_index]
            render_tab_content(selected_tab)
        else:
            # Fallback to first tab if index is invalid
            st.error("Invalid tab selection. Showing first tab.")
            render_tab_content(page.tabs[0])
        
    else:
        # Single tab case
        render_tab_content(page.tabs[0])

    # Always display the call trace for debugging
    display_call_trace()


def render_tab_content(tab_content: TabPage):
    """Render content for a single tab."""
    if tab_content.is_placeholder:
        st.header(tab_content.title)
        st.write("Coming soon...")
        return
    
    # Add tab title for clarity
    st.subheader(f"📊 {tab_content.title}")
    
    # Use new dynamic form creation
    input_values, validation_errors = create_dynamic_input_form(tab_content.data_source_key)
    
    # Display validation errors if any
    has_errors = display_validation_errors(validation_errors)
    
    # Show action buttons only if we're in initial stage or different data source
    show_button = (st.session_state.get('stage', 'initial') == 'initial' or 
                   st.session_state.get('params', {}).get('data_source') != tab_content.data_source_key)
    
    if show_button:
        create_action_buttons(tab_content.data_source_key, input_values, validation_errors)
    
    # Display data exporter if we have data for this source
    if st.session_state.get('params', {}).get('data_source') == tab_content.data_source_key and st.session_state.get('stage', 'initial') != 'initial':
        display_data_exporter()
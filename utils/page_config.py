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



def render_page(page: Page):
    st.set_page_config(page_title=page.title, layout="wide")
    st.title(page.title)

    if len(page.tabs) > 1:
        tab_titles = [tab.title for tab in page.tabs]
        st_tabs = st.tabs(tab_titles)
    else:
        st_tabs = [st.container()]

    for i, tab_content in enumerate(page.tabs):
        with st_tabs[i]:
            if tab_content.is_placeholder:
                st.header(tab_content.title)
                st.write("Coming soon...")
                continue
            
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

    # Always display the call trace for debugging
    display_call_trace()

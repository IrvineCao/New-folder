import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable
from utils.ui_components import create_input_form, display_data_exporter
from utils.logic import handle_get_data_button

@dataclass
class TabPage:
    title: str
    data_source_key: str
    show_kw_pfm_options: bool = False
    is_placeholder: bool = False
    required_inputs: List[str] = None

@dataclass
class Page:
    title: str
    icon: str
    tabs: List[TabPage]

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

            st.header(f"{tab_content.title} Data Export")
            
            workspace_id, storefront_input, start_date, end_date, pfm_options = create_input_form(
                tab_content.data_source_key, 
                show_kw_pfm_options=tab_content.show_kw_pfm_options,
                required_inputs=tab_content.required_inputs
            )
            
            show_button = (st.session_state.stage == 'initial' or 
                           st.session_state.params.get('data_source') != tab_content.data_source_key)
            
            if show_button:
                if st.button("Preview Data", type="primary", use_container_width=True, key=f'get_data_{tab_content.data_source_key}'):
                    handle_get_data_button(
                        workspace_id, storefront_input, start_date, end_date, 
                        tab_content.data_source_key,
                        **pfm_options
                    )
            
            if st.session_state.params.get('data_source') == tab_content.data_source_key and st.session_state.stage != 'initial':
                display_data_exporter()

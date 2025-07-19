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

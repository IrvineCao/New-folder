import streamlit as st

st.set_page_config(layout="wide", page_title="Help & User Guide")

# --- Custom CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/style.css")

st.markdown("<h1 class='main-title'>Help & User Guide</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Your complete guide to using the Data Export Tool.</div>", unsafe_allow_html=True)
st.divider()

# --- User Guide ---
st.header("🚀 Getting Started: Your First Export")
st.markdown("""
Welcome! This guide will walk you through everything you need to know to get the data you need, quickly and easily.
""")

# --- Step 1 ---
with st.container():
    st.subheader("Step 1: Select Your Report")
    st.markdown("""
    The first step is to choose the type of data you want to export. Use the navigation sidebar on the left to find the report you need. Reports are grouped into categories:

    - **Storefront in Workspace**: Provides a list of all storefronts associated with a specific workspace.
    - **Keyword Lab**: Offers deep insights into keyword performance, search volume, and competitor data.
    - **Digital Shelf Analytics**: A collection of reports for analyzing keyword performance, product tracking, and more.
    """)

# --- Step 2 ---
with st.container():
    st.subheader("Step 2: Configure Your Parameters")
    st.markdown("""
    Next, you need to tell the system exactly what data to pull by setting the parameters. Fields marked with a red asterisk (`*`) are required.
    """)
    st.info("**Pro Tip:** The **Get Data** button will remain disabled until all required fields are filled correctly.")

    st.markdown("#### Required Parameters")
    st.markdown("""
    - **Workspace ID (`*`)**: This is the unique identifier for your workspace. You must enter a single, numeric ID.
    - **Storefront EID (`*`)**: Enter the EID for the storefront(s) you want to analyze. You can enter a single ID or multiple IDs separated by commas (e.g., `123, 456, 789`).
    - **Date Range (`*`)**: Select the start and end dates for your analysis. The data exported will be from within this time period.
    """)

    st.markdown("#### Optional Filters")
    st.markdown("""
    Some reports have optional filters to help you refine your results even further. You can leave these set to `None` to include all data, or select a specific option to narrow the results.
    - **Device Type**: Filter data based on whether the user was on a `Desktop` or `Mobile` device.
    - **Display Type**: Filter by how the product was displayed, such as `Paid`, `Organic`, `Top`.
    - **Product Position**: Filter by the position of the product, such as `-1 (All)`, `4`, `10`.
    """)

# --- Step 3 ---
with st.container():
    st.subheader("Step 3: Preview and Download")
    st.markdown("""
    Once your parameters are set, you're ready to get your data.
    """)
    st.markdown("1. **Click `🚀 Get Data`**: The system will fetch a preview of the first 500 rows. This helps you verify that the data is what you expected without waiting for a full export.")
    st.markdown("2. **Review the Preview Table**: A table will appear showing the preview data. Check the columns and rows to ensure everything looks correct.")
    st.markdown("3. **Download the Full Report**: If the preview is correct, click the **`📥 Download Full Report as CSV`** button. This will generate and download a complete CSV file with all the data that matches your parameters.")

st.divider()

# --- FAQ ---
st.header("🤔 Frequently Asked Questions")

with st.expander("Why is the 'Get Data' button disabled?"):
    st.markdown("The button is disabled if any required fields (marked with `*`) are empty or contain invalid data. Please check that you have entered a valid, numeric Workspace ID and at least one Storefront EID.")

with st.expander("How long will the full export take?"):
    st.markdown("Export time depends on the size of the data. For very large date ranges or many storefronts, it might take a few minutes. The preview is designed to be fast, while the full export is more comprehensive.")

with st.expander("What does 'None' mean in a filter?"):
    st.markdown("Selecting `None` in an optional filter means you are not applying that filter. For example, setting `Device Type` to `None` will include data from both Desktop and Mobile devices.")

with st.expander("Who can I contact for help?"):
    st.markdown("If you encounter an error or have questions about the data, please reach out to the Irvine.")

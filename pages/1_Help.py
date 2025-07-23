import streamlit as st

# --- Cấu hình trang ---
st.set_page_config(
    page_title="The Unofficial Rulebook",
    page_icon="📜",
    layout="wide"
)

# --- CSS tùy chỉnh - Dựa trên file CSS của trang chủ ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    body {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }

    /* Ẩn header và footer mặc định của Streamlit */
    .st-emotion-cache-18ni7ap, .st-emotion-cache-h4xjwg {
        display: none;
    }

    /* Áp dụng phong cách tiêu đề gradient cho trang Trợ giúp */
    .main-title {
        font-size: 4.0rem; /* Hơi nhỏ hơn một chút cho phù hợp với trang văn bản */
        font-weight: 900;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #ff007f, #00ffcc);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.2em 0;
    }

    /* Áp dụng phong cách tiêu đề phụ */
    .sub-header {
        text-align: center;
        font-size: 1.15rem;
        color: #a1a1aa;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
    }
    
    
    /* Làm cho các tiêu đề phụ (h2, h3) nổi bật hơn */
    h2, h3 {
        font-weight: 700;
        color: #ffffff;
    }
    
    /* THAY ĐỔI QUAN TRỌNG: Định dạng lại các hộp thông báo của Streamlit để phù hợp với chủ đề */
    div[data-testid="stInfo"],
    div[data-testid="stWarning"],
    div[data-testid="stError"] {
        background-color: rgba(255, 0, 127, 0.1); /* Nền màu hồng nhạt */
        border-left: 4px solid #ff007f; /* Viền trái màu hồng đậm */
        border-radius: 8px;
    }
    
    /* Thay đổi màu chữ bên trong hộp thông báo lỗi để dễ đọc hơn */
    div[data-testid="stError"] p {
        color: #ffc4e1; 
    }
</style>
""", unsafe_allow_html=True)


# --- Nội dung trang ---

# Sử dụng các lớp CSS đã định nghĩa ở trên
st.markdown("<h1 class='main-title'>The Unofficial Rulebook</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='sub-header'>
    So, you found it. The secret weapon. Legend has it, Irvine sacrificed a weekend of scrolling through memes to build this, all so he could finally free his DMs from the 'Hey, can you pull this for me real quick?' army.
    <br>
    Think of reading this guide as your small, silent 'thank you' for his sacrifice. It's the chill thing to do.
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()

# --- Mục 1: Bộ lọc ---
st.header("1. The Holy Trinity of Filters")
st.markdown("This is the most crucial part. It's where you tell the machine what you want. Garbage in, garbage out. Don't give us garbage.")

st.subheader("Workspace ID 💼")
st.markdown("This is the big one, the master key to your data kingdom. You should know this number. If you don't, you probably shouldn't be here. Just saying.")

st.subheader("Storefront EID 🏬")
st.markdown("Enter one or more Storefront EIDs, separated by commas. **CRITICAL RULE:** They must all belong to the same Workspace you entered above. Don't try to mix and match data from different universes. This tool is smart, but it's not a dimension-hopping wizard.")
st.info("If you don't know how to get Storefront EID, you can use Storefront in workspace report.")

st.subheader("Date Range 📅")
st.markdown("Pick your start and end dates. Common sense applies: the end date should come after the start date.")
st.warning(
    """
    **PAY ATTENTION, THESE ARE THE LAWS OF THE LAND:**
    - If you select **1 or 2 storefronts**, you get a maximum date range of **60 days**.
    - If you select **3 to 5 storefronts**, your maximum date range is reduced to **30 days**.
    
    *Why the limits? Because every query you run is a tiny burden on our servers. Too much burden, and the whole thing goes up in smoke. Irvine really, really doesn't want to fix that on a weekend.*
    """
)
st.divider()

# --- Mục 2: Bộ lọc bổ sung ---
st.header("2. Special Ops: Additional Filters")
st.markdown("When you select the **Keyword Performance** report from the sidebar, you unlock a new set of shiny filters. Use their power wisely.")

st.info(
    """
    These filters are currently available **ONLY** for the Keyword Performance report.
    - **Device Type:** Filter by Mobile, Desktop, etc.
    - **Display Type:** Filter by how the product was displayed (e.g., Organic, Ad).
    - **Product Position:** Filter by the product's rank on the page.
    """
)
st.error(
    """
    **IMPORTANT LIMITATION (FOR NOW):**
    
    For these filters, you can select the **NONE** option from each dropdown list to select all options inside the dropdown list.
    
    Currently, multi-select is not supported. Irvine won't do it unless he's forced to.
    """
)
st.divider()


# --- Mục 3: Quy trình ---
st.header("3. The Four Steps to Data Glory")
st.markdown("Follow these steps in order. It's like a recipe for a cake, but instead of cake, you get a beautiful CSV file. Which is... almost as good.")

st.markdown("#### **Step 1: Preview the Goods**")
st.markdown("Once your filters are set, hit the **'Preview Data'** button. This is your safety net. It fetches the first 500 rows and shows them to you. It's your 'look before you leap' moment to ensure the data doesn't look cursed or completely wrong.")

st.markdown("#### **Step 2: Read the Summary**")
st.markdown("After the preview, a summary box will appear. It gives you the vital stats: an *estimate* of the total rows you're about to unleash, the query time, etc. Read it. If it says 'Estimated Rows: 2 million,' you've done something very wrong.")

st.markdown("#### **Step 3: Unleash the Beast (Export)**")
st.markdown("If the preview looks good and the summary doesn't give you a heart attack, it's time for the main event. Smash that **'Export Full Data'** button. Depending on the size of your request, this could be instant or it might take a minute. Go stretch your legs. Hydrate.")

st.markdown("#### **Step 4: Secure the Bag (Download)**")
st.markdown("When the export is complete, the glorious **'Download CSV Now'** button will appear. Click it. The data is yours. You've done it. You're a data champion.")
st.divider()


# --- Mục 4: Ghi chú quan trọng ---
st.header("4. The Fine Print (Don't Skip This, We're Serious) 💀")

st.error(
    """
    **THE HARD LIMIT: 50,000 ROWS!**
    
    If your query is estimated to have more than 50,000 rows, the export button will be disabled. **The system will block you.** This is not a negotiation.
    
    **Solution:** Don't panic. Just go back and narrow your date range or reduce the number of storefronts. It's an easy fix.
    """
)

st.markdown("### Need a Do-Over?")
st.markdown("Messed up? Feeling lost? Want to start fresh? The **'Start New Export'** button is your best friend. It's the 'Ctrl+Alt+Delete' for this app. It wipes the slate clean so you can try again.")

st.markdown("### Technical Support? 🛠️")
st.markdown(
    """
    Okay, let's have a real talk. Before you even *think* about sending a message for help:
    1.  Have you tried turning it off and on again? (i.e., hitting the **'Start New Export'** button).
    2.  Have you re-read this sacred text from top to bottom?
    3.  Have you calmly asked a coworker if you're missing something obvious?
    4.  Have you taken a deep breath, counted to ten, and tried one more time?

    If the app is *truly* on fire, spitting out nonsense, and you've exhausted all other options... then, and only then, you may **ping IrvineCao**. He built this, so he can fix it. But let's all agree to make that the absolute last resort to preserve his sanity.
    """
)

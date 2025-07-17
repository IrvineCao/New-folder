import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="The Unofficial Rulebook",
    page_icon="📜",
    layout="wide"
)

# --- Custom CSS for consistent vibes ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    body {
        font-family: 'Inter', sans-serif;
    }

    /* Make headers pop */
    h1, h2, h3 {
        font-weight: 700;
    }
    
    h1 {
        color: #ff4b1f; /* Orange color for main title */
    }

    /* Style for the info boxes */
    .st-emotion-cache-1wivapv {
        background-color: rgba(255, 75, 31, 0.1); /* Light orange background */
        border-left-color: #ff4b1f; /* Orange left border */
    }
</style>
""", unsafe_allow_html=True)


# --- Page Content ---

st.title("The Unofficial Rulebook 📜")
st.markdown("*(Welcome to the tutorial level. Yes, you have to play it.)*")

st.markdown("This tool was forged in the fires of repetitive tasks and fueled by Irvine's desperate need for peace and quiet. It exists so you can get the data you need, whenever you need it, without sending that dreaded 'Can you help me export something on EO but its not letting me do it?' message. The absolute least you can do is read this guide. Don't be *that* person.")
st.divider()


# --- Section 1: Filters ---
st.header("1. The Holy Trinity of Filters")
st.markdown("This is the most crucial part. It's where you tell the machine what you want. Garbage in, garbage out. Don't give us garbage.")

st.subheader("Workspace ID 💼")
st.markdown("This is the big one, the master key to your data kingdom. You should know this number. If you don't, you probably shouldn't be here. Just saying.")

st.subheader("Storefront EID 🏬")
st.markdown("Enter one or more Storefront EIDs, separated by commas. **CRITICAL RULE:** They must all belong to the same Workspace you entered above. Don't try to mix and match data from different universes. This tool is smart, but it's not a dimension-hopping wizard.")
st.warning("You can query a **MAXIMUM of 5 storefronts** at a time. We know you're ambitious, but let's not get greedy and crash the server.")

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

# --- Section 2: Additional Filters ---
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
    
    For these new filters, you can only select **ONE** option from each dropdown at a time.
    
    Yes, we know you want to select multiple options. That feature is on the roadmap. But the roadmap is long, and Irvine is but one man. Patience, young grasshopper. Multi-select will come... eventually.
    """
)
st.divider()


# --- Section 3: The Workflow ---
st.header("3. The Four Steps to Data Glory")
st.markdown("Follow these steps in order. It's like a recipe for a cake, but instead of cake, you get a beautiful CSV file. Which is... almost as good.")

st.markdown("#### **Step 1: Preview the Goods**")
st.markdown("Once your filters are set, hit the **'Preview Data'** button. This is your safety net. It fetches the first 500 rows and shows them to you. It's your 'look before you leap' moment to ensure the data doesn't look cursed or completely wrong.")

st.markdown("#### **Step 2: Read the Summary**")
st.markdown("After the preview, a summary box will appear. It gives you the vital stats: an *estimate* of the total rows you're about to unleash, the query time, etc. Read it. If it says 'Estimated Rows: 2 million,' you've done something very wrong.")

st.markdown("#### **Step 3: Unleash the Beast (Export)**")
st.markdown("If the preview looks good and the summary doesn't give you a heart attack, it's time for the main event. Smash that **'Export Full Data'** button. Depending on the size of your request, this could be instant or it might take a minute. Go stretch your legs. Hydrate.")

st.markdown("#### **Step 4: Secure the Bag (Download)**")
st.markdown(
    "When the export is complete, the glorious **'Download CSV Now'** button will appear. Click it. The data is yours. You've done it. You're a data champion."
)
st.image("download.jpg")
st.divider()


# --- Section 4: The Fine Print ---
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

    If the app is *truly* on fire, spitting out nonsense, and you've exhausted all other options... then, and only then, you may **ping IrvineCao**. He built this, so he can fix it (Maybe).
    """
)
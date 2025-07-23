import streamlit as st

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Your Data Export Survival Guide",
    page_icon="📚",
    layout="wide"
)

# --- CSS tùy chỉnh ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    body {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }

    .st-emotion-cache-18ni7ap, .st-emotion-cache-h4xjwg {
        display: none;
    }

    .main-title {
        font-size: 4.0rem;
        font-weight: 900;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #ff007f, #00ffcc);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.2em 0;
    }

    .sub-header {
        text-align: center;
        font-size: 1.15rem;
        color: #a1a1aa;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
    }
    
    h2, h3 {
        font-weight: 700;
        color: #ffffff;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, rgba(255, 0, 127, 0.1), rgba(0, 255, 204, 0.1));
        border-left: 4px solid #00ffcc;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(255, 177, 43, 0.1));
        border-left: 4px solid #ff6b6b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .tip-box {
        background: linear-gradient(135deg, rgba(81, 207, 102, 0.1), rgba(34, 197, 94, 0.1));
        border-left: 4px solid #51cf66;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 class='main-title'>Your Data Export Survival Guide</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='sub-header'>
    🎉 Congratulations! You've discovered the holy grail of data exports. No more begging, no more waiting, no more sad DMs to Irvine. 
    <br><br>
    This guide will turn you from a data export newbie into a certified export ninja in just 5 minutes. Ready? Let's dive in! 🚀
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# --- Quick Start ---
st.header("🚀 Quick Start (For the Impatient)")
st.markdown(
    """
    <div class='highlight-box'>
    <h3>🏃‍♂️ TL;DR Version:</h3>
    1. Pick a report from the sidebar<br>
    2. Fill in Workspace ID + Storefront EID<br>  
    3. Choose your dates<br>
    4. Click "Get Data" → Wait → Click "Export Full Data" → Download CSV<br>
    5. Profit! 💰
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# --- The Golden Rules ---
st.header("🏆 The Golden Rules (Break These at Your Own Risk)")

st.subheader("👑 Rule #1: Know Your Numbers")
st.markdown(
    """
    <div class='tip-box'>
    <strong>Workspace ID</strong> 🏢: This is your passport to the data kingdom. You should know this number by heart. If you don't, ask your team lead or check your existing reports.
    <br><br>
    <strong>Storefront EID</strong> 🏬: These are your shop IDs. You can enter multiple ones (separated by commas), but they MUST belong to the same workspace. Don't try to mix and match from different universes! 
    <br><br>
    <strong>Pro Tip:</strong> Use the "Storefront in Workspace" report first to get a list of all available storefronts in your workspace. It's like a phone book, but for shops! 📞
    </div>
    """, 
    unsafe_allow_html=True
)

st.subheader("⏰ Rule #2: The Date Range Commandments")
st.markdown(
    """
    <div class='warning-box'>
    <h4>🚨 ATTENTION: These limits are non-negotiable!</h4>
    
    <strong>1-2 storefronts:</strong> Maximum 60 days<br>
    <strong>3-5 storefronts:</strong> Maximum 30 days<br>
    <strong>More than 5:</strong> You're pushing it, buddy. Keep it under 30 days or the system will give you the cold shoulder. ❄️
    <br><br>
    <strong>Why these limits?</strong> Because every query is a tiny burden on our servers. Too much burden = system goes boom 💥. And nobody wants to explain to the team why the data export tool caught fire on a Friday afternoon.
    </div>
    """, 
    unsafe_allow_html=True
)

st.subheader("🛡️ Rule #3: The 50,000 Row Law")
st.markdown(
    """
    <div class='warning-box'>
    <h4>⚖️ This is THE LAW, not a suggestion!</h4>
    
    If your query tries to export more than <strong>50,000 rows</strong>, the system will block you faster than a bouncer at an exclusive club. 🚫
    <br><br>
    <strong>What to do if you hit the limit:</strong><br>
    • Reduce your date range (most effective)<br>
    • Select fewer storefronts<br>
    • Use optional filters to narrow down results<br>
    • Sacrifice a coffee to the data gods ☕<br>
    <br>
    <strong>Why 50k?</strong> It's the perfect balance between "useful data" and "not crashing the server." Trust us on this one.
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# --- Advanced Features ---
st.header("🎛️ Advanced Features (For the Power Users)")

st.subheader("🔍 Optional Filters (The Secret Sauce)")
st.markdown(
    """
    <div class='highlight-box'>
    Some reports (like <strong>Keyword Performance</strong>) come with special filters:
    <br><br>
    <strong>Device Type:</strong> Mobile, Desktop, or None (for all devices)<br>
    <strong>Display Type:</strong> Paid, Organic, Top, or None (for all types)<br>
    <strong>Product Position:</strong> Specific ranking positions or None (for all positions)<br>
    <br>
    <strong>Current Limitation:</strong> You can only select one option per filter (no multi-select yet). But hey, selecting "None" gives you everything! 🎯
    </div>
    """, 
    unsafe_allow_html=True
)

st.subheader("👀 The Preview Feature (Your Safety Net)")
st.markdown(
    """
    <div class='tip-box'>
    Always, ALWAYS check the preview before exporting! It shows you:
    <br><br>
    ✅ First 500 rows of your data<br>
    ✅ Total estimated rows<br>
    ✅ Number of columns<br>
    ✅ Query execution time<br>
    <br>
    Think of it as a "look before you leap" moment. If the preview looks weird, your full export probably will too. Trust your gut! 🤔
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# --- The Export Process ---
st.header("🎯 The Export Process (Step by Step)")

st.markdown("### Step 1: Fill the Form Like a Pro")
st.markdown("""
- **Required fields** have a red asterisk (*) - these are mandatory, no exceptions
- **Optional fields** are nice-to-haves - use them to filter your data further
- **Red error messages** mean you messed up somewhere - fix them before proceeding
""")

st.markdown("### Step 2: Preview Your Masterpiece")
st.markdown("""
Click "🚀 Get Data" and watch the magic happen:
- If you see green success messages, you're golden ✅
- If you see red error messages, read them carefully and fix the issues ❌
- The summary box tells you everything about your data - read it!
""")

st.markdown("### Step 3: Export Like a Boss")
st.markdown("""
If the preview looks good:
- Click "🚀 Export Full Data" 
- Wait patiently (grab a coffee ☕)
- Click "📥 Download CSV Now" when it appears
- Celebrate your victory! 🎉
""")

st.divider()

# --- Troubleshooting ---
st.header("🔧 Troubleshooting (When Things Go Wrong)")

st.subheader("😱 Common Problems & Solutions")

with st.expander("❌ \"No data found for the selected criteria\"", expanded=False):
    st.markdown("""
    **What it means:** Your filters are too restrictive, or the data doesn't exist.
    
    **Solutions:**
    - Expand your date range
    - Remove optional filters  
    - Double-check your Workspace ID and Storefront EIDs
    - Try a different time period when you know data exists
    """)

with st.expander("🚫 \"Data is too large to export (X rows)\"", expanded=False):
    st.markdown("""
    **What it means:** You hit the 50,000 row limit. The system is protecting itself (and you).
    
    **Solutions (in order of effectiveness):**
    1. **Reduce date range** - Most effective way to cut down rows
    2. **Select fewer storefronts** - Each storefront multiplies your data
    3. **Add optional filters** - Device type, display type, etc.
    4. **Split into multiple exports** - Export different time periods separately
    """)

with st.expander("⚡ \"Database Connection Error\"", expanded=False):
    st.markdown("""
    **What it means:** The database is having a bad day.
    
    **Solutions:**
    - Wait 30 seconds and try again
    - If it persists, ping the tech team
    - Check if other people are having the same issue
    - As a last resort, sacrifice a rubber duck to the database gods 🦆
    """)

with st.expander("🐛 \"An unexpected error occurred\"", expanded=False):
    st.markdown("""
    **What it means:** Something weird happened that we didn't anticipate.
    
    **Solutions:**
    - Click "🔄 Start New Export" to reset everything
    - Try again with different parameters
    - If it keeps happening, screenshot the error and ping the tech team
    - Don't panic - your data is safe!
    """)

st.divider()

# --- Pro Tips ---
st.header("💡 Pro Tips (From the Data Export Veterans)")

st.markdown(
    """
    <div class='tip-box'>
    <h4>🎯 Efficiency Hacks:</h4>
    
    <strong>1. Start Small:</strong> Test with 1 storefront and 7 days first, then scale up<br>
    <strong>2. Use Presets:</strong> "Last 30 days" is usually what you want<br>
    <strong>3. Check the Summary:</strong> If it says 45k rows, you're cutting it close!<br>
    <strong>4. Name Your Downloads:</strong> The CSV comes with a date, but rename it something meaningful<br>
    <strong>5. Preview is Free:</strong> Use it liberally - it doesn't count against any limits<br>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='highlight-box'>
    <h4>🚀 Advanced User Tricks:</h4>
    
    <strong>Radio Buttons vs Tabs:</strong> We use radio buttons instead of traditional tabs because they're more stable. Don't worry, you'll get used to it!<br><br>
    <strong>Session Memory:</strong> The tool remembers your inputs as you navigate between reports. Convenient!<br><br>
    <strong>Multiple Exports:</strong> You can run multiple exports by opening new browser tabs. Each tab is independent.<br><br>
    <strong>CSV Formatting:</strong> Files are UTF-8 encoded and Excel-ready. No weird character issues!<br>
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# --- Available Reports ---
st.header("📊 Available Reports (Your Arsenal)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🛍️ **Storefront in Workspace**
    *Your phonebook for storefronts*
    - Lists all storefronts in a workspace
    - Use this first to get your Storefront EIDs
    - Super fast, no date range needed
    
    ### 🔬 **Keyword Lab** 
    *The keyword goldmine*
    - Keyword discovery data
    - Search volumes, performance metrics
    - GMV, cost, clicks, impressions
    
    ### 📈 **Keyword Performance**
    *Advanced keyword analytics*
    - Detailed performance breakdowns
    - Device, display, position filters
    - Share of search, conversion rates
    """)

with col2:
    st.markdown("""
    ### 📦 **Product Tracking**
    *Your product monitoring dashboard*
    - Product positioning data
    - Sales performance tracking
    - Brand and product insights
    
    ### 🏟️ **Competition Landscape**
    *Know your enemies*
    - Competitor analysis data
    - Market share insights
    - Positioning comparisons
    
    ### 🎯 **Storefront Optimization**
    *Performance optimization data*
    - GMV, ROAS, CPC metrics
    - Cost analysis
    - ROI calculations
    """)

st.divider()

# --- Support ---
st.header("🆘 Need Help? (The Last Resort Protocol)")

st.markdown(
    """
    <div class='warning-box'>
    <h4>🚨 Before you ask for help, have you tried:</h4>
    
    1. ✅ Reading this guide from top to bottom?<br>
    2. ✅ Clicking the "🔄 Start New Export" button?<br>
    3. ✅ Waiting 30 seconds and trying again?<br>
    4. ✅ Asking a colleague if they've seen this issue?<br>
    5. ✅ Taking a deep breath and counting to ten?<br>
    <br>
    <strong>If you answered YES to all of the above,</strong> then and only then, you may ping <strong>IrvineCao</strong> for help. 
    <br><br>
    Please include:<br>
    • What you were trying to do<br>
    • What error message you got (screenshot preferred)<br>
    • Your workspace ID and date range<br>
    • A sincere apology for bothering Irvine 😄<br>
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# --- Fun Closing ---
st.header("🎉 Congratulations!")

st.markdown(
    """
    <div class='highlight-box'>
    <h3>🏆 You are now a certified Data Export Ninja!</h3>
    
    You have the power to:
    <br>
    ✨ Export data faster than Irvine can say "SQL"<br>
    ✨ Navigate filters like a pro<br>
    ✨ Troubleshoot issues without breaking a sweat<br>
    ✨ Impress your colleagues with your data export prowess<br>
    <br>
    <strong>Remember:</strong> With great power comes great responsibility. Use this tool wisely, and may your CSVs be ever formatted correctly! 📊✨
    </div>
    """, 
    unsafe_allow_html=True
)

st.balloons()

# --- Easter Egg ---
if st.button("🎁 Click for a surprise!", help="What could this button do? 🤔"):
    st.success("🎉 Congratulations! You found the easter egg! You're officially a power user now!")
    st.markdown("**Fun fact:** This data export tool was built in exactly 2 weeks, powered by coffee ☕ and the desperate need to stop pinging Irvine for data exports. 😄")
    st.image("https://media.giphy.com/media/3oriNYQX2lC6dfW2Ji/giphy.gif", width=300)
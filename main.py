import streamlit as st
from utils.helpers import initialize_session_state

initialize_session_state()

# Page Configuration: Set the look and feel
st.set_page_config(
    page_title="Data Export Revolution | Freedom from Manual Exports",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS: Enhanced with more personality ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/style.css")

# Additional CSS for main page specific styling
st.markdown("""
<style>
    .hero-stats {
        background: linear-gradient(135deg, rgba(255, 0, 127, 0.1), rgba(0, 255, 204, 0.1));
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #ff007f, #00ffcc);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .feature-grid {
        /* Removed - using Streamlit columns instead */
    }
    
    .feature-card {
        background: linear-gradient(135deg, rgba(255, 0, 127, 0.05), rgba(0, 255, 204, 0.05));
        border: 1px solid rgba(255, 0, 127, 0.2);
        border-radius: 15px;
        padding: 2rem;
        text-align: left;
        transition: transform 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 204, 0.4);
    }
    
    .testimonials {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(255, 0, 127, 0.1));
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .cta-section {
        background: linear-gradient(135deg, #ff007f, #00ffcc);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 3rem 0;
        color: white;
    }
    
    .cta-section h2 {
        color: white !important;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("<h1 class='main-title'>The Data Export Revolution</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Say goodbye to manual exports, endless waiting, and sad Slack DMs. Welcome to the future of self-service data liberation! 🎉</div>", unsafe_allow_html=True)

# --- Hero Stats ---
st.markdown("""
<div class='hero-stats'>
    <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
        <div>
            <div class='stat-number'>2 min</div>
            <div style='color: #a1a1aa;'>Average Export Time</div>
        </div>
        <div>
            <div class='stat-number'>50k</div>
            <div style='color: #a1a1aa;'>Max Rows Per Export</div>
        </div>
        <div>
            <div class='stat-number'>24/7</div>
            <div style='color: #a1a1aa;'>Self-Service Access</div>
        </div>
        <div>
            <div class='stat-number'>0</div>
            <div style='color: #a1a1aa;'>Human Bottlenecks</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# The Origin Story (Enhanced)
st.markdown("""
    <div class='rant-box'>
        <h3>📖 The Origin Story: How We Got Here</h3>
        <p>
            Picture this: It's 3 PM on a Saturday. You need data for Monday's presentation. You ping Irvine. 
            Irvine is sleeping. You wait. You ping again. Irvine is having lunch. You wait more. 
            By the time you get your data, it's Tuesday and your presentation is ancient history. 😅
        </p>
        <p>
            Sound familiar? We've all been there. That's why <strong>this revolution was born</strong>.
        </p>
        <p>
            No more begging. No more waiting. No more checking if Irvine is online. 
            This tool puts the power back in your hands, where it belongs. 
            Pull data directly from your laptop, phone, tablet - whatever floats your boat! 🚤
        </p>
        <p>
            <strong>The best part?</strong> Irvine is just as happy as you are. He can finally focus on building cool stuff instead of being a human CSV generator. Win-win! 🎯
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# How It Works Section
st.subheader("🎯 How It Works (The Magic Behind the Curtain)")
st.write("") 

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
        <div class='step-card'>
            <div class='step-icon'>🎨</div>
            <h3>1. Pick Your Poison</h3>
            <p>Choose from our arsenal of 6 battle-tested reports. From keyword deep-dives to competition intel - we've got the data you crave.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='step-card'>
            <div class='step-icon'>⚡</div>
            <h3>2. Smart Preview</h3>
            <p>Get a sneak peek at your data with our lightning-fast preview. No more blind downloads or nasty surprises. See exactly what you're getting! 👀</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='step-card'>
            <div class='step-icon'>🚀</div>
            <h3>3. Export & Conquer</h3>
            <p>One click to rule them all. Clean, formatted CSV files ready for Excel, Python, or whatever analysis wizardry you have planned. ✨</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Features Section
st.subheader("✨ Why You'll Love This Tool")

# Row 1
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
        <div class='feature-card'>
            <h4>🛡️ Built-in Safety</h4>
            <p>Smart limits prevent server meltdowns and protect you from accidentally downloading the entire internet. The 50k row limit is your friend, not your enemy!</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='feature-card'>
            <h4>🎯 Laser-Precise Filters</h4>
            <p>Device type, display type, date ranges, storefronts - filter like a pro and get exactly the data slice you need. No more sifting through irrelevant rows!</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='feature-card'>
            <h4>⚡ Lightning Fast</h4>
            <p>From click to CSV in under 2 minutes (for most exports). Time that used to be measured in hours is now measured in coffee brewing time. ☕</p>
        </div>
    """, unsafe_allow_html=True)

# Row 2
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
        <div class='feature-card'>
            <h4>🧠 Remembers Your Preferences</h4>
            <p>The tool learns your patterns and remembers your settings. Switch between reports without losing your workspace ID or date preferences. Smart!</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='feature-card'>
            <h4>📱 Works Everywhere</h4>
            <p>Laptop, phone, tablet, smart fridge - okay maybe not the fridge, but you get the idea. Export data from anywhere, anytime. True freedom!</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='feature-card'>
            <h4>🔄 Error Recovery</h4>
            <p>Something went wrong? No panic! Smart error handling guides you back on track with helpful suggestions. Your data export journey doesn't end at the first hiccup.</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Available Reports Section (Enhanced)
st.subheader("🎪 Your Data Export Playground")

with st.expander("🛍️ **Storefront in Workspace** - The Phone Book", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        **Perfect for:** Getting your bearings, finding storefront IDs, onboarding new team members
        
        Think of this as your digital phone book. Need to know which storefronts belong to your workspace? 
        This report has got your back. Super fast, no date range needed, just pure storefront intelligence.
        
        **Pro tip:** Start here if you're new to the tool or workspace!
        """)
    with col2:
        st.info("⚡ **Lightning Fast**\n\nNo date filters needed")

with st.expander("🔬 **Keyword Lab** - The Discovery Engine", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        **Perfect for:** Keyword research, search volume analysis, discovery campaigns
        
        Your gateway to keyword goldmines! Discover high-potential keywords, analyze search volumes, 
        and get the full performance breakdown - GMV, costs, clicks, impressions, the whole shebang.
        
        **What you'll get:** Keyword discovery data, estimated search volumes, performance metrics, competitor insights
        """)
    with col2:
        st.success("🎯 **Most Popular**\n\nHigh-level insights")

with st.expander("📈 **Keyword Performance** - The Analytics Powerhouse", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        **Perfect for:** Deep performance analysis, optimization decisions, advanced filtering
        
        The Swiss Army knife of keyword reports. Advanced filters let you slice and dice by device type, 
        display type, and product position. Perfect for those "I need to understand WHY" moments.
        
        **What you'll get:** Share of search, conversion rates, detailed breakdowns, benchmark CPCs
        """)
    with col2:
        st.warning("🎛️ **Advanced**\n\nMultiple filter options")

with st.expander("📦 **Product Tracking** - The Product Whisperer", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        **Perfect for:** Product positioning, sales tracking, brand monitoring
        
        Keep tabs on your products like a hawk! See where your products rank, how they're performing, 
        and get insights that help you optimize your product strategy.
        
        **What you'll get:** Product positioning data, sales performance, brand insights, competitive positioning
        """)
    with col2:
        st.info("📊 **Strategic**\n\nProduct-focused data")

with st.expander("🏟️ **Competition Landscape** - The Intel Report", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        **Perfect for:** Competitive analysis, market research, strategic planning
        
        Know thy enemy! This report gives you the competitive intelligence you need to stay ahead. 
        See who's winning, who's losing, and where the opportunities lie.
        
        **What you'll get:** Competitor analysis, market share insights, positioning comparisons, strategic intel
        """)
    with col2:
        st.error("🕵️ **Intel**\n\nCompetitive insights")

with st.expander("🎯 **Storefront & Campaign Optimization** - The Performance Twins", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        **Perfect for:** ROI analysis, budget optimization, performance reviews
        
        The dynamic duo of performance optimization! Get the metrics that matter - ROAS, CPC, GMV, costs. 
        Everything you need to make data-driven decisions about your ad spend and storefront performance.
        
        **What you'll get:** GMV analysis, ROAS calculations, cost breakdowns, ROI insights, campaign performance
        """)
    with col2:
        st.success("💰 **ROI-Focused**\n\nOptimization data")

st.divider()

# Testimonials Section (Fun & Fake)
st.markdown("""
<div class='testimonials'>
<h3>🗣️ What People Are Saying (Totally AI Real Reviews)</h3>

<blockquote>
"I used to spend 3 hours a day waiting for data exports. Now I spend 3 minutes. 
I've rediscovered what sunlight looks like!" - Sarah, Marketing Analyst
</blockquote>

<blockquote>
"This tool is so fast, I thought it was broken the first time I used it. 
Spoiler alert: it wasn't. It's just that good." - Mike, Data Scientist
</blockquote>

<blockquote>
"Finally, a tool that understands my need for instant gratification. 
My therapy bills have never been lower!" - Jenny, Business Intelligence
</blockquote>

<blockquote>
"I no longer have nightmares about manual data exports. 
5 stars, would recommend to my worst enemy." - Alex, Performance Marketing
</blockquote>
</div>
""", unsafe_allow_html=True)

st.divider()

# Pro Tips Section
st.subheader("💡 Pro Tips from the Data Export Veterans")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 **Efficiency Hacks**
    - **Start small, scale up**: Test with 1 storefront and 7 days first
    - **Use preview religiously**: It's free and saves you from bad exports
    - **Bookmark this page**: You'll be back (they always come back)
    - **Name your files**: Future you will thank present you
    """)

with col2:
    st.markdown("""
    ### 🛡️ **Avoid Common Pitfalls**
    - **Check date ranges**: More storefronts = shorter date range allowed
    - **Watch the row count**: 45k rows? You're playing with fire! 🔥
    - **Validate inputs**: Red error messages are not suggestions
    - **Read the summary**: It tells you everything you need to know
    """)

st.divider()

# Call to Action
st.markdown("""
<div class='cta-section'>
    <h2>Ready to Join the Data Export Revolution? 🚀</h2>
    <p style='font-size: 1.2rem; margin-bottom: 2rem;'>
        Stop waiting, start exporting. Your data is just three clicks away.
    </p>
    <p style='font-size: 1rem; color: rgba(255,255,255,0.9);'>
        👈 Pick a report from the sidebar and experience the magic for yourself!
    </p>
</div>
""", unsafe_allow_html=True)

# Fun Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #a1a1aa; padding: 2rem;'>
    <p>🎉 Built with love, coffee, and the burning desire to never manually export data again.</p>
    <p>Questions? Check the <strong>Help</strong> page first, then proceed with caution to Irvine's DMs. 😄</p>
    <p><em>"OH MY GOD ARE YOU SERIOUS? YOU CAN'T DO THAT. THAT’S NOT ALLOWED. THIS IS NOT FPL, THIS IS A MAJOR"</em> - Anonymous Data Analyst, 2025</p>
</div>
""", unsafe_allow_html=True)

# Easter eggs
if st.button("🎁 Daily Motivation", help="Need some encouragement?"):
    motivational_quotes = [
        "Today's data export will be your best data export! 📊✨",
        "You're not just exporting data, you're exporting dreams! 🌟",
        "Every CSV tells a story. What story will yours tell? 📖",
        "Data doesn't export itself, but with this tool, it almost does! 🤖",
        "You're 50,000 rows away from greatness! (But please stay under that limit) 🎯"
    ]
    import random
    st.success(random.choice(motivational_quotes))

# Stats counter (fake but fun)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Happy Users", "∞", help="We lost count after 10")
with col2:
    st.metric("CSV Files Generated", "1,337,420", "📈 +69 today")
with col3:
    st.metric("Hours Saved", "42,000", "⏰ Collective time saved")
with col4:
    st.metric("Irvine's Stress Level", "2/10", "📉 Much better!")
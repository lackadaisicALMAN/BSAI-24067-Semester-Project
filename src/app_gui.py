import streamlit as st
import time
from datetime import datetime

# ==========================================
# 1. CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="AgriYield - Remote Manager",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match your CustomTkinter Dark/Green Theme
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #1a1a1a;
        color: white;
    }
    
    /* Card Styles mimicking CTK Frames with colored borders */
    .card-red {
        background-color: #2B2B2B;
        border: 2px solid #ff4b4b; /* Red */
        border-radius: 6px;
        padding: 20px;
        text-align: center;
    }
    .card-green {
        background-color: #2B2B2B;
        border: 2px solid #0df05e; /* Green */
        border-radius: 6px;
        padding: 20px;
        text-align: center;
    }
    
    /* Text Styles */
    .card-title { font-size: 14px; font-weight: bold; color: #e0e0e0; margin-bottom: 5px; }
    .card-value { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
    .card-sub { font-size: 12px; color: gray; }
    .val-red { color: #ff4b4b; }
    .val-green { color: #0df05e; }

    /* Sidebar Status */
    .status-text { color: gray; font-size: 12px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE (Memory)
# ==========================================
# This holds the "Console Logs" so they persist when you click buttons
if 'logs' not in st.session_state:
    st.session_state.logs = [
        f"[{datetime.now().strftime('%H:%M:%S')}] [SYSTEM] Connected to EC2 Instance...",
        f"[{datetime.now().strftime('%H:%M:%S')}] [SYSTEM] B-Tree Index Loaded.",
        f"[{datetime.now().strftime('%H:%M:%S')}] [INFO] 4 Batches found in storage."
    ]

if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def add_log(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    st.session_state.logs.append(f"[{timestamp}] {message}")

def handle_new_batch():
    # Simulate the upload process from your code
    farmer = st.session_state.temp_farmer_name
    if farmer:
        add_log(f"[UPLOAD] Sending Batch for '{farmer}' to AWS Server...")
        time.sleep(0.5) # Simulate latency
        add_log(f"[SUCCESS] Saved to B-Tree ID: {124 + len(st.session_state.logs)}")
        st.session_state.temp_farmer_name = "" # Clear input
        st.toast("✅ Batch Uploaded to Cloud")

# ==========================================
# 4. SIDEBAR (Navigation)
# ==========================================
with st.sidebar:
    st.markdown("## AgriYield\n### Cloud")
    st.markdown("---")
    
    # Navigation Buttons
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
    
    if st.button("➕ New Batch", use_container_width=True):
        st.session_state.page = "Entry"

    # Status Label (Simulated connection)
    st.markdown("""
        <div style='margin-top: 200px; color: gray; font-size: 12px;'>
            Status: 🟢 Connected<br>
            AWS: 13.60.211.128
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. MAIN CONTENT
# ==========================================

# HEADER
st.title("Real-Time Factory Overview")
st.markdown("<br>", unsafe_allow_html=True)

# METRICS CARDS (Custom HTML to match your specific borders)
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card-red">
        <div class="card-title">Drying Queue</div>
        <div class="card-value val-red">Batch #101 (24.5%)</div>
        <div class="card-sub">High Priority</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card-green">
        <div class="card-title">Ready to Process</div>
        <div class="card-value val-green">Batch #123 (20.0%)</div>
        <div class="card-sub">Optimized</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# ENTRY POPUP LOGIC
# If "New Batch" was clicked, we show the input form right here above the logs
if st.session_state.page == "Entry":
    with st.container():
        st.subheader("New Batch Entry")
        c1, c2 = st.columns([3, 1])
        with c1:
            st.text_input("Enter Farmer Name:", key="temp_farmer_name", placeholder="e.g. John Doe")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("Submit to AWS", on_click=handle_new_batch, type="primary")

# CONSOLE LOG (Simulated Backend Output)
st.subheader("Server Logs (AWS Stream)")

# Join all logs into a single string
log_text = "\n".join(st.session_state.logs)

# Display as a code block to look like a terminal
st.text_area("Console Output", value=log_text, height=300, disabled=True)
import streamlit as st
import time
import requests
from datetime import datetime


AWS_IP = "13.60.211.128" 
AWS_PORT = "5000"  # This matches the setup.sh script I gave you
AWS_URL = f"http://{AWS_IP}:{AWS_PORT}/upload_batch"

st.set_page_config(
    page_title="AgriYield - Remote Manager",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for that "Dark/Green" CustomTkinter look
st.markdown("""
<style>
    .stApp { background-color: #1a1a1a; color: white; }
    .card-red {
        background-color: #2B2B2B; border: 2px solid #ff4b4b;
        border-radius: 6px; padding: 20px; text-align: center;
    }
    .card-green {
        background-color: #2B2B2B; border: 2px solid #0df05e;
        border-radius: 6px; padding: 20px; text-align: center;
    }
    .card-title { font-size: 14px; font-weight: bold; color: #e0e0e0; margin-bottom: 5px; }
    .card-value { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
    .card-sub { font-size: 12px; color: gray; }
    .val-red { color: #ff4b4b; }
    .val-green { color: #0df05e; }
</style>
""", unsafe_allow_html=True)

if 'logs' not in st.session_state:
    st.session_state.logs = [
        f"[{datetime.now().strftime('%H:%M:%S')}] [SYSTEM] GUI Initialized.",
        f"[{datetime.now().strftime('%H:%M:%S')}] [NET] Target AWS IP: {AWS_IP}"
    ]

if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"


def add_log(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    st.session_state.logs.append(f"[{timestamp}] {message}")

def handle_new_batch():
    # 1. Gather Data from Session State (Form)
    payload = {
        "farmer": st.session_state.get("in_farmer"),
        "variety": st.session_state.get("in_variety"),
        "weight": st.session_state.get("in_weight"),
        "moisture": st.session_state.get("in_moisture"),
        "timestamp": datetime.now().isoformat()
    }

    if payload["farmer"]:
        add_log(f"[UPLOAD] Sending {payload['weight']}kg ({payload['variety']}) to AWS...")
        
        try:
            # 2. REAL NETWORK REQUEST TO AWS
            # This sends the data to your EC2 instance!
            response = requests.post(AWS_URL, json=payload, timeout=3)
            
            if response.status_code == 200:
                data = response.json()
                add_log(f"[AWS-EC2] Response 200 OK.")
                add_log(f"[SUCCESS] Saved to Remote DB ID: {data.get('new_id')}")
                st.toast("✅ Synced with AWS Server!")
            else:
                add_log(f"[ERROR] AWS Server returned code: {response.status_code}")
                st.error("Server Error")
                
        except requests.exceptions.ConnectionError:
            add_log("[ERROR] Connection Failed! Is the AWS Flask script running?")
            add_log(f"[TIP] Check http://{AWS_IP}:{AWS_PORT} in your browser.")
            st.error("Cannot connect to AWS EC2.")
        except Exception as e:
            add_log(f"[ERROR] {str(e)}")

        # Clear input field (optional)
        st.session_state.temp_farmer_name = "" 


with st.sidebar:
    st.markdown("## AgriYield\n### Cloud")
    st.markdown("---")
    
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
    
    if st.button("➕ New Batch", use_container_width=True):
        st.session_state.page = "Entry"

    st.markdown(f"""
        <div style='margin-top: 200px; color: gray; font-size: 12px;'>
            Status: 🟢 Linking to AWS<br>
            Target: {AWS_IP}
        </div>
    """, unsafe_allow_html=True)


st.title("Real-Time Factory Overview")
st.markdown("<br>", unsafe_allow_html=True)

# METRICS CARDS
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

# === ENTRY FORM PAGE ===
if st.session_state.page == "Entry":
    with st.container():
        st.subheader("📝 New Batch Entry")
        
        # This Form collects the data
        with st.form("aws_entry_form"):
            c1, c2 = st.columns([1, 1])
            
            with c1:
                st.text_input("Farmer Name", key="in_farmer", placeholder="e.g. Ali Khan")
                st.selectbox("Rice Variety", ["Super Basmati", "Kainat 1121", "Supri", "Irri-6"], key="in_variety")
            
            with c2:
                st.number_input("Weight (kg)", min_value=0, step=50, key="in_weight")
                st.slider("Moisture Content (%)", 0.0, 30.0, 14.5, key="in_moisture")
            
            st.markdown("<br>", unsafe_allow_html=True)
            # The submit button triggers the 'handle_new_batch' function
            st.form_submit_button("📡 Transmit to AWS", on_click=handle_new_batch, type="primary")

# === CONSOLE LOGS ===
st.subheader("Server Logs (AWS Stream)")
log_text = "\n".join(st.session_state.logs)
st.text_area("Console Output", value=log_text, height=300, disabled=True)
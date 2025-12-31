import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="RiceMill AWS IoT Controller",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to mimic a clean 'App-like' interface
st.markdown("""
<style>
    /* Global Styles */
    .main { background-color: #0e1117; }
    
    /* Card Styling */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Status Dots */
    .status-dot {
        height: 12px;
        width: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    .status-on { background-color: #10b981; box-shadow: 0 0 8px #10b981; }
    .status-off { background-color: #ef4444; }
    .status-warn { background-color: #f59e0b; }
    
    /* Metric Typography */
    .metric-label { font-size: 0.8rem; color: #9ca3af; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #f3f4f6; }
    
    /* Header Adjustment */
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BACKEND SERVICE (AWS SIMULATION)
# ==========================================
class RiceMillBackend:
    """
    This class simulates the connection to AWS Services.
    In a real deployment, you would import 'boto3' here and connect
    to DynamoDB (for data) and IoT Core (for machines).
    """
    
    def __init__(self):
        # SIMULATING DATABASE (DynamoDB)
        if 'db_batches' not in st.session_state:
            st.session_state.db_batches = [
                {"id": "BATCH-2024-001", "rice_type": "Super Basmati (Old)", "stage": "Polishing", "weight_kg": 1200, "moisture": 11.5, "quality": "A+"},
                {"id": "BATCH-2024-002", "rice_type": "Kainat 1121", "stage": "Husking", "weight_kg": 5000, "moisture": 13.2, "quality": "Std"},
                {"id": "BATCH-2024-003", "rice_type": "Irri-6", "stage": "Intake", "weight_kg": 8500, "moisture": 14.8, "quality": "B"},
            ]
        
        if 'db_orders' not in st.session_state:
            st.session_state.db_orders = [
                {"id": "ORD-8821", "client": "Global Exports Ltd", "item": "Super Basmati", "qty_bags": 500, "status": "Ready"},
                {"id": "ORD-8822", "client": "Local Market Dist.", "item": "Irri-6", "qty_bags": 120, "status": "Processing"},
            ]

        # SIMULATING IOT SHADOWS (AWS IoT Core)
        if 'iot_machines' not in st.session_state:
            st.session_state.iot_machines = {
                "Paddy Cleaner": {"status": "ON", "rpm": 1450, "temp": 45, "vibration": 0.2},
                "Rubber Husker": {"status": "ON", "rpm": 2800, "temp": 62, "vibration": 1.4},
                "Paddy Separator": {"status": "OFF", "rpm": 0, "temp": 24, "vibration": 0.0},
                "Abrasive Whitener": {"status": "ON", "rpm": 3200, "temp": 71, "vibration": 0.8},
                "Silky Polisher": {"status": "ON", "rpm": 1200, "temp": 55, "vibration": 0.3},
                "Color Sorter": {"status": "ERR", "rpm": 0, "temp": 28, "vibration": 0.0},
            }

    # --- Data Fetching Methods ---
    def get_batches(self):
        # Real code: return dynamo_db.Table('Batches').scan()['Items']
        return st.session_state.db_batches

    def get_machines(self):
        # Real code: return iot_client.get_thing_shadow(thingName='RiceMill01')
        # Simulate slight sensor fluctuation for realism
        for name, m in st.session_state.iot_machines.items():
            if m['status'] == "ON":
                m['temp'] += random.uniform(-0.5, 0.5)
                m['vibration'] = max(0, m['vibration'] + random.uniform(-0.1, 0.1))
        return st.session_state.iot_machines

    def get_orders(self):
        return st.session_state.db_orders

    # --- Action Methods ---
    def create_batch(self, rice_type, weight, moisture):
        new_id = f"BATCH-2024-{len(st.session_state.db_batches) + 1:03d}"
        new_batch = {
            "id": new_id,
            "rice_type": rice_type,
            "stage": "Intake",
            "weight_kg": weight,
            "moisture": moisture,
            "quality": "Pending"
        }
        st.session_state.db_batches.append(new_batch)
        return True

    def toggle_machine(self, machine_name):
        # Real code: iot_client.publish(topic='factory/command', payload={'machine': machine_name, 'action': 'toggle'})
        current = st.session_state.iot_machines[machine_name]['status']
        new_status = "OFF" if current == "ON" else "ON"
        st.session_state.iot_machines[machine_name]['status'] = new_status
        return new_status

# Initialize Backend
backend = RiceMillBackend()

# ==========================================
# 3. AUTHENTICATION LOGIC
# ==========================================
def check_login():
    if st.session_state.pin_input == "1234":
        st.session_state.authenticated = True
        st.session_state.pin_input = ""
    else:
        st.toast("❌ Access Denied: Invalid PIN", icon="🔒")

def logout():
    st.session_state.authenticated = False
    st.rerun()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# ==========================================
# 4. MAIN APP INTERFACE
# ==========================================

if not st.session_state.authenticated:
    # LOGIN SCREEN
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='text-align: center; margin-top: 100px;'>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/3061/3061341.png", width=80)
        st.title("RiceMill OS")
        st.markdown("Cloud-Connected Factory Control")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.text_input("Security PIN", type="password", key="pin_input", on_change=check_login)
        st.button("Connect to Mainframe", on_click=check_login, type="primary", use_container_width=True)
        
        st.markdown("---")
        st.caption("Status: 🟢 AWS us-east-1 Connected")

else:
    # LOGGED IN DASHBOARD
    
    # --- Sidebar ---
    with st.sidebar:
        st.title("🌾 FactoryOps")
        st.caption("v2.4.1 | AWS IoT Core")
        
        menu = st.radio("Module Selection", 
            ["Control Room", "Batch Management", "Logistics & Orders", "System Diagnostics"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Mini status in sidebar
        st.markdown("**System Health**")
        st.progress(92)
        st.caption("CPU Load: 92% | Mem: 4.1GB")
        
        st.markdown("<br>"*5, unsafe_allow_html=True)
        if st.button("🔴 Emergency Stop"):
            st.toast("EMERGENCY PROTOCOL INITIATED", icon="🚨")
        if st.button("🔒 Logout"):
            logout()

    # --- View 1: Control Room (Machines) ---
    if menu == "Control Room":
        st.markdown("### 🏭 Live Machine Telemetry")
        st.markdown("Real-time data stream from **AWS IoT Core**")
        
        machines = backend.get_machines()
        
        # Create a grid of cards
        cols = st.columns(3)
        row_idx = 0
        
        for name, data in machines.items():
            # Determine Color based on status
            status_color = "status-on" if data['status'] == "ON" else ("status-warn" if data['status'] == "ERR" else "status-off")
            border_color = "green" if data['status'] == "ON" else "red"
            
            with cols[row_idx % 3]:
                with st.container(border=True):
                    # Header
                    c_head1, c_head2 = st.columns([3, 1])
                    c_head1.markdown(f"**{name}**")
                    c_head2.markdown(f"<div class='status-dot {status_color}'></div>", unsafe_allow_html=True)
                    
                    # Metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric("RPM", data['rpm'])
                    m2.metric("Temp", f"{int(data['temp'])}°C")
                    m3.metric("Vib", f"{data['vibration']:.1f}")
                    
                    # Controls
                    btn_label = "STOP" if data['status'] == "ON" else "START"
                    if st.button(f"{btn_label}", key=f"btn_{name}", type="secondary" if data['status']=="ON" else "primary", use_container_width=True):
                        new_state = backend.toggle_machine(name)
                        st.toast(f"Command sent: {name} -> {new_state}", icon="📡")
                        time.sleep(0.5)
                        st.rerun()
                
            row_idx += 1
            if row_idx % 3 == 0:
                st.write("") # Spacer row

    # --- View 2: Batch Management ---
    elif menu == "Batch Management":
        st.markdown("### 📦 Rice Batch Inventory")
        
        tab1, tab2 = st.tabs(["Active Batches", "Intake New Batch"])
        
        with tab1:
            df = pd.DataFrame(backend.get_batches())
            
            # Styled Dataframe
            st.dataframe(
                df,
                column_config={
                    "moisture": st.column_config.NumberColumn(
                        "Moisture %",
                        format="%.1f%%",
                    ),
                    "weight_kg": st.column_config.ProgressColumn(
                        "Weight (kg)",
                        min_value=0,
                        max_value=10000,
                        format="%d kg",
                    ),
                    "stage": st.column_config.SelectboxColumn(
                        "Processing Stage",
                        options=["Intake", "Cleaning", "Husking", "Polishing", "Grading", "Packing"],
                    )
                },
                use_container_width=True,
                hide_index=True
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.info("💡 **Tip:** Click on 'Processing Stage' cells to update status immediately.")
            with col_b:
                st.download_button("Download Report (CSV)", df.to_csv(), "batches.csv", use_container_width=True)

        with tab2:
            st.markdown("#### Paddy Intake Form")
            with st.form("new_batch_form"):
                c1, c2 = st.columns(2)
                with c1:
                    b_type = st.selectbox("Rice Variety", ["Super Basmati", "Kainat 1121", "Supri", "Irri-6", "C9"])
                    b_weight = st.number_input("Net Weight (kg)", min_value=100, step=50)
                with c2:
                    b_moisture = st.slider("Moisture Content (%)", 0.0, 30.0, 14.0)
                    b_notes = st.text_area("Quality Notes", placeholder="e.g., High broken percentage observed")
                
                submitted = st.form_submit_button("Register Batch", type="primary")
                if submitted:
                    backend.create_batch(b_type, b_weight, b_moisture)
                    st.success("Batch ID Generated & Label Printed!")
                    time.sleep(1)
                    st.rerun()

    # --- View 3: Logistics ---
    elif menu == "Logistics & Orders":
        st.markdown("### 🚚 Global Logistics")
        
        orders = backend.get_orders()
        
        # Order Tracking Kanban-style
        col_pending, col_ready, col_shipped = st.columns(3)
        
        with col_pending:
            st.markdown("#### 🕒 Processing")
            for o in orders:
                if o['status'] == "Processing":
                    st.info(f"**{o['client']}**\n\n{o['item']} - {o['qty_bags']} Bags")
        
        with col_ready:
            st.markdown("#### ✅ Ready for Load")
            for o in orders:
                if o['status'] == "Ready":
                    st.success(f"**{o['client']}**\n\n{o['item']} - {o['qty_bags']} Bags")
                    if st.button("Mark Shipped", key=o['id']):
                        o['status'] = "Shipped"
                        st.toast(f"Order {o['id']} dispatched!", icon="🚛")
                        time.sleep(1)
                        st.rerun()
                        
        with col_shipped:
            st.markdown("#### 🚢 Dispatched")
            for o in orders:
                if o['status'] == "Shipped":
                    st.warning(f"**{o['client']}**\n\n{o['item']} - {o['qty_bags']} Bags")

    # --- View 4: Diagnostics ---
    elif menu == "System Diagnostics":
        st.title("🖥️ Server Room")
        
        st.markdown("### Cloud Connection Status")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("DynamoDB Latency", "24ms", "-2ms")
        col2.metric("IoT Message Rate", "120 msg/min", "+12")
        col3.metric("Error Rate", "0.01%", "0%")
        col4.metric("Active Users", "3")
        
        st.markdown("### Sensor Calibration")
        st.text("Last calibration: 2 days ago")
        
        chart_data = pd.DataFrame({
            'Time': range(20),
            'Vibration': [random.uniform(0, 1) for _ in range(20)],
            'Temperature': [random.uniform(40, 60) for _ in range(20)]
        })
        st.line_chart(chart_data, y=['Vibration', 'Temperature'], height=250)
        
        with st.expander("Advanced Logs"):
            st.code("""
            [10:42:01] INFO: Connected to AWS IoT Endpoint a2x9...
            [10:42:05] INFO: Subscribed to topic 'factory/sensors/#'
            [10:43:12] WARN: Husker vibration deviation detected (0.8 > 0.5)
            [10:44:00] INFO: Batch BATCH-2024-002 sync complete.
            """)
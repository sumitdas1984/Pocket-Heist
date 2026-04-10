import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Pocket Heist | Operations",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM THEMING (HEIST STYLE) ---
st.markdown("""
    <style>
    /* Dark Terminal Theme */
    .main {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .stApp {
        background-color: #0e1117;
    }
    
    /* Heist Cards */
    .heist-card {
        background-color: #1a1c23;
        border-left: 5px solid #ffd700; /* Gold accent */
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .heist-title {
        color: #ffd700;
        font-size: 1.25rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .status-active { color: #00ff41; font-weight: bold; } /* Matrix Green */
    .status-expired { color: #ff4b4b; font-weight: bold; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 8px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        box-shadow: 0 0 10px #2ea043;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (MOCK DB) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'heists' not in st.session_state:
    # Initial Mock Data
    st.session_state.heists = [
        {"id": 1, "title": "The Decoy Doughnut", "target": "Marketing Dept", "difficulty": "Easy", "assigned_to": "Agent_Blue", "creator": "Admin", "deadline": (datetime.now() + timedelta(hours=2)).strftime("%H:%M"), "status": "Active"},
        {"id": 2, "title": "Operation Sticky Note", "target": "CEO Laptop", "difficulty": "Extreme", "assigned_to": "Operative_X", "creator": "Admin", "deadline": (datetime.now() + timedelta(hours=5)).strftime("%H:%M"), "status": "Active"},
        {"id": 3, "title": "The Printer Jam", "target": "HR Printer", "difficulty": "Medium", "assigned_to": "Ghost", "creator": "Agent_Blue", "deadline": "14:00 (Expired)", "status": "Expired"},
    ]

# --- HELPER FUNCTIONS ---
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()

# --- AUTHENTICATION UI ---
def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.icons8.com/ios-filled/100/ffd700/security-configuration.png", width=100)
        st.title("Establish Connection")
        st.subheader("Pocket Heist Terminal")
        
        with st.form("auth_form"):
            user = st.text_input("Operative Codename")
            password = st.text_input("Encryption Key", type="password")
            action = st.form_submit_button("Authenticate")
            
            if action:
                if user and password: # Simple mock validation
                    st.session_state.authenticated = True
                    st.session_state.username = user
                    st.success("Access Granted. Decrypting dashboard...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        
        st.caption("Don't have a codename? [Contact Headquarters]")

# --- MAIN DASHBOARD UI ---
def show_dashboard():
    # Sidebar Nav
    with st.sidebar:
        st.title("🕵️ Pocket Heist")
        st.write(f"Logged in as: **{st.session_state.username}**")
        st.markdown("---")
        nav = st.radio("Navigation", ["🛰 War Room (Active)", "📜 Mission Archive", "✏️ Plan New Heist"])
        st.markdown("---")
        if st.button("Terminate Session (Logout)"):
            logout()

    if nav == "🛰 War Room (Active)":
        st.header("Active Operations")
        st.write("Current missions in progress across the office.")
        
        # Filter active missions
        active_heists = [h for h in st.session_state.heists if h['status'] == "Active"]
        
        if not active_heists:
            st.info("No active heists. Time to plan something devious?")
        else:
            cols = st.columns(2)
            for i, heist in enumerate(active_heists):
                with cols[i % 2]:
                    st.markdown(f"""
                        <div class="heist-card">
                            <div class="heist-title">{heist['title']}</div>
                            <p><b>Target:</b> {heist['target']}</p>
                            <p><b>Difficulty:</b> {heist['difficulty']}</p>
                            <p><b>Assigned To:</b> {heist['assigned_to']}</p>
                            <p><b>Deadline:</b> {heist['deadline']}</p>
                            <p class="status-active">▶ IN PROGRESS</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Abort {heist['id']}", key=f"abort_{heist['id']}"):
                        st.toast("Mission aborted. Scuttling evidence...")

    elif nav == "📜 Mission Archive":
        st.header("Expired & Completed Missions")
        expired_heists = [h for h in st.session_state.heists if h['status'] == "Expired"]
        
        st.table(pd.DataFrame(expired_heists).drop(columns=['id']))

    elif nav == "✏️ Plan New Heist":
        st.header("Mission Blueprint")
        st.write("Define the parameters for your next office mischief.")
        
        with st.form("new_heist_form"):
            title = st.text_input("Mission Name", placeholder="e.g. Operation Desk-Swap")
            target = st.text_input("The Target", placeholder="Who or what is being targeted?")
            
            c1, c2 = st.columns(2)
            difficulty = c1.selectbox("Difficulty Level", ["Training", "Easy", "Medium", "Hard", "Legendary"])
            assignee = c2.text_input("Assign to Operative", placeholder="Codename")
            
            description = st.text_area("Intel / Mission Details", placeholder="Describe the mischief...")

            submit = st.form_submit_button("Launch Heist")
            
            if submit:
                if title and target and assignee:
                    new_h = {
                        "id": len(st.session_state.heists) + 1,
                        "title": title,
                        "target": target,
                        "difficulty": difficulty,
                        "assigned_to": assignee,
                        "creator": st.session_state.username,
                        "deadline": (datetime.now() + timedelta(hours=3)).strftime("%H:%M"),
                        "status": "Active"
                    }
                    st.session_state.heists.insert(0, new_h)
                    st.success("Heist launched! Notification sent to operative.")
                    st.balloons()
                else:
                    st.warning("Blueprint incomplete. Fill all required fields.")

# --- APP ROUTING ---
if not st.session_state.authenticated:
    show_login()
else:
    show_dashboard()
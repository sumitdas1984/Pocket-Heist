"""
Pocket Heist - Streamlit Frontend
A gamified task-assignment application with a spy/heist aesthetic
"""
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Import API client
from api_client import (
    login,
    register,
    list_active_heists,
    list_archive_heists,
    list_my_heists,
    create_heist,
    abort_heist
)

# Page config
st.set_page_config(
    page_title="Pocket Heist",
    page_icon="🕐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark terminal CSS theme
st.markdown("""
<style>
    /* Dark terminal theme */
    :root {
        --primary-color: #FFD700;
        --secondary-color: #FB64B6;
        --background-color: #0e1117;
        --card-background: #0A101D;
        --border-color: #FFD700;
        --text-color: #99A1AF;
        --heading-color: white;
        --success-color: #05DF72;
        --error-color: #FF6467;
    }

    /* Main background */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Headers */
    h1, h2, h3 {
        color: var(--primary-color) !important;
        font-weight: 700;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--card-background);
        color: var(--primary-color);
        border: 1px solid var(--primary-color);
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }

    .stButton>button:hover {
        background-color: var(--primary-color);
        color: var(--background-color);
        border-color: var(--primary-color);
    }

    /* Input fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        background-color: var(--card-background);
        color: var(--heading-color);
        border: 1px solid var(--border-color);
    }

    /* Cards */
    .heist-card {
        background-color: var(--card-background);
        border-left: 4px solid var(--primary-color);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }

    /* Status badge */
    .status-badge {
        background-color: var(--success-color);
        color: var(--background-color);
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--card-background);
    }

    /* Center content for login */
    .center-content {
        display: flex;
        flex-direction: column;
        justify-center: center;
        align-items: center;
        min-height: 60vh;
    }
</style>
""", unsafe_allow_html=True)


def show_login_page():
    """Display login/register screen"""
    st.markdown('<div class="center-content">', unsafe_allow_html=True)

    st.markdown("# 🕐 Pocket Heist")
    st.markdown("### Establish Connection")
    st.markdown("*Tiny missions. Big office mischief.*")
    st.markdown("---")

    tab1, tab2 = st.tabs(["🔐 Authenticate", "📝 Register"])

    with tab1:
        st.markdown("#### Login to Your Account")

        with st.form("login_form"):
            username = st.text_input("Operative Codename", key="login_username")
            password = st.text_input("Encryption Key", type="password", key="login_password")
            submit = st.form_submit_button("Authenticate", use_container_width=True)

            if submit:
                if username and password:
                    try:
                        result = login(username, password)
                        if "error" in result:
                            st.error(result["error"])
                        else:
                            st.success("Connection established!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Connection to HQ lost. Try again. ({str(e)})")
                else:
                    st.warning("Enter both codename and encryption key.")

    with tab2:
        st.markdown("#### Create New Account")

        with st.form("register_form"):
            new_username = st.text_input("Choose Codename", key="register_username")
            new_password = st.text_input("Set Encryption Key (min 8 characters)", type="password", key="register_password")
            confirm_password = st.text_input("Confirm Encryption Key", type="password", key="confirm_password")
            register_submit = st.form_submit_button("Register", use_container_width=True)

            if register_submit:
                if new_username and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Encryption keys do not match.")
                    elif len(new_password) < 8:
                        st.error("Encryption key must be at least 8 characters.")
                    else:
                        try:
                            result = register(new_username, new_password)
                            if "error" in result:
                                st.error(result["error"])
                            else:
                                st.success("Account created! You can now authenticate.")
                        except Exception as e:
                            st.error(f"Registration failed. ({str(e)})")
                else:
                    st.warning("Fill all fields to register.")

    st.markdown('</div>', unsafe_allow_html=True)


def show_war_room():
    """Display active heists (War Room)"""
    st.markdown("# 🎯 War Room - Active Operations")
    st.markdown("*Track ongoing missions and assignments*")
    st.markdown("---")

    try:
        heists = list_active_heists()

        if not heists:
            st.info("📭 No active heists. Time to plan a new mission!")
            return

        # Display in 2-column grid
        col1, col2 = st.columns(2)

        for idx, heist in enumerate(heists):
            col = col1 if idx % 2 == 0 else col2

            with col:
                # Heist card
                st.markdown(f"""
                <div class="heist-card">
                    <h3 style="color: var(--primary-color); margin-top: 0;">🎯 {heist['title']}</h3>
                    <p><strong>Target:</strong> {heist['target']}</p>
                    <p><strong>Difficulty:</strong> {heist['difficulty']}</p>
                    <p><strong>Assigned to:</strong> {heist['assignee_username']}</p>
                    <p><strong>Deadline:</strong> {heist['deadline'][:16]}</p>
                    <p><strong>Creator:</strong> {heist['creator_username']}</p>
                    <span class="status-badge">▶ IN PROGRESS</span>
                </div>
                """, unsafe_allow_html=True)

                # Show description if exists
                if heist.get('description'):
                    with st.expander("📋 Mission Details"):
                        st.write(heist['description'])

                # Abort button (only for creator)
                if heist['creator_username'] == st.session_state.get('username'):
                    if st.button(f"🚫 Abort Mission", key=f"abort_{heist['id']}"):
                        try:
                            result = abort_heist(heist['id'])
                            if "error" in result:
                                st.toast(f"❌ {result['error']}", icon="🚫")
                            else:
                                st.toast(f"✅ Mission aborted: {heist['title']}", icon="🚫")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Failed to abort: {str(e)}")

                st.markdown("---")

    except Exception as e:
        st.error(f"Connection to HQ lost. Try again. ({str(e)})")


def show_mission_archive():
    """Display archived heists (Mission Archive)"""
    st.markdown("# 📚 Mission Archive")
    st.markdown("*Completed and aborted operations*")
    st.markdown("---")

    try:
        heists = list_archive_heists()

        if not heists:
            st.info("📭 No archived heists yet.")
            return

        # Convert to DataFrame for table display
        df_data = []
        for heist in heists:
            df_data.append({
                "ID": heist['id'],
                "Title": heist['title'],
                "Target": heist['target'],
                "Difficulty": heist['difficulty'],
                "Assignee": heist['assignee_username'],
                "Creator": heist['creator_username'],
                "Deadline": heist['deadline'][:16],
                "Status": heist['status'],
                "Created": heist['created_at'][:16]
            })

        df = pd.DataFrame(df_data)

        # Display as table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"Connection to HQ lost. Try again. ({str(e)})")


def show_plan_new_heist():
    """Display form to create new heist (Mission Blueprint)"""
    st.markdown("# 📝 Plan New Heist - Mission Blueprint")
    st.markdown("*Design and launch a new mission*")
    st.markdown("---")

    with st.form("create_heist_form"):
        st.markdown("### Mission Parameters")

        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("🎯 Mission Name *", placeholder="e.g., Steal the Coffee Machine")
            target = st.text_input("🎪 Target *", placeholder="e.g., Office Kitchen")
            difficulty = st.selectbox(
                "⚡ Difficulty *",
                options=["Training", "Easy", "Medium", "Hard", "Legendary"]
            )

        with col2:
            assignee = st.text_input("👤 Assign to Operative *", placeholder="Enter operative codename")

            # Auto-set deadline to +3 hours from now
            default_deadline = datetime.now() + timedelta(hours=3)
            deadline_date = st.date_input("📅 Deadline Date *", value=default_deadline)
            deadline_time = st.time_input("🕐 Deadline Time *", value=default_deadline.time())

        description = st.text_area(
            "📋 Intel / Mission Details",
            placeholder="Optional: Additional mission details, instructions, or intel...",
            height=100
        )

        submit = st.form_submit_button("🚀 Launch Mission", use_container_width=True)

        if submit:
            if not all([title, target, difficulty, assignee]):
                st.warning("⚠️ Blueprint incomplete. Fill all required fields.")
            else:
                try:
                    # Combine date and time
                    deadline_dt = datetime.combine(deadline_date, deadline_time)
                    deadline_iso = deadline_dt.isoformat()

                    result = create_heist(
                        title=title,
                        target=target,
                        difficulty=difficulty,
                        assignee_username=assignee,
                        deadline=deadline_iso,
                        description=description if description else None
                    )

                    if "error" in result:
                        st.error(f"❌ {result['error']}")
                    else:
                        st.success(f"✅ Mission launched: {result['title']}")
                        st.balloons()
                        # Clear form by rerunning
                        st.rerun()

                except Exception as e:
                    st.error(f"Connection to HQ lost. Try again. ({str(e)})")


def show_my_heists():
    """Display heists created by current user"""
    st.markdown("# 📂 My Missions")
    st.markdown("*Heists you have created*")
    st.markdown("---")

    try:
        heists = list_my_heists()

        if not heists:
            st.info("📭 You haven't created any heists yet.")
            return

        for heist in heists:
            status_color = {
                "Active": "var(--success-color)",
                "Aborted": "var(--error-color)",
                "Expired": "var(--text-color)"
            }.get(heist['status'], "var(--text-color)")

            st.markdown(f"""
            <div class="heist-card">
                <h3 style="color: var(--primary-color); margin-top: 0;">🎯 {heist['title']}</h3>
                <p><strong>Target:</strong> {heist['target']}</p>
                <p><strong>Difficulty:</strong> {heist['difficulty']}</p>
                <p><strong>Assigned to:</strong> {heist['assignee_username']}</p>
                <p><strong>Deadline:</strong> {heist['deadline'][:16]}</p>
                <p><strong>Status:</strong> <span style="color: {status_color}; font-weight: 600;">{heist['status']}</span></p>
            </div>
            """, unsafe_allow_html=True)

            if heist.get('description'):
                with st.expander("📋 Mission Details"):
                    st.write(heist['description'])

            st.markdown("---")

    except Exception as e:
        st.error(f"Connection to HQ lost. Try again. ({str(e)})")


def main():
    """Main app logic"""

    # Check if user is authenticated
    if "access_token" not in st.session_state:
        show_login_page()
        return

    # Sidebar navigation
    with st.sidebar:
        st.markdown("# 🕐 Pocket Heist")
        st.markdown(f"**Operative:** {st.session_state.get('username', 'Unknown')}")
        st.markdown("---")

        page = st.radio(
            "Navigation",
            options=[
                "🎯 War Room",
                "📝 Plan New Heist",
                "📂 My Missions",
                "📚 Mission Archive"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")

        if st.button("🚪 Terminate Session", use_container_width=True):
            # Logout
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Display selected page
    if page == "🎯 War Room":
        show_war_room()
    elif page == "📝 Plan New Heist":
        show_plan_new_heist()
    elif page == "📂 My Missions":
        show_my_heists()
    elif page == "📚 Mission Archive":
        show_mission_archive()


if __name__ == "__main__":
    main()

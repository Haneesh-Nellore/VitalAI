import streamlit as st
from auth.session_manager import SessionManager
from components.footer import show_footer
from config.app_config import ANALYSIS_DAILY_LIMIT, APP_NAME, APP_ICON

def show_sidebar():
    with st.sidebar:
        # App branding in sidebar
        st.markdown(f"""
            <div style='
                padding: 1.25rem 0.5rem 1rem 0.5rem;
                border-bottom: 1px solid rgba(99, 179, 237, 0.15);
                margin-bottom: 1rem;
            '>
                <h2 style='
                    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
                    font-size: 1.3rem;
                    font-weight: 700;
                    color: #F1F5F9;
                    margin: 0;
                    letter-spacing: -0.02em;
                '>
                    {APP_ICON} {APP_NAME}
                </h2>
                <p style='
                    color: #475569;
                    font-size: 0.75rem;
                    margin: 0.2rem 0 0 0;
                '>Health Analysis Agent</p>
            </div>
        """, unsafe_allow_html=True)

        # New session button
        if st.button("＋ New Analysis Session", use_container_width=True, type="primary"):
            if st.session_state.user and 'id' in st.session_state.user:
                success, session = SessionManager.create_chat_session()
                if success:
                    st.session_state.current_session = session
                    st.rerun()
                else:
                    st.error("Failed to create session")
            else:
                st.error("Please log in again")
                SessionManager.logout()
                st.rerun()

        # Daily limit counter
        if 'analysis_count' not in st.session_state:
            st.session_state.analysis_count = 0

        remaining = ANALYSIS_DAILY_LIMIT - st.session_state.analysis_count
        remaining_color = "#68D391" if remaining > 3 else "#FC8181"
        progress = (remaining / ANALYSIS_DAILY_LIMIT) * 100

        st.markdown(
            f"""
            <div style='
                padding: 0.75rem 1rem;
                border-radius: 12px;
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(99, 179, 237, 0.1);
                margin: 0.75rem 0;
            '>
                <div style='
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 0.5rem;
                '>
                    <p style='margin: 0; color: #64748B; font-size: 0.78rem; font-weight: 500;'>
                        Daily Analysis Limit
                    </p>
                    <p style='
                        margin: 0;
                        color: {remaining_color};
                        font-weight: 600;
                        font-size: 0.85rem;
                    '>
                        {remaining}/{ANALYSIS_DAILY_LIMIT}
                    </p>
                </div>
                <div style='
                    height: 4px;
                    background: rgba(45, 55, 72, 0.8);
                    border-radius: 2px;
                    overflow: hidden;
                '>
                    <div style='
                        height: 100%;
                        width: {progress}%;
                        background: {remaining_color};
                        border-radius: 2px;
                        transition: width 0.3s ease;
                    '></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin: 0.5rem 0; border-top: 1px solid rgba(99,179,237,0.1);'></div>", unsafe_allow_html=True)

        show_session_list()

        st.markdown("<div style='margin: 0.5rem 0; border-top: 1px solid rgba(99,179,237,0.1);'></div>", unsafe_allow_html=True)

        if st.button("⎋ Logout", use_container_width=True):
            SessionManager.logout()
            st.rerun()

        show_footer(in_sidebar=True)


def show_session_list():
    if st.session_state.user and 'id' in st.session_state.user:
        success, sessions = SessionManager.get_user_sessions()
        if success:
            if sessions:
                st.markdown("""
                    <p style='
                        color: #475569;
                        font-size: 0.75rem;
                        font-weight: 600;
                        letter-spacing: 0.08em;
                        text-transform: uppercase;
                        margin: 0.5rem 0 0.5rem 0;
                    '>Previous Sessions</p>
                """, unsafe_allow_html=True)
                render_session_list(sessions)
            else:
                st.markdown("""
                    <p style='color: #475569; font-size: 0.85rem; text-align: center; padding: 1rem 0;'>
                        No sessions yet
                    </p>
                """, unsafe_allow_html=True)


def render_session_list(sessions):
    if 'delete_confirmation' not in st.session_state:
        st.session_state.delete_confirmation = None

    for session in sessions:
        render_session_item(session)


def render_session_item(session):
    if not session or not isinstance(session, dict) or 'id' not in session:
        return

    session_id = session['id']
    current_session = st.session_state.get('current_session', {})
    current_session_id = current_session.get('id') if isinstance(current_session, dict) else None
    is_active = current_session_id == session_id

    with st.container():
        title_col, delete_col = st.columns([4, 1])

        with title_col:
            label = f"{'▶ ' if is_active else '📝 '}{session['title']}"
            if st.button(label, key=f"session_{session_id}", use_container_width=True):
                st.session_state.current_session = session
                st.rerun()

        with delete_col:
            if st.button("🗑", key=f"delete_{session_id}", help="Delete this session"):
                if st.session_state.delete_confirmation == session_id:
                    st.session_state.delete_confirmation = None
                else:
                    st.session_state.delete_confirmation = session_id
                st.rerun()

        if st.session_state.delete_confirmation == session_id:
            st.warning("Delete this session?")
            left_btn, right_btn = st.columns(2)
            with left_btn:
                if st.button("Yes", key=f"confirm_delete_{session_id}", type="primary", use_container_width=True):
                    handle_delete_confirmation(session_id, current_session_id)
            with right_btn:
                if st.button("No", key=f"cancel_delete_{session_id}", use_container_width=True):
                    st.session_state.delete_confirmation = None
                    st.rerun()


def handle_delete_confirmation(session_id, current_session_id):
    if not session_id:
        st.error("Invalid session")
        return

    success, error = SessionManager.delete_session(session_id)
    if success:
        st.session_state.delete_confirmation = None
        if current_session_id and current_session_id == session_id:
            st.session_state.current_session = None
        st.rerun()
    else:
        st.error(f"Failed to delete: {error}")

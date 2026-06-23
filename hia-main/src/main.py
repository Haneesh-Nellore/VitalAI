import streamlit as st
from auth.session_manager import SessionManager
from components.auth_pages import show_login_page
from components.sidebar import show_sidebar
from components.analysis_form import show_analysis_form
from components.footer import show_footer
from components.header import show_header
from components.health_score import show_health_score_dashboard
from config.app_config import APP_NAME, APP_TAGLINE, APP_DESCRIPTION, APP_ICON
from services.ai_service import get_chat_response

# Must be the first Streamlit command
st.set_page_config(
    page_title=f"{APP_NAME} - Health Analysis Agent",
    page_icon=APP_ICON,
    layout="wide"
)

# Initialize session state
SessionManager.init_session()

# Global dark theme
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #0F172A !important;
            color: #F1F5F9 !important;
        }

        /* Sidebar dark */
        section[data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid rgba(99, 179, 237, 0.1) !important;
        }

        /* Hide form submission helper text */
        div[data-testid="InputInstructions"] > span:nth-child(1) {
            visibility: hidden;
        }

        /* Chat input */
        .stChatInput > div {
            background-color: #1E293B !important;
            border: 1px solid #2D3748 !important;
            border-radius: 12px !important;
        }

        /* Info boxes (user messages) */
        .stAlert[data-baseweb="notification"] {
            background-color: #1E293B !important;
            border: 1px solid rgba(99, 179, 237, 0.2) !important;
            border-radius: 12px !important;
            color: #F1F5F9 !important;
        }

        /* Success boxes (AI messages) */
        div[data-testid="stSuccessMessage"] {
            background-color: rgba(104, 211, 145, 0.08) !important;
            border: 1px solid rgba(104, 211, 145, 0.2) !important;
            border-radius: 12px !important;
            color: #F1F5F9 !important;
        }

        /* Expander */
        .streamlit-expanderHeader {
            background-color: #1E293B !important;
            border-radius: 10px !important;
            color: #94A3B8 !important;
        }

        /* Primary button */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
            border: none !important;
            border-radius: 10px !important;
            color: white !important;
            font-weight: 600 !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


def show_welcome_screen():
    st.markdown(f"""
        <div style='
            text-align: center;
            padding: 5rem 2rem;
        '>
            <div style='
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #3B82F6, #06B6D4);
                border-radius: 24px;
                font-size: 2.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
            '>
                {APP_ICON}
            </div>
            <h1 style='
                font-family: Inter, sans-serif;
                font-size: 2.5rem;
                font-weight: 700;
                color: #F1F5F9;
                margin: 0 0 0.75rem 0;
                letter-spacing: -0.03em;
            '>{APP_NAME}</h1>
            <p style='
                color: #64748B;
                font-size: 1.1rem;
                margin: 0 0 0.5rem 0;
            '>{APP_DESCRIPTION}</p>
            <p style='
                color: #475569;
                font-size: 0.95rem;
                margin: 0 0 2.5rem 0;
            '>{APP_TAGLINE}</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        if st.button("＋ Create New Analysis Session", use_container_width=True, type="primary"):
            success, session = SessionManager.create_chat_session()
            if success:
                st.session_state.current_session = session
                st.rerun()
            else:
                st.error("Failed to create session")


def show_chat_history():
    success, messages = st.session_state.auth_service.get_session_messages(
        st.session_state.current_session["id"]
    )

    if success:
        first_assistant = True
        for msg in messages:
            if msg.get("role") == "system":
                continue
            if msg["role"] == "user":
                st.markdown(f"""
                    <div style='
                        background: rgba(30, 41, 59, 0.8);
                        border: 1px solid rgba(99, 179, 237, 0.15);
                        border-radius: 12px;
                        padding: 0.875rem 1.25rem;
                        margin: 0.5rem 0;
                        color: #CBD5E0;
                        font-size: 0.92rem;
                    '>
                        <span style='color: #63B3ED; font-size: 0.75rem; font-weight: 600;'>YOU</span><br/>
                        {msg["content"]}
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Show health score dashboard before first AI response
                if first_assistant:
                    show_health_score_dashboard(msg["content"])
                    first_assistant = False

                st.markdown(f"""
                    <div style='
                        background: rgba(104, 211, 145, 0.06);
                        border: 1px solid rgba(104, 211, 145, 0.15);
                        border-radius: 12px;
                        padding: 0.875rem 1.25rem;
                        margin: 0.5rem 0;
                        color: #E2E8F0;
                        font-size: 0.92rem;
                        line-height: 1.7;
                    '>
                        <span style='color: #68D391; font-size: 0.75rem; font-weight: 600;'>🤖 VITALAI</span><br/>
                        {msg["content"]}
                    </div>
                """, unsafe_allow_html=True)

        return messages
    return []


def handle_chat_input(messages):
    if prompt := st.chat_input("Ask a follow-up question about your report..."):
        st.markdown(f"""
            <div style='
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(99, 179, 237, 0.15);
                border-radius: 12px;
                padding: 0.875rem 1.25rem;
                margin: 0.5rem 0;
                color: #CBD5E0;
            '>
                <span style='color: #63B3ED; font-size: 0.75rem; font-weight: 600;'>YOU</span><br/>
                {prompt}
            </div>
        """, unsafe_allow_html=True)

        st.session_state.auth_service.save_chat_message(
            st.session_state.current_session["id"], prompt, role="user"
        )

        context_text = st.session_state.get("current_report_text", "")

        if not context_text and messages:
            for msg in messages:
                if msg.get("role") == "system" and "__REPORT_TEXT__" in msg.get("content", ""):
                    content = msg.get("content", "")
                    start_idx = content.find("__REPORT_TEXT__\n") + len("__REPORT_TEXT__\n")
                    end_idx = content.find("\n__END_REPORT_TEXT__")
                    if start_idx > len("__REPORT_TEXT__\n") - 1 and end_idx > start_idx:
                        context_text = content[start_idx:end_idx]
                        st.session_state.current_report_text = context_text
                        break

        with st.spinner("Thinking..."):
            response = get_chat_response(prompt, context_text, messages)

            st.markdown(f"""
                <div style='
                    background: rgba(104, 211, 145, 0.06);
                    border: 1px solid rgba(104, 211, 145, 0.15);
                    border-radius: 12px;
                    padding: 0.875rem 1.25rem;
                    margin: 0.5rem 0;
                    color: #E2E8F0;
                    line-height: 1.7;
                '>
                    <span style='color: #68D391; font-size: 0.75rem; font-weight: 600;'>🤖 VITALAI</span><br/>
                    {response}
                </div>
            """, unsafe_allow_html=True)

            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session["id"], response, role="assistant"
            )
            st.rerun()


def main():
    SessionManager.init_session()

    if not SessionManager.is_authenticated():
        show_login_page()
        show_footer()
        return

    # Show header
    show_header()

    # Show sidebar
    show_sidebar()

    # Main content
    if st.session_state.get("current_session"):
        st.markdown(f"""
            <h2 style='
                font-size: 1.3rem;
                font-weight: 600;
                color: #F1F5F9;
                margin: 0 0 1.5rem 0;
                letter-spacing: -0.01em;
            '>📊 {st.session_state.current_session["title"]}</h2>
        """, unsafe_allow_html=True)

        messages = show_chat_history()

        if messages:
            with st.expander("🔄 New Analysis / Update Report", expanded=False):
                show_analysis_form()
            handle_chat_input(messages)
        else:
            show_analysis_form()
    else:
        show_welcome_screen()


if __name__ == "__main__":
    main()

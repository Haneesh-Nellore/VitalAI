import streamlit as st
from auth.session_manager import SessionManager
from config.app_config import APP_ICON, APP_NAME, APP_TAGLINE, APP_DESCRIPTION
from utils.validators import validate_signup_fields
import time

def show_login_page():
    if 'form_type' not in st.session_state:
        st.session_state['form_type'] = 'login'

    current_form = st.session_state['form_type']

    # Global dark theme styles
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

            html, body, [class*="css"] {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: #0F172A;
                color: #F1F5F9;
            }

            div[data-testid="InputInstructions"] > span:nth-child(1) {
                visibility: hidden;
            }

            /* Input fields */
            .stTextInput > div > div > input {
                background-color: #1E293B !important;
                border: 1px solid #2D3748 !important;
                border-radius: 10px !important;
                color: #F1F5F9 !important;
                padding: 0.6rem 1rem !important;
                font-size: 0.95rem !important;
            }

            .stTextInput > div > div > input:focus {
                border-color: #63B3ED !important;
                box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.15) !important;
            }

            /* Primary button */
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
                border: none !important;
                border-radius: 10px !important;
                color: white !important;
                font-weight: 600 !important;
                padding: 0.6rem 1.5rem !important;
                font-size: 0.95rem !important;
                letter-spacing: 0.02em !important;
                transition: all 0.2s ease !important;
            }

            .stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
            }

            /* Secondary button */
            .stButton > button[kind="secondary"] {
                background: transparent !important;
                border: 1px solid #2D3748 !important;
                border-radius: 10px !important;
                color: #94A3B8 !important;
                font-size: 0.9rem !important;
            }

            .stButton > button[kind="secondary"]:hover {
                border-color: #63B3ED !important;
                color: #63B3ED !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Hero section
    st.markdown(f"""
        <div style='
            text-align: center;
            padding: 3rem 1rem 2rem 1rem;
        '>
            <div style='
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 72px;
                height: 72px;
                background: linear-gradient(135deg, #3B82F6, #06B6D4);
                border-radius: 20px;
                font-size: 2rem;
                margin-bottom: 1.25rem;
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
            '>
                {APP_ICON}
            </div>
            <h1 style='
                font-family: Inter, sans-serif;
                font-size: 2.2rem;
                font-weight: 700;
                color: #F1F5F9;
                margin: 0 0 0.5rem 0;
                letter-spacing: -0.03em;
            '>
                {APP_NAME}
            </h1>
            <p style='
                color: #64748B;
                font-size: 1rem;
                margin: 0 0 0.5rem 0;
            '>
                {APP_TAGLINE}
            </p>
            <p style='
                color: #63B3ED;
                font-size: 1.05rem;
                font-weight: 500;
                margin: 0;
            '>
                {"Welcome back 👋" if current_form == 'login' else "Create your account ✨"}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if current_form == 'login':
            show_login_form()
        else:
            show_signup_form()

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        toggle_text = "Don't have an account? Sign up →" if current_form == 'login' else "Already have an account? Login →"
        if st.button(toggle_text, use_container_width=True, type="secondary"):
            st.session_state['form_type'] = 'signup' if current_form == 'login' else 'login'
            st.rerun()

def show_login_form():
    with st.form("login_form"):
        st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin-bottom: 0.25rem;'>Email</p>", unsafe_allow_html=True)
        email = st.text_input("Email", key="login_email", label_visibility="collapsed")

        st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin: 0.75rem 0 0.25rem 0;'>Password</p>", unsafe_allow_html=True)
        password = st.text_input("Password", type="password", key="login_password", label_visibility="collapsed")

        st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

        if st.form_submit_button("Login", use_container_width=True, type="primary"):
            if email and password:
                success, result = SessionManager.login(email, password)
                if success:
                    with st.spinner("Logging in..."):
                        st.success("Login successful! Redirecting...")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error(f"Login failed: {result}")
            else:
                st.error("Please enter both email and password")

def show_signup_form():
    with st.form("signup_form"):
        st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin-bottom: 0.25rem;'>Full Name</p>", unsafe_allow_html=True)
        new_name = st.text_input("Full Name", key="signup_name", label_visibility="collapsed")

        st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin: 0.75rem 0 0.25rem 0;'>Email</p>", unsafe_allow_html=True)
        new_email = st.text_input("Email", key="signup_email", label_visibility="collapsed")

        st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin: 0.75rem 0 0.25rem 0;'>Password</p>", unsafe_allow_html=True)
        new_password = st.text_input("Password", type="password", key="signup_password", label_visibility="collapsed")

        st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin: 0.75rem 0 0.25rem 0;'>Confirm Password</p>", unsafe_allow_html=True)
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_password2", label_visibility="collapsed")

        st.markdown("""
            <div style='
                background: rgba(99, 179, 237, 0.08);
                border: 1px solid rgba(99, 179, 237, 0.15);
                border-radius: 10px;
                padding: 0.75rem 1rem;
                margin: 1rem 0;
            '>
                <p style='color: #64748B; font-size: 0.8rem; margin: 0 0 0.4rem 0; font-weight: 500;'>Password requirements:</p>
                <p style='color: #64748B; font-size: 0.78rem; margin: 0; line-height: 1.6;'>
                    ✓ At least 8 characters &nbsp;
                    ✓ One uppercase letter &nbsp;
                    ✓ One lowercase letter &nbsp;
                    ✓ One number
                </p>
            </div>
        """, unsafe_allow_html=True)

        if st.form_submit_button("Create Account", use_container_width=True, type="primary"):
            validation_result = validate_signup_fields(
                new_name, new_email, new_password, confirm_password
            )

            if not validation_result[0]:
                st.error(validation_result[1])
                return

            with st.spinner("Creating your account..."):
                success, response = st.session_state.auth_service.sign_up(
                    new_email, new_password, new_name
                )

                if success:
                    st.session_state.authenticated = True
                    st.session_state.user = response
                    st.success("Account created! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Sign up failed: {response}")

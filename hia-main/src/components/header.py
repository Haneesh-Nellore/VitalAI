import streamlit as st
from config.app_config import APP_NAME, APP_ICON, APP_TAGLINE, PRIMARY_COLOR, TEXT_SECONDARY

def show_header():
    # App branding header
    st.markdown(f"""
        <div style='
            padding: 1.5rem 0 1rem 0;
            border-bottom: 1px solid rgba(99, 179, 237, 0.15);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        '>
            <div>
                <h1 style='
                    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
                    font-size: 1.8rem;
                    font-weight: 700;
                    color: #F1F5F9;
                    margin: 0;
                    letter-spacing: -0.02em;
                '>
                    {APP_ICON} {APP_NAME}
                </h1>
                <p style='
                    font-size: 0.85rem;
                    color: #94A3B8;
                    margin: 0.25rem 0 0 0;
                    letter-spacing: 0.01em;
                '>
                    {APP_TAGLINE}
                </p>
            </div>
            {_user_badge()}
        </div>
    """, unsafe_allow_html=True)

def _user_badge():
    if st.session_state.get('user'):
        display_name = st.session_state.user.get('name') or st.session_state.user.get('email', '')
        # Show only first name or email prefix
        short_name = display_name.split('@')[0].split(' ')[0].capitalize()
        return f"""
            <div style='
                display: flex;
                align-items: center;
                gap: 0.5rem;
                background: rgba(99, 179, 237, 0.1);
                border: 1px solid rgba(99, 179, 237, 0.2);
                border-radius: 2rem;
                padding: 0.4rem 0.9rem;
            '>
                <div style='
                    width: 28px;
                    height: 28px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #63B3ED, #4299E1);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.75rem;
                    font-weight: 700;
                    color: white;
                '>
                    {short_name[0].upper()}
                </div>
                <span style='
                    color: #CBD5E0;
                    font-size: 0.85rem;
                    font-weight: 500;
                '>
                    {short_name}
                </span>
            </div>
        """
    return ""

import streamlit as st
from config.app_config import APP_NAME, APP_ICON, APP_TAGLINE


def show_header():
    st.markdown(f"""
        <div style='
            padding: 1.25rem 0 1rem 0;
            border-bottom: 1px solid rgba(99, 179, 237, 0.15);
            margin-bottom: 1.5rem;
        '>
            <h1 style='
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 1.8rem;
                font-weight: 700;
                color: #F1F5F9;
                margin: 0;
                letter-spacing: -0.02em;
            '>{APP_ICON} {APP_NAME}</h1>
            <p style='
                font-size: 0.85rem;
                color: #94A3B8;
                margin: 0.25rem 0 0 0;
            '>{APP_TAGLINE}</p>
        </div>
    """, unsafe_allow_html=True)

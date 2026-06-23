import streamlit as st
import requests

def get_github_stars():
    try:
        response = requests.get("https://api.github.com/repos/Haneesh-Nellore/VitalAI")
        if response.status_code == 200:
            return response.json()["stargazers_count"]
        return None
    except:
        return None

def show_footer(in_sidebar=False):
    @st.cache_data(ttl=3600)
    def get_cached_stars():
        return get_github_stars()

    stars_count = get_cached_stars()

    base_styles = f"""
        text-align: center;
        padding: 1rem;
        background: rgba(15, 23, 42, 0.6);
        border-top: 1px solid rgba(99, 179, 237, 0.15);
        margin-top: {'0' if in_sidebar else '2rem'};
        {'width: 100%' if not in_sidebar else ''};
    """

    st.markdown(
        f"""
        <div style='{base_styles}'>
            <p style='
                font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
                color: #64B5F6;
                font-size: 0.75rem;
                letter-spacing: 0.05em;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 6px;
            '>
                <span style="color: #4a5568; font-size: 0.7rem;">
                    <a href='https://github.com/Haneesh-Nellore/VitalAI'
                       target='_blank'
                       style='color: #63B3ED; text-decoration: none; font-weight: 500;'>
                        ⭐ VitalAI on GitHub
                        {f' · {stars_count} stars' if stars_count is not None else ''}
                    </a>
                </span>
                <span style="color: #4a5568; font-size: 0.7rem;">
                    Built by
                    <a href='https://linkedin.com/in/haneeshnellore'
                       target='_blank'
                       style='color: #63B3ED; text-decoration: none; font-weight: 500;'>
                        Haneesh Nellore
                    </a>
                </span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

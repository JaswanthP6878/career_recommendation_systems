# ui.py
import streamlit as st

def sidebar_settings():
    with st.sidebar:
        st.image("Logo/yat_logo_white.svg", width="stretch")

        st.write("Accessibility")

        font_options = {
            "Standard": 18,
            "Large": 24,
            "Extra Large": 32,
        }

        selected = st.radio(
            "Text Size",
            options=list(font_options.keys()),
            horizontal=False
        )
        st.session_state.font_size = font_options[selected]


def apply_styles():
    font_size = st.session_state.get("font_size", 18)

    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: 'DM Sans', sans-serif;
            font-size: {font_size}px;
        }}
        h1, h2, h3 {{
            font-family: 'Bebas Neue', sans-serif;
            letter-spacing: 0.04em;
        }}
        .stButton > button {{
            border-radius: 30px;
            font-family: 'DM Sans', sans-serif;
            font-weight: 700;
        }}
        /* --- Assessment radio options as vertical selection cards --- */
        [data-testid="stRadio"] [role="radiogroup"] > label {{
            background: #181818;
            border: 1px solid #2a2a2a;
            border-radius: 10px;
            padding: 12px 18px;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            transition: border-color 0.15s, background 0.15s;
            width: 100%;
        }}
        [data-testid="stRadio"] [role="radiogroup"] > label:hover {{
            border-color: #F5C800;
            background: #202020;
        }}
        [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {{
            border-color: #F5C800;
            background: rgba(245, 200, 0, 0.08);
        }}
        [data-testid="stRadio"] [role="radiogroup"] > label > div:first-child {{
            display: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

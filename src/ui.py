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

        st.session_state.high_contrast = st.toggle(
            "High Contrast",
            value=st.session_state.get("high_contrast", False)
        )
        st.session_state.reduce_motion = st.toggle(
            "Reduce Motion",
            value=st.session_state.get("reduce_motion", False)
        )


def apply_styles():
    font_size = st.session_state.get("font_size", 18)
    high_contrast = st.session_state.get("high_contrast", False)
    reduce_motion = st.session_state.get("reduce_motion", False)

    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True
    )

    contrast_css = """
        html, body, [class*="css"] { background-color: #000000 !important; color: #ffffff !important; }
        .stButton > button { border: 2px solid #ffffff !important; }
        [data-testid="stSidebar"] { background-color: #000000 !important; }
    """ if high_contrast else ""

    motion_css = """
        *, *::before, *::after {
            animation-duration: 0.001ms !important;
            transition-duration: 0.001ms !important;
        }
    """ if reduce_motion else ""

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
        {contrast_css}
        {motion_css}
        </style>
        """,
        unsafe_allow_html=True
    )

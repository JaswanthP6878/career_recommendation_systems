# ui.py
import streamlit as st

def sidebar_settings():
    with st.sidebar:
        st.image("Logo/young_aspiring_thinkers_logo.png")
        
        st.header("Appearance")

        st.session_state.font_size = st.slider(
            "Font size",
            12,
            32,
            st.session_state.get("font_size", 18)
        )

        

def apply_styles():
    font_size = st.session_state.get("font_size", 18)

    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-size: {font_size}px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
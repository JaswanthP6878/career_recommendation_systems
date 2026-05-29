import os, base64
import streamlit as st
from src.ui import sidebar_settings, apply_styles

sidebar_settings()
apply_styles()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()



### find icon in https://fonts.google.com/icons?utm_source=chatgpt.com

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

Interest = st.Page("Profile/Interest.py", title="Interest", icon=":material/favorite:")
Skill = st.Page("Profile/Skill.py", title="Skills", icon=":material/favorite:")

Recommender = st.Page("Tools/Recommender.py", title="Matches", icon=":material/compare_arrows:", default=True)

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Profile": [Interest, Skill],
            "Tools": [Recommender]
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
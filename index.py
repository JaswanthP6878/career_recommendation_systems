import os, base64
import streamlit as st
from src.ui import sidebar_settings, apply_styles

sidebar_settings()
apply_styles()

# -----------------------------------
# Initialize Session State
# -----------------------------------

defaults = {
    "name": "Brian Mwangi",
    "gender": "Male",
    "age": 16,
    "education": "Grade 10",
    "languages": ["English", "Swahili (Kiswahili)"],
    "location": "Kenya",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.text_input("Username:")
    st.text_input("Password:", type = "password")
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

Person = st.Page("Profile/Person.py", title="My Info", icon=":material/person:", default=True)
Interest = st.Page("Profile/Interest.py", title="Interest", icon=":material/favorite:")
Skill = st.Page("Profile/Skill.py", title="Skills", icon=":material/favorite:")

Recommender = st.Page("Tools/Recommender.py", title="Recommendations", icon=":material/compare_arrows:")
Chatbot = st.Page("Tools/Chatbot.py", title="Live Advisor", icon=":material/smart_toy:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Profile": [Person, Interest, Skill],
            "Tools": [Recommender, Chatbot],
            "Account": [logout_page],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
import types
import streamlit as st
from openai import OpenAI
import google.generativeai as genai

UseOpenAi = True

st.title("🤖 Career Advisor Monewa")

if UseOpenAi:
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    if "LLM_model" not in st.session_state:
        st.session_state["LLM_model"] = "gpt-3.5-turbo"
    model = client
else:
    # Configure Gemini API
    genai.configure(api_key=st.secrets["gemini"]["api_key"])
    # Load Gemini model
    if "LLM_model" not in st.session_state:
        st.session_state["LLM_model"] = "gemini-3.5-flash"
    model = genai.GenerativeModel("gemini-3.5-flash")


prompt = f"""
You are Monewa, an experienced carreer advisor in Africa.

You're helping a student. Advior based on their profile, interests, and skills.
Name:{st.session_state["name"]}
Gender:{st.session_state["gender"]}
Age:{st.session_state["age"]}
Education:{st.session_state["education"]}
Languages:{st.session_state["languages"]}
Location:{st.session_state["location"]}

they're interested in {st.session_state["selected_interests"] if "selected_interests" in st.session_state else None}

they have following skills: {st.session_state["selected_skills"] if "selected_skills" in st.session_state else None}

they might be good fit for {st.session_state["recommending_jobs"] if "recommending_jobs" in st.session_state else None}

They may need help to understands
- all possible career option.
- what school(s), course(s), and/or certificate(s) they will need to pursue their goal.
Make sure your reply is easy to follow for their age. Be patient and fun!

Now, just say hi to the student and simply suggest 3 things you can help them with (keep it short & sweet).
"""


def fetch_response(user_query):
    if UseOpenAi:
        messages = [{"role": "system", "content": prompt}]
        for msg in st.session_state.chat_session.history:
            role = "assistant" if msg["role"] == "model" else msg["role"]
            messages.append({"role": role, "content": msg["content"]})
        if user_query:
            messages.append({"role": "user", "content": user_query})
        response = client.chat.completions.create(
            model=st.session_state["LLM_model"],
            messages=messages,
        )
        return response.choices[0].message.content
    else:
        response = st.session_state.chat_session.model.generate_content(user_query)
        return response.parts[0].text


# Function to translate roles between Gemini and Streamlit terminology
def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    if UseOpenAi:
        st.session_state.chat_session = types.SimpleNamespace(history=[])
        response_text = fetch_response("")
    else:
        st.session_state.chat_session = model.start_chat(history=[])
        response = st.session_state.chat_session.model.generate_content(prompt)
        response_text = response.parts[0].text
    st.session_state.chat_session.history.append({"role": "model", "content": response_text})


# Display the chat history
for msg in st.session_state.chat_session.history:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

# Input field for user's message
user_input = st.chat_input("Ask Advisor Monewa...")
if user_input:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_input)

    # Get response from the active model
    response_text = fetch_response(user_input)

    # Display the response
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Add user and assistant messages to the chat history
    st.session_state.chat_session.history.append({"role": "user", "content": user_input})
    st.session_state.chat_session.history.append({"role": "model", "content": response_text})

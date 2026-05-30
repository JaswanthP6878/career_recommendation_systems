import streamlit as st
from openai import OpenAI
import google.generativeai as genai

UseOpenAi = False

st.title("🤖 Career Advisor Monewa")

if UseOpenAi:
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    if "LLM_model" not in st.session_state:
        st.session_state["LLM_model"] = "gpt-3.5-turbo"
else:
    # Configure Gemini API
    genai.configure(api_key=st.secrets["gemini"]["api_key"])
    # Load Gemini model
    if "LLM_model" not in st.session_state:
        st.session_state["LLM_model"]  = "gemini-3.5-flash"
    model = genai.GenerativeModel("gemini-3.5-flash")


prompt = f"""
You are Monewa, an experienced carreer advisor in Africa. 

You're helping a student. Advior based on their profile, interests, and skills.
Name:{st.session_state["name"]}
Gender:{st.session_state["gender"]}
Age:{st.session_state["age"]}
Education:{st.session_state["education"]}
Location:{st.session_state["location"]}

they're interested in {st.session_state["selected_interests"] if "selected_interests" in st.session_state else None}

they have following skills: {st.session_state["selected_skills"] if "selected_skills" in st.session_state else None}

They may need help to understands 
- all possible career option. 
- what school(s), course(s), and/or certificate(s) they will need to pursue their goal. 
Make sure your reply is easy to follow for their age. Be patient and fun! 

Now, just say hi to the student and simply suggest 3 things you can help them with (keep it short & sweet). 
"""

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    response = st.session_state.chat_session.model.generate_content(prompt)
    st.session_state.chat_session.history.append({"role": "model", "content": response.parts[0].text})

# Function to translate roles between Gemini and Streamlit terminology
def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role

def fetch_gemini_response(user_query):
    # Use the session's model to generate a response
    response = st.session_state.chat_session.model.generate_content(user_query)
    print(f"Gemini's Response: {response}")
    return response.parts[0].text


# Display the chat history
for msg in st.session_state.chat_session.history:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

# Input field for user's message
user_input = st.chat_input("Ask Advisor Monewa...")
if user_input:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_input)

    # Send user's message to Gemini and get the response
    gemini_response = fetch_gemini_response(user_input)

    # Display Gemini's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    # Add user and assistant messages to the chat history
    st.session_state.chat_session.history.append({"role": "user", "content": user_input})
    st.session_state.chat_session.history.append({"role": "model", "content": gemini_response})

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         stream = client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )
#         response = st.write_stream(stream)
#     st.session_state.messages.append({"role": "assistant", "content": response})
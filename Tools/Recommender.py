# app.py
import os
import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer
from PIL import Image
import base64

UseOpenAi = False
for key in ["skills", "interests"]:
    if f"selected_{key}" not in st.session_state:
        st.session_state[f"selected_{key}"] = []


# # === Centered logo and header block ===
# col1, col2, col3 = st.columns([1, 2, 1])
# with col2:
#     logo = Image.open("young_aspiring_thinkers_logo.png")
#     st.image(logo, width=180)

st.markdown(
    "<h1 style='text-align: left;'>🎓 Career Path Recommender</h1>",
    unsafe_allow_html=True
)
st.write("Answer a few questions to get a personalized career suggestion!")

# === Inputs ===
interests = st.multiselect(
    "What are your interests?",
    ["Information Technology (IT)", "Business", "Healthcare", "Engineering", "Media", "Agriculture", "Finance", "AI", 
     "Design", "Education", "Audit & Tax", "Mining", "Transportation & Logistics"], 
    default=st.session_state["selected_interests"] # Get Saved Interests from Session State
)

if st.session_state["selected_interests"] == []:
    st.write("Don’t know your interests yet? Take the assessment:")

    if st.button("🧠 Take Interest Assessment"):
        st.switch_page("Profile/Interest.py") 

# -----------------------------------
# Skill Options
# -----------------------------------

skill_options = [
    # WEF 2025 Core Skills
    "Analytical Thinking", "Resilience, Flexibility & Agility", "Leadership & Social Influence",
    "Creative Thinking", "Motivation & Self-awareness", "Technological Literacy",
    "Empathy & Active Listening", "Curiosity & Lifelong Learning", "Talent Management",
    "Service Orientation & Customer Service",

    # Technical/Domain-Specific Skills
    "Coding", "Math", "Data Analysis",
    "Public Speaking", "Project Management", "Research",
    "Financial Modeling"
]

# -----------------------------------
# Multiselect
# -----------------------------------

skills = st.multiselect(
    "What skills do you have?",
    skill_options,
    default=st.session_state["selected_skills"] # Get Saved Skills from Session State
)

if st.session_state["selected_skills"] == []:
    st.write("Don’t know your skills yet? Take the assessment:")

    if st.button("🧠 Take Skill Assessment"):
        st.switch_page("Profile/Skill.py") 

education_list = ["Grade 10", "Grade 11", "Grade 12", "Post-matric / University"]

education = st.selectbox(
    "What is your current education level?",
    education_list,
    index=education_list.index(st.session_state["education"])
)

submit = st.button("Find My Career Path")

# === Load Karrierewege model ===
@st.cache_resource
def load_model():
    model_name = "ElenaSenger/career-path-representation-mpnet-karrierewege"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

## === If user submits ===
if submit:
    # === Step 1: Generate starting job using OpenAI/Gemini ===
    prompt = f"""
    Based on the following student profile, suggest one starting job they could pursue after school 
    (e.g., IT Assistant, Lab Technician, Sales Trainee). Be concise.

    Interests: {', '.join(interests)}
    Skills: {', '.join(skills)}
    Education: {education}

    Only return the job title and nothing else.
    """
    if UseOpenAi:
        client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    else:
        # Configure Gemini API
        genai.configure(api_key=st.secrets["gemini"]["api_key"])
        # Load Gemini model
        gemini_model = genai.GenerativeModel("gemini-3.5-flash")



    try:
        with st.spinner("Thinking..."):
            if UseOpenAi:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful career advisor."},
                        {"role": "user", "content": prompt}
                    ]
                )
                starting_job = response.choices[0].message.content.strip()
            else:
                # Gemini response
                response = gemini_model.generate_content(prompt)
                starting_job = response.text.strip()

            st.success(f"🧭 Starting Role: {starting_job}")

            # === Step 2: Karrierewege inference ===
            candidate_jobs = [
                "Software Developer",
                "Marketing Specialist",
                "Data Analyst",
                "AI Researcher",
                "Mechanical Engineer",
                "Healthcare Assistant",
                "Teacher",
                "Sales Manager",
                "UX Designer",
                "Lab Technician"
            ]

            # Embed history
            history_inputs = tokenizer(starting_job, return_tensors="pt")

            with torch.no_grad():
                history_output = model(**history_inputs)
                history_embedding = history_output.pooler_output

            # Embed candidates
            candidate_inputs = tokenizer(
                candidate_jobs,
                padding=True,
                truncation=True,
                return_tensors="pt"
            )

            with torch.no_grad():
                candidate_output = model(**candidate_inputs)
                candidate_embeddings = candidate_output.pooler_output

            # Cosine similarity
            similarities = F.cosine_similarity(
                history_embedding,
                candidate_embeddings
            )

            top_scores, top_indices = similarities.topk(3)

            st.write("🔮 **Top Recommended Career Paths:**")

            for i in top_indices:
                st.write(
                    f"• {candidate_jobs[i]} "
                    f"(Score: {similarities[i]:.2f})"
                )
            
            # if st.button("Start Talking to the Advisor"):
            #     st.switch_page("Tools/Chatbot.py")

    except Exception as e:
        st.error(f"Error generating career suggestion: {e}")

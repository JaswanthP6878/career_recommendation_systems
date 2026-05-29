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

#st.set_page_config(page_title="Career Recommender", layout="centered")


# Convert local image to base64
def get_base64_logo(path):
    if not os.path.exists(path):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(os.path.join("Logo", path)):
            path = os.path.join("Logo", path)
        elif os.path.exists(os.path.join(current_dir, path)):
            path = os.path.join(current_dir, path)
        elif os.path.exists(os.path.join(current_dir,"Logo", path)):
            path = os.path.join(current_dir,"Logo", path)
    print(path)
    with open(path, "rb") as image_file:
        # if path.endswith('svg'):
        #     return base64.b64encode(path.encode('utf-8')).decode("utf-8")
        return base64.b64encode(image_file.read()).decode()

logo_base64 = get_base64_logo("young_aspiring_thinkers_logo.png")
#logo_base64 = get_base64_logo("yat_logo_white.svg")

# Inject fixed-position clickable logo in top-left corner
# Inject fixed-position clickable logo (lower + larger)
st.markdown(f"""
    <style>
    .fixed-logo {{
        position: fixed;
        top: 60px;      /* Moved lower for full visibility */
        left: 40px;     /* Small buffer from edge */
        z-index: 1000;
    }}
    </style>

    <div class="fixed-logo">
        <a href="https://youngaspiringthinkers.org" target="_blank">
            <img src="data:image/png;base64,{logo_base64}" width="180">
        </a>
    </div>
""", unsafe_allow_html=True)



# Add top and left padding to the main app content to avoid logo overlap
# Add padding to avoid overlap with fixed logo
st.markdown("""
    <style>
    section.main > div:first-child {
        padding-top: 90px;
        padding-left: 20px;
    }
    </style>
""", unsafe_allow_html=True)



st.markdown("""
    <style>
    /* === Input border override === */
    div[data-baseweb="select"] > div {
        border: 1px solid #4CAF50 !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"]:focus-within > div {
        border: 2px solid #388E3C !important;
    }

    .stMultiSelect [data-baseweb="tag"] {
        background-color: #C8E6C9 !important;
        color: black !important;
    }

    /* === Button style (normal + hover + active) === */
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px;
    }

    .stButton > button:hover {
        background-color: #45a049 !important;
        color: white !important;
    }

    .stButton > button:active {
        background-color: #388E3C !important;
        color: white !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)


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

st.write("Don’t know your interests yet? Take the assessment:")

if st.button("🧠 Take Interest Assessment"):
    st.switch_page("pages/Interest.py") 

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


st.write("Don’t know your skills yet? Take the assessment:")

if st.button("🧠 Take Skill Assessment"):
    st.switch_page("pages/Skill.py") 

education = st.selectbox(
    "What is your current education level?",
    ["Grade 10", "Grade 11", "Grade 12", "Post-matric / University"]
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

    except Exception as e:
        st.error(f"Error generating career suggestion: {e}")

# st.markdown("---")
# st.markdown("📣 We'd love your feedback to improve this tool!")

# st.markdown(
#     "[Fill out our quick feedback form](https://forms.gle/pGLd1D5WeZcvE8GS7)",
#     unsafe_allow_html=True
# )
# === Show feedback prompt after recommendations ===
st.markdown("---")

st.markdown(
    """
    <div style="padding: 1rem; background-color: #f0f8ff; border-left: 4px solid #4CAF50; border-radius: 8px; font-size: 0.95rem;">
        <h4 style="margin-top: 0; font-size: 1rem;">📣 We'd love your feedback!</h4>
        <p style="margin-bottom: 0.5rem;">Help us improve the tool by sharing your thoughts.</p>
        <a href="https://forms.gle/6ikb3Ubmy31CbNyS8" target="_blank" style="color: #1a73e8; font-weight: bold;">
            Fill out our quick feedback form
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

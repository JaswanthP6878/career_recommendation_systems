# app.py
import os, json
import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer
from PIL import Image
#import base64
from bs4 import BeautifulSoup
import pandas as pd

UseOpenAi = True
for key in ["skills", "interests"]:
    if f"selected_{key}" not in st.session_state:
        st.session_state[f"selected_{key}"] = []

# === Load Karrierewege model ===
@st.cache_resource
def load_model():
    model_name = "ElenaSenger/career-path-representation-mpnet-karrierewege"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

def runRecommender():
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
            recommending_job = []
            for i in top_indices:
                st.write(
                    f"• {candidate_jobs[i]} "
                    f"(Score: {similarities[i]:.2f})"
                )
                recommending_job.append(candidate_jobs[i])
            
            st.session_state["recommending_jobs"] = recommending_job

            with open("Data/kenya_research.html", "r", encoding="utf-8") as f:
                html = f.read()

            soup = BeautifulSoup(html, "html.parser")
            career_data = soup.get_text(separator="\n")

            prompt = f"""
                Student Profile:
                Interests: {', '.join(interests)}
                Skills: {', '.join(skills)}
                Education: {education}

                Recommended Job:
                {starting_job} and {recommending_job}

                Career Database:
                {career_data}

                Using the Career Database:

                1. Identify skill gaps between the student and the recommended job.
                2. List skills the student should learn.
                3. Suggest relevant universities, colleges, or training providers.
                4. List any open opportunities mentioned in the database.
                5. Explain why each recommendation is relevant.

                CRITICAL REQUIREMENT: You must output ONLY a valid JSON object. Do not include any conversational text, markdown formatting blocks (like ```json), introduction, or wrap-up commentary. Start your response with "{" and end it with "}".

                The JSON must follow this exact schema structure:

                {{
                "skill_gaps": [
                    {{
                    "gap": "string (The name of the skill category)",
                    "description": "string (Detailed explanation of what the student lacks)"
                    }}
                ],
                "skills_to_learn": [
                    {{
                    "skill": "string (Must match the exact 'gap' name from above)",
                    "details": "string (Actionable advice on what technical tools or concepts to study)"
                    }}
                ],
                "recommended_institutions": [
                    {{
                    "institution": "string (Full name of the university or training center)",
                    "type": "string (e.g., Public University, Private University, Online Bootcamp)",
                    "relevance": "string (Specific reason why this institution fixes the gap)"
                    }}
                ],
                "open_opportunities": [
                    {{
                    "employer_or_sector": "string (Target companies or industry sectors)",
                    "details": "string (Context on why they are hiring for this skillset)"
                    }}
                ]
                }}
            """

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
            print(response)
            st.session_state["response"] = starting_job

            return 0

    except Exception as e:
        st.error(f"Error generating career suggestion: {e}")


st.markdown(
    "<h1 style='text-align: left;'>🎓 Career Path Recommender</h1>",
    unsafe_allow_html=True
)

if "recommending_jobs" not in st.session_state:
    showForm = True
else:
    showForm = False

if showForm:
    st.write("Answer a few questions to get a personalized career suggestion!")

    # === Inputs ===
    interests = st.multiselect(
        "What are your interests?",
        ["Entrepreneurship", "Information Technology (IT)", "Business", "Healthcare", "Engineering", "Media", "Agriculture", "Finance", "AI", 
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
    ## === If user submits ===
    if submit:
        if runRecommender() == 0:
            st.rerun()

else:
    st.write("🔮 **Top Recommended Career Paths:**")
    for job in st.session_state["recommending_jobs"]:
        st.write(
            f"• {job} "
        )
    if "response" in st.session_state:
        with st.spinner("Analyzing profile and career databases..."):
            try:
                raw_text = st.session_state.response
                
                # 2. Defensive JSON Cleaning
                # Sometimes models bypass instructions and wrap text in markdown blocks anyway.
                if raw_text.startswith("```json"):
                    raw_text = raw_text.replace("```json", "", 1)
                elif raw_text.startswith("```"):
                    raw_text = raw_text.replace("```", "", 1)
                if raw_text.endswith("```"):
                    raw_text = raw_text.rsplit("```", 1)[0]
                    
                raw_text = raw_text.strip()

                # 3. Parse the clean string into a Python Dictionary
                data = json.loads(raw_text)
                
                # --- Streamlit Display UI ---
                st.success("Analysis Complete!")
                st.markdown("---")
                
                # Section 1: Merged Skills and Gaps Table
                st.subheader("🎯 Skill Gaps & What to Learn")
                if data.get("skill_gaps") and data.get("skills_to_learn"):
                    df_gaps = pd.DataFrame(data["skill_gaps"])
                    df_skills = pd.DataFrame(data["skills_to_learn"])
                    
                    # Merge dataframes together on the skill/gap category name
                    df_merged = pd.merge(df_gaps, df_skills, left_on="gap", right_on="skill").drop(columns=["skill"])
                    df_merged.columns = ["Skill Category", "Current Gap Description", "Action Plan / What to Study"]
                    
                    st.dataframe(df_merged, width="stretch", hide_index=True)
                else:
                    st.info("No major skill gaps identified.")

                st.markdown("---")

                # Section 2: Recommended Institutions Table
                st.subheader("🏛️ Recommended Training Institutions")
                if data.get("recommended_institutions"):
                    df_inst = pd.DataFrame(data["recommended_institutions"])
                    df_inst.columns = ["Institution / Provider", "Type", "Strategic Relevance"]
                    
                    st.dataframe(df_inst, width="stretch", hide_index=True)
                else:
                    st.info("No specific institutions recommended.")

                st.markdown("---")

                # Section 3: Open Market Opportunities
                st.subheader("💼 Active Market Opportunities")
                if data.get("open_opportunities"):
                    for opp in data["open_opportunities"]:
                        with st.expander(f"📌 {opp.get('employer_or_sector', 'Target Sector')}", expanded=True):
                            st.write(opp.get('details', 'No details provided.'))
                else:
                    st.info("No direct opportunities found in the current database tracking period.")

            except json.JSONDecodeError as je:
                st.error("Could not parse the AI output into a clean table structure.")
                with st.expander("See Raw Output"):
                    st.code(je.text)
                    st.caption(f"Error details: {str(je)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")


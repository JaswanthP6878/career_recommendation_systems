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

for key, val in {
    "accommodation_needed": None,
    "accommodation_types": [],
    "accommodation_other": "",
    "accommodation_denied": None,
    "accommodation_denied_reason": "",
    "accommodation_completed": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


def get_accommodation_summary():
    if not st.session_state.get("accommodation_completed"):
        return "Not specified"
    needed = st.session_state.get("accommodation_needed", "Not specified")
    if needed == "No":
        return "No accommodations needed"
    types = st.session_state.get("accommodation_types", []).copy()
    other = st.session_state.get("accommodation_other", "")
    if "Other" in types and other:
        types[types.index("Other")] = f"Other ({other})"
    parts = [f"Needs accommodations: {needed}"]
    if types:
        parts.append(f"Requested: {', '.join(types)}")
    return "; ".join(parts)

# === Load Karrierewege model ===
@st.cache_resource
def load_model():
    model_name = "ElenaSenger/career-path-representation-mpnet-karrierewege"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

def runRecommender():
    accommodation_summary = get_accommodation_summary()
    accom_needed = st.session_state.get("accommodation_needed")
    accom_types = st.session_state.get("accommodation_types", [])
    has_accommodations = accom_needed in ("Yes", "Not sure") and bool(accom_types)

    # === Step 1: Generate starting job using OpenAI/Gemini ===
    if has_accommodations:
        accom_constraint = (
            f"Accommodation needs: {accommodation_summary}\n"
            f"    IMPORTANT: Suggest a job that is realistic for someone with these needs. "
            f"Prefer roles that commonly offer remote work, flexible hours, low-stimulation "
            f"environments, or assistive-technology-friendly workplaces — whichever match: "
            f"{', '.join(accom_types)}."
        )
    else:
        accom_constraint = ""

    prompt = f"""
    Based on the following student profile, suggest one starting job they could pursue after school
    (e.g., IT Assistant, Lab Technician, Sales Trainee). Be concise.

    Interests: {', '.join(interests)}
    Skills: {', '.join(skills)}
    Education: {education}
    {accom_constraint}
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

            accom_directive = ""
            if has_accommodations:
                accom_directive = f"""
                IMPORTANT — ACCOMMODATION REQUIREMENTS:
                The student requires: {', '.join(accom_types)}
                You MUST address accommodations for EVERY institution and EVERY opportunity:
                - For each institution: state specifically whether it offers support for the student's needs, or write "Not confirmed".
                - For each opportunity: note whether the employer/sector is known for inclusive hiring, remote-friendly roles, or flexible arrangements that match the student's needs, or write "Not confirmed".
                Do not skip this — it is a mandatory part of every recommendation.
                """

            prompt = f"""
                Student Profile:
                Accommodation needs: {accommodation_summary}
                Interests: {', '.join(interests)}
                Skills: {', '.join(skills)}
                Education: {education}
                {accom_directive}
                Recommended Job:
                {starting_job} and {recommending_job}

                Career Database:
                {career_data}

                Using the Career Database:

                1. Identify skill gaps between the student and the recommended job.
                2. List skills the student should learn.
                3. Suggest relevant universities, colleges, or training providers. Prefer institutions that support the student's accommodation needs.
                4. List any open opportunities from the database. Prefer employers or sectors with inclusive or flexible work practices.
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
                    "relevance": "string (Specific reason why this institution fixes the gap)",
                    "accommodation_notes": "string (How this institution supports the student's specific accommodation needs, or 'Not confirmed')"
                    }}
                ],
                "open_opportunities": [
                    {{
                    "employer_or_sector": "string (Target companies or industry sectors)",
                    "details": "string (Context on why they are hiring for this skillset)",
                    "accommodation_notes": "string (Known inclusive hiring practices, remote or flexible options that match the student's needs, or 'Not confirmed')"
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
    interest_options = ["Entrepreneurship", "Information Technology (IT)", "Business", "Healthcare", "Engineering", "Media", "Finance", "AI", "Design", "Education"]
    interests = st.multiselect(
        "What are your interests?",
        interest_options,
        default=[v for v in st.session_state["selected_interests"] if v in interest_options]
    )

    if st.session_state["selected_interests"] == []:
        st.write("Don’t know your interests yet? Take the assessment:")

        if st.button("🧠 Take Interest Assessment"):
            st.switch_page("Profile/Interest.py") 

    # -----------------------------------
    # Skill Options
    # -----------------------------------

    skill_options = [
        "Analytical Thinking", "Adaptability", "Leadership",
        "Creative Thinking", "Self-awareness", "Tech Literacy",
        "Communication", "Project Management", "Research",
        "Financial Literacy",
    ]

    # -----------------------------------
    # Multiselect
    # -----------------------------------

    skills = st.multiselect(
        "What skills do you have?",
        skill_options,
        default=[v for v in st.session_state["selected_skills"] if v in skill_options]
    )

    if st.session_state["selected_skills"] == []:
        st.write("Don’t know your skills yet? Take the assessment:")

        if st.button("🧠 Take Skill Assessment"):
            st.switch_page("Profile/Skill.py")

    if not st.session_state.get("accommodation_completed"):
        st.write("Have accommodation needs? Let us know so we can tailor results:")
        if st.button("Accommodation Needs"):
            st.switch_page("Profile/Accommodation.py")

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
                    has_accom_col = "accommodation_notes" in df_inst.columns
                    if has_accom_col:
                        df_inst = df_inst[["institution", "type", "relevance", "accommodation_notes"]]
                        df_inst.columns = ["Institution / Provider", "Type", "Strategic Relevance", "Accommodation Support"]
                    else:
                        df_inst = df_inst[["institution", "type", "relevance"]]
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
                            accom_note = opp.get('accommodation_notes')
                            if accom_note:
                                st.markdown(f"**Accommodation Support:** {accom_note}")
                else:
                    st.info("No direct opportunities found in the current database tracking period.")

                st.markdown("---")
                if st.button("🤖 Talk to Advisor About These Results", use_container_width=True):
                    st.switch_page("Tools/Chatbot.py")

            except json.JSONDecodeError as je:
                st.error("Could not parse the AI output into a clean table structure.")
                with st.expander("See Raw Output"):
                    st.code(je.text)
                    st.caption(f"Error details: {str(je)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")


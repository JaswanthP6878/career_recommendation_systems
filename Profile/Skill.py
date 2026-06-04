import streamlit as st
from src.assessment_engine import run_assessment

questions = {
    1:  "I enjoy solving complex problems by breaking them into smaller parts.",
    2:  "I adapt quickly when plans or situations suddenly change.",
    3:  "I naturally take initiative when working in teams or group settings.",
    4:  "I enjoy generating new ideas or thinking of creative solutions.",
    5:  "I regularly reflect on my strengths, weaknesses, and personal growth.",
    6:  "I feel comfortable learning and using new digital tools or technologies.",
    7:  "I actively listen and try to understand other people's feelings or perspectives.",
    8:  "I feel confident working with numbers, formulas, or calculations.",
    9:  "I enjoy analyzing information to identify patterns or insights.",
    10: "I feel comfortable presenting ideas in front of groups or audiences.",
    11: "I enjoy organizing tasks, timelines, and resources to complete goals.",
    12: "I enjoy investigating topics deeply before making decisions or conclusions.",
    13: "I am interested in understanding investments, budgets, or business financials.",
    14: "I stay calm and productive under pressure or during setbacks.",
    15: "I can quickly learn how to use unfamiliar software or technical systems.",
}

skill_mapping = {
    "Analytical Thinking": [1, 9],
    "Adaptability":        [2, 14],
    "Leadership":          [3],
    "Creative Thinking":   [4],
    "Self-awareness":      [5],
    "Tech Literacy":       [6, 15],
    "Communication":       [7, 10],
    "Project Management":  [11],
    "Research":            [12],
    "Financial Literacy":  [8, 13],
}

run_assessment(
    title="🧠 Skill Assessment",
    questions=questions,
    category_mapping=skill_mapping,
    session_key="skills",
    return_page="Tools/Recommender.py",
    advisor_page="Tools/Chatbot.py"
)

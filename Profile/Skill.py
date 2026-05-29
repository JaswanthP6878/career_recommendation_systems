import streamlit as st
from src.assessment_engine import run_assessment

questions = {
    1: "I enjoy solving complex problems by breaking them into smaller parts.",
    2: "I adapt quickly when plans or situations suddenly change.",
    3: "I naturally take initiative when working in teams or group settings.",
    4: "I enjoy generating new ideas or thinking of creative solutions.",
    5: "I regularly reflect on my strengths, weaknesses, and personal growth.",
    6: "I feel comfortable learning and using new digital tools or technologies.",
    7: "I actively listen and try to understand other people’s feelings or perspectives.",
    8: "I enjoy learning new topics even outside of school or work requirements.",
    9: "I am good at identifying people’s strengths and helping them improve.",
    10: "I enjoy helping customers, clients, or other people solve problems.",
    11: "I enjoy writing code, scripts, or software programs.",
    12: "I feel confident working with numbers, formulas, or calculations.",
    13: "I enjoy analyzing information to identify patterns or insights.",
    14: "I feel comfortable presenting ideas in front of groups or audiences.",
    15: "I enjoy organizing tasks, timelines, and resources to complete goals.",
    16: "I enjoy investigating topics deeply before making decisions or conclusions.",
    17: "I am interested in understanding investments, budgets, or business financials.",
    18: "I stay calm and productive under pressure or during setbacks.",
    19: "I often inspire or motivate others during group activities.",
    20: "I like experimenting with different approaches to solve problems.",
    21: "I actively seek feedback to improve my performance.",
    22: "I can quickly learn how to use unfamiliar software or technical systems.",
    23: "I enjoy interpreting charts, reports, or datasets to support decisions.",
    24: "I can confidently explain complex ideas in a simple and engaging way.",
    25: "I enjoy planning long-term goals and coordinating people or resources effectively."
}

skill_mapping = {
    "Analytical Thinking": [1, 13, 23],
    "Resilience, Flexibility & Agility": [2, 18],
    "Leadership & Social Influence": [3, 19, 25],
    "Creative Thinking": [4, 20],
    "Motivation & Self-awareness": [5, 21],
    "Technological Literacy": [6, 22],
    "Empathy & Active Listening": [7],
    "Curiosity & Lifelong Learning": [8],
    "Talent Management": [9],
    "Service Orientation & Customer Service": [10],
    "Coding": [11],
    "Math": [12],
    "Data Analysis": [13, 23],
    "Public Speaking": [14, 24],
    "Project Management": [15, 25],
    "Research": [16],
    "Financial Modeling": [17]
}

run_assessment(
    title="🧠 Skill Assessment",
    questions=questions,
    category_mapping=skill_mapping,
    session_key="skills",
    return_page="Profile/Recommender.py"
)
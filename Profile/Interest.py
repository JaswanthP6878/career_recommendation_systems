import streamlit as st
from src.assessment_engine import run_assessment

questions = {
    1: "I enjoy solving technical problems using computers, software, or digital tools.",
    2: "I like analyzing data to find patterns, trends, or insights.",
    3: "I am interested in learning how businesses make money and grow.",
    4: "I enjoy helping people improve their health or well-being.",
    5: "I like building, fixing, or designing machines, systems, or structures.",
    6: "I enjoy creating visual content such as graphics, videos, or digital designs.",
    7: "I feel motivated when teaching, mentoring, or explaining concepts to others.",
    8: "I enjoy working with numbers, calculations, and financial records.",
    9: "I am curious about how artificial intelligence and automation work.",
    10: "I enjoy planning, organizing, and managing projects or people.",
    11: "I like working outdoors or in environments connected to nature and land.",
    12: "I am comfortable following detailed rules, standards, and procedures.",
    13: "I enjoy researching problems and finding efficient solutions.",
    14: "I am interested in storytelling, journalism, social media, or entertainment content.",
    15: "I enjoy understanding how goods and services move from one place to another.",
    16: "I am interested in sustainable food production, farming, or environmental management.",
    17: "I like reviewing information carefully to identify errors or inconsistencies.",
    18: "I enjoy working with technology that improves productivity or communication.",
    19: "I prefer work that combines creativity with practical problem-solving.",
    20: "I am interested in how large industrial operations or extraction industries work.",
    21: "I enjoy collaborating with teams to achieve business or operational goals.",
    22: "I feel energized when learning about new technologies and innovations.",
    23: "I am interested in careers that involve caring for or supporting people directly.",
    24: "I enjoy analyzing risks, compliance issues, or financial accuracy.",
    25: "I would enjoy a career that requires continuous learning and adapting to change."
}

career_mapping = {
    "Information Technology (IT)": [1, 9, 18, 22],
    "Business": [3, 10, 21],
    "Healthcare": [4, 12, 23],
    "Engineering": [5, 13, 19, 20],
    "Media": [6, 14],
    "Agriculture": [11, 16],
    "Finance": [2, 3, 8, 24],
    "AI": [1, 2, 9, 13, 18, 22],
    "Design": [6, 19],
    "Education": [7, 23],
    "Audit & Tax": [8, 12, 17, 24],
    "Mining": [11, 20],
    "Transportation & Logistics": [10, 15, 21]
}

run_assessment(
    title="🎯 Career Interest Assessment",
    questions=questions,
    category_mapping=career_mapping,
    session_key="interests",
    return_page="Profile/Recommender.py"
)
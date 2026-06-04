import streamlit as st
from src.assessment_engine import run_assessment

questions = {
    1:  "I am driven to start my own ventures, build brands, or launch new products from scratch.",
    2:  "I enjoy designing, managing, and troubleshooting computer networks, databases, or cloud infrastructure.",
    3:  "I like analyzing corporate strategies, market trends, and how organizations scale efficiently.",
    4:  "I am deeply interested in medical science, patient care, and improving clinical health outcomes.",
    5:  "I enjoy applying math and physics principles to design physical infrastructure, machinery, or structural components.",
    6:  "I am passionate about public relations, journalism, digital storytelling, and content creation.",
    7:  "I enjoy evaluating investment strategies, managing capital portfolios, and studying stock or money markets.",
    8:  "I am fascinated by building deep learning architectures, neural networks, and training computer vision models.",
    9:  "I love crafting visual layouts, prototyping product interfaces, or developing branding aesthetics.",
    10: "I enjoy developing academic curricula, lecturing, or creating instructional training modules.",
    11: "I am highly comfortable taking calculated financial risks to turn an innovative idea into a commercial reality.",
    12: "I enjoy writing code, building software applications, or customizing technical systems for clients.",
    13: "I prefer working in clinical, hospital, or wellness environments supporting community healthcare delivery.",
    14: "I excel at analyzing complex datasets, building corporate financial models, and tracking macroeconomic trends.",
    15: "I want to specialize in Natural Language Processing (NLP), predictive analytics, and automated workflow systems.",
}

career_mapping = {
    "Entrepreneurship":            [1, 11],
    "Information Technology (IT)": [2, 12],
    "Business":                    [3],
    "Healthcare":                  [4, 13],
    "Engineering":                 [5],
    "Media":                       [6],
    "Finance":                     [7, 14],
    "AI":                          [8, 15],
    "Design":                      [9],
    "Education":                   [10],
}

run_assessment(
    title="🎯 Career Interest Assessment",
    questions=questions,
    category_mapping=career_mapping,
    session_key="interests",
    return_page="Tools/Recommender.py",
    advisor_page="Tools/Chatbot.py"
)

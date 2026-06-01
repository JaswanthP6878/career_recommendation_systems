import streamlit as st
from src.assessment_engine import run_assessment

questions = {
1: "I am driven to start my own ventures, build brands, or launch new products from scratch.",
    2: "I enjoy designing, managing, and troubleshooting computer networks, databases, or cloud infrastructure.",
    3: "I like analyzing corporate strategies, market trends, and how organizations scale efficiently.",
    4: "I am deeply interested in medical science, patient care, and improving clinical health outcomes.",
    5: "I enjoy applying math and physics principles to design physical infrastructure, machinery, or structural components.",
    6: "I am passionate about public relations, journalism, digital storytelling, and content creation.",
    7: "I find fulfillment in breeding livestock, cultivating crops, or studying sustainable agronomy systems.",
    8: "I enjoy evaluating investment strategies, managing capital portfolios, and studying stock or money markets.",
    9: "I am fascinated by building deep learning architectures, neural networks, and training computer vision models.",
    10: "I love crafting visual layouts, prototyping product interfaces, or developing branding aesthetics.",
    11: "I enjoy developing academic curricula, lecturing, or creating instructional training modules.",
    12: "I like examining corporate ledgers, ensuring regulatory compliance, and preparing corporate tax filings.",
    13: "I am interested in geological exploration, mineral extraction techniques, and heavy industrial machinery.",
    14: "I enjoy optimizing supply chain networks, warehouse routing, and the physical movement of global freight.",
    15: "I am highly comfortable taking calculated financial risks to turn an innovative idea into a commercial reality.",
    16: "I enjoy writing code, building software applications, or customizing technical systems for clients.",
    17: "I excel at team leadership, operational management, and optimizing workflow efficiencies in corporate settings.",
    18: "I prefer working in clinical, hospital, or wellness environments supporting community healthcare delivery.",
    19: "I like researching complex technical breakdowns and engineering practical solutions for real-world equipment.",
    20: "I am drawn to careers in broadcast media, entertainment networks, or running large-scale social media campaigns.",
    21: "I want to work with precision agricultural technology, smart irrigation, or large-scale food production operations.",
    22: "I excel at analyzing complex datasets, building corporate financial models, and tracking macroeconomic trends.",
    23: "I want to specialize in Natural Language Processing (NLP), predictive analytics, and automated workflow systems.",
    24: "I enjoy human-centered design, industrial product styling, or creating digital animations and graphics.",
    25: "I feel energized when mentoring others, designing corporate training programs, or simplifying complex ideas.",
    26: "I have a high attention to detail when looking for reporting errors, financial discrepancies, or fraudulent entries.",
    27: "I am comfortable working with heavy resource extraction systems, safety regulations, and environmental impact data.",
    28: "I enjoy managing fleet logistics, dispatch operations, and coordinate complex multi-modal transportation."
}

career_mapping = {
    "Entrepreneurship": [1, 15, 3],               # Shared focus on scaling business
    "Information Technology (IT)": [2, 16, 19],
    "Business": [3, 17, 15],                      # Overlaps with entrepreneurial execution
    "Healthcare": [4, 18, 25],                    # Shared with education/coaching element
    "Engineering": [5, 19, 13],                   # Crosses into infrastructure and mining
    "Media": [6, 20, 10],                         # Connects heavily to design
    "Agriculture": [7, 21, 14],                   # Links to logistical distribution
    "Finance": [8, 22, 3],                        # Links to corporate strategic planning
    "AI": [9, 23, 16],                            # Strongly linked to advanced software engineering
    "Design": [10, 24, 5],                        # Structural engineering design crossover
    "Education": [11, 25, 18],                    # Shared caregiving/support trait
    "Audit & Tax": [12, 26, 8],                   # Shared mathematical analysis
    "Mining": [13, 27, 5],                        # Shared mechanical/civil engineering alignment
    "Transportation & Logistics": [14, 28, 17]    # Shared corporate operations focus
}

run_assessment(
    title="🎯 Career Interest Assessment",
    questions=questions,
    category_mapping=career_mapping,
    session_key="interests",
    return_page="Tools/Recommender.py"
)
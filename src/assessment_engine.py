import streamlit as st
#import pandas as pd


def run_assessment(title, questions, category_mapping, session_key, return_page="Tools/Recommender.py"):
    """
    Reusable Streamlit assessment engine.

    Parameters
    ----------
    title : str
        Assessment title.

    questions : dict
        {question_number: question_text}

    category_mapping : dict
        {
            "Category Name": [question_numbers]
        }

    session_key : str
        Unique identifier for session state.

    return_page : str
        Page to return to after assessment.
    """

    # -----------------------------------
    # Page Header
    # -----------------------------------

    st.title(title)

    # -----------------------------------
    # Response Scale — emoji labels from mockup design
    # -----------------------------------

    response_scale = {
        "😄 Strongly Agree": 5,
        "🙂 Agree": 4,
        "😐 Neutral": 3,
        "🙁 Disagree": 2,
        "😖 Strongly Disagree": 1,
    }

    # -----------------------------------
    # Session Keys
    # -----------------------------------

    question_index_key = f"{session_key}_question_index"
    responses_key = f"{session_key}_responses"
    results_key = f"{session_key}_results"
    top5_key = f"{session_key}_top5"
    completed_key = f"{session_key}_completed"

    # -----------------------------------
    # Initialize Session State
    # -----------------------------------

    if question_index_key not in st.session_state:
        st.session_state[question_index_key] = 1

    if responses_key not in st.session_state:
        st.session_state[responses_key] = {}

    if completed_key not in st.session_state:
        st.session_state[completed_key] = False

    # -----------------------------------
    # Show Results Screen
    # -----------------------------------

    if st.session_state[completed_key]:

        st.success("✅ Assessment Complete!")
        st.subheader("🏆 Your Top 5 Results")

        for i, (category, score) in enumerate(st.session_state[top5_key], start=1):
            with st.container(border=True):
                col_name, col_score = st.columns([3, 1])
                col_name.markdown(f"**{i}. {category}**")
                col_score.markdown(f"**{score}%**")
                st.progress(score / 100)

        if st.button("⬅ Return"):
            st.switch_page(return_page)

        return

    # -----------------------------------
    # Current Question
    # -----------------------------------

    q_num = st.session_state[question_index_key]
    q_text = questions[q_num]

    # -----------------------------------
    # Progress Bar
    # -----------------------------------

    progress = q_num / len(questions)

    st.progress(progress)
    st.caption(f"Question {q_num} of {len(questions)}")

    st.markdown(f"### {q_text}")

    existing_answer = st.session_state[responses_key].get(q_num)

    current_response = st.radio(
        "Response",
        options=list(response_scale.keys()),
        index=(
            list(response_scale.keys()).index(existing_answer)
            if existing_answer else None
        ),
        key=f"{session_key}_question_{q_num}",
        label_visibility="collapsed",
    )

    # -----------------------------------
    # Navigation Buttons
    # -----------------------------------

    col1, col2 = st.columns(2)

    # Previous Button
    with col1:
        if q_num > 1:
            if st.button("⬅ Previous"):
                st.session_state[question_index_key] -= 1
                st.rerun()

    # Next / Submit Button
    with col2:
        # -----------------------------------
        # Next Question
        # -----------------------------------
        if q_num < len(questions):
            if st.button("Next ➡"):
                if current_response is None:
                    st.warning("Please select an answer.")
                else:
                    st.session_state[responses_key][q_num] = current_response
                    st.session_state[question_index_key] += 1
                    st.rerun()

        # -----------------------------------
        # Submit Assessment
        # -----------------------------------
        else:
            if st.button("🚀 Submit Assessment"):
                if current_response is None:
                    st.warning("Please select an answer.")
                else:
                    st.session_state[responses_key][q_num] = current_response

                    # -------------------------
                    # Convert to Numeric
                    # -------------------------
                    numeric_responses = {
                        q: response_scale[r]
                        for q, r in st.session_state[
                            responses_key
                        ].items()
                    }

                    # -------------------------
                    # Calculate Scores
                    # -------------------------
                    results = {}
                    for category, q_list in category_mapping.items():
                        raw_score = sum(
                            numeric_responses[q]
                            for q in q_list
                        )
                        max_score = len(q_list) * 5

                        normalized_score = round((raw_score / max_score) * 100,2)

                        results[category] = normalized_score

                    # -------------------------
                    # Sort Results
                    # -------------------------
                    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

                    top_5 = sorted_results[:5]

                    # -------------------------
                    # Save Results
                    # -------------------------
                    st.session_state[results_key] = sorted_results

                    st.session_state[top5_key] = top_5

                    # IMPORTANT:
                    # Auto-fill support
                    st.session_state[f"selected_{session_key}"] = [category for category, score in top_5]

                    st.session_state[completed_key] = True

                    st.rerun()
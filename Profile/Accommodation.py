import streamlit as st

RETURN_PAGE = "Tools/Recommender.py"
ADVISOR_PAGE = "Tools/Chatbot.py"

ACCOMMODATION_OPTIONS = [
    "Flexible deadlines or work hours",
    "Sign language interpreter",
    "Accessible learning materials (large print, braille, audio)",
    "Captions for videos or meetings",
    "Quiet or reduced-stimulation workspace",
    "Modified tasks or workload",
    "Assistive technology or software",
    "Physical access changes (ramps, seating)",
    "Remote participation options",
    "Mental health or psychosocial support",
    "Other",
]

st.title("♿ Accommodation Needs")
st.caption("Your responses help us find opportunities and institutions that meet your needs.")

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

# --- Completion screen ---
if st.session_state["accommodation_completed"]:
    st.success("✅ Accommodation profile saved!")

    with st.container(border=True):
        st.subheader("Your Responses")
        st.write(f"**Needs accommodations:** {st.session_state['accommodation_needed']}")
        if st.session_state["accommodation_types"]:
            types = st.session_state["accommodation_types"].copy()
            if "Other" in types and st.session_state["accommodation_other"]:
                types[types.index("Other")] = f"Other ({st.session_state['accommodation_other']})"
            st.write(f"**Requested accommodations:** {', '.join(types)}")
        st.write(f"**Previously denied:** {st.session_state['accommodation_denied']}")
        if st.session_state["accommodation_denied_reason"]:
            st.write(f"**Reason given:** {st.session_state['accommodation_denied_reason']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Career Recommendations", use_container_width=True):
            st.switch_page(RETURN_PAGE)
    with col2:
        if st.button("🤖 Talk to Advisor", use_container_width=True):
            st.switch_page(ADVISOR_PAGE)

    if st.button("✏️ Edit Responses"):
        st.session_state["accommodation_completed"] = False
        st.rerun()

    st.stop()

# --- Q1 ---
st.markdown("### 1. Do you need any accommodations to fully take part in education or work?")
q1_options = ["Yes", "No", "Not sure"]
q1 = st.radio(
    "q1",
    options=q1_options,
    index=q1_options.index(st.session_state["accommodation_needed"])
    if st.session_state["accommodation_needed"] in q1_options else None,
    label_visibility="collapsed",
)

# --- Q2 + Q3 (conditional on Q1) ---
q2 = []
q3 = ""
if q1 in ("Yes", "Not sure"):
    st.markdown("---")
    st.markdown("### 2. What accommodations would help you?")
    st.caption("Select all that apply")
    q2 = st.multiselect(
        "q2",
        options=ACCOMMODATION_OPTIONS,
        default=[v for v in st.session_state["accommodation_types"] if v in ACCOMMODATION_OPTIONS],
        label_visibility="collapsed",
    )

    if "Other" in q2:
        st.markdown("### 3. Please specify your other accommodation need:")
        q3 = st.text_input(
            "q3",
            value=st.session_state["accommodation_other"],
            label_visibility="collapsed",
            placeholder="Describe your accommodation need...",
        )

# --- Q4 ---
st.markdown("---")
st.markdown("### 4. Have you ever asked for accommodations and not received them?")
q4_options = ["Yes", "No", "Prefer not to say"]
q4 = st.radio(
    "q4",
    options=q4_options,
    index=q4_options.index(st.session_state["accommodation_denied"])
    if st.session_state["accommodation_denied"] in q4_options else None,
    label_visibility="collapsed",
)

# --- Q5 (conditional on Q4) ---
q5 = ""
if q4 == "Yes":
    st.markdown("### 5. Please specify the main reason given:")
    q5 = st.text_input(
        "q5",
        value=st.session_state["accommodation_denied_reason"],
        label_visibility="collapsed",
        placeholder="Describe the reason...",
    )

# --- Save ---
st.markdown("---")
if st.button("💾 Save Responses", use_container_width=True):
    if q1 is None:
        st.warning("Please answer question 1.")
    elif q4 is None:
        st.warning("Please answer question 4.")
    else:
        st.session_state["accommodation_needed"] = q1
        st.session_state["accommodation_types"] = q2
        st.session_state["accommodation_other"] = q3
        st.session_state["accommodation_denied"] = q4
        st.session_state["accommodation_denied_reason"] = q5
        st.session_state["accommodation_completed"] = True
        st.rerun()

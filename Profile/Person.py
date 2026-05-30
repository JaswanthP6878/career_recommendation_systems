import streamlit as st

african_locations = [
    "Nigeria", "Ethiopia", "Egypt", "Democratic Republic of the Congo",
    "Tanzania", "South Africa", "Kenya", "Uganda", "Sudan", "Algeria",
    "Morocco", "Ghana", "Mozambique", "Madagascar", "Cameroon", "Côte d'Ivoire",
    "Niger", "Burkina Faso", "Mali", "Malawi",
    ]

educations_list = ["Grade 10", "Grade 11", "Grade 12", "Post-matric / University"]

st.title("👤 My Info")

# -----------------------------------
# Initialize Session State
# -----------------------------------

defaults = {
    "name": "Brian Mwangi",
    "gender": "Male",
    "age": 16,
    "education": "Grade 10",
    "location": "Kenya",
    "edit_profile": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------------
# View Mode
# -----------------------------------

if not st.session_state.edit_profile:

    with st.container(border=True):
        st.subheader("Personal Information")

        st.write(f"**Name:** {st.session_state.name}")
        st.write(f"**Gender:** {st.session_state.gender}")
        st.write(f"**Age:** {st.session_state.age}")
        st.write(f"**Education:** {st.session_state.education}")
        st.write(f"**Location:** {st.session_state.location}")

    if st.button("✏️ Update Profile"):
        st.session_state.edit_profile = True
        st.rerun()

# -----------------------------------
# Edit Mode
# -----------------------------------

else:

    st.subheader("Update Your Profile")

    with st.form("profile_form"):

        name = st.text_input(
            "Name",
            value=st.session_state.name
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other", "Prefer not to say"],
            index=[
                "Male",
                "Female",
                "Other",
                "Prefer not to say"
            ].index(st.session_state.gender)
        )

        age = st.number_input(
            "Age",
            min_value=6,
            max_value=30,
            value=st.session_state.age
        )

        education = st.selectbox(
            "Education",
            educations_list,
            index = educations_list.index(st.session_state.education)
        )

        location = st.selectbox(
            "Location",
            african_locations,
            index=african_locations.index(st.session_state.location)
        )

        col1, col2 = st.columns(2)

        with col1:
            save = st.form_submit_button("💾 Save")

        with col2:
            cancel = st.form_submit_button("❌ Cancel")

    # Save Changes
    if save:

        st.session_state.name = name
        st.session_state.gender = gender
        st.session_state.age = age
        st.session_state.education = education
        st.session_state.location = location

        st.session_state.edit_profile = False

        st.success("Profile updated successfully!")
        st.rerun()

    # Cancel Changes
    if cancel:

        st.session_state.edit_profile = False
        st.rerun()
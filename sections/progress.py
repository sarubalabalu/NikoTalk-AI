import streamlit as st


def show_progress():

    if st.button("⬅️ Back to Home", key="progress_back"):
        st.session_state.page = "home"
        st.rerun()

    st.title("📊 My Progress & Score")

    st.write(
        "Your learning progress and scores will appear here."
    )

    st.info(
        "🚧 Progress Dashboard is under development."
    )
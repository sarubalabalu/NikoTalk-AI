import streamlit as st
from data.grammar_data import GRAMMAR
from utils.scoring import calculate_percentage, get_score_message


def show_grammar():

    if "grammar_topic" not in st.session_state:
        st.session_state.grammar_topic = list(GRAMMAR.keys())[0]

    if "grammar_question" not in st.session_state:
        st.session_state.grammar_question = 0

    if "grammar_score" not in st.session_state:
        st.session_state.grammar_score = 0

    if "grammar_answered" not in st.session_state:
        st.session_state.grammar_answered = False

    if "grammar_selected_answer" not in st.session_state:
        st.session_state.grammar_selected_answer = None

    st.markdown("""
    <div class="hero">
        <div class="hero-title">📖 Grammar Practice</div>
        <div class="hero-text">Learn grammar rules, practice questions, and improve your English.</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Back to Home", key="grammar_home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("## 🎯 Choose a Grammar Topic")

    topic_names = list(GRAMMAR.keys())
    selected_topic = st.selectbox(
        "Select a grammar topic:",
        topic_names,
        index=topic_names.index(st.session_state.grammar_topic),
        key="grammar_topic_select"
    )

    if selected_topic != st.session_state.grammar_topic:
        st.session_state.grammar_topic = selected_topic
        st.session_state.grammar_question = 0
        st.session_state.grammar_score = 0
        st.session_state.grammar_answered = False
        st.session_state.grammar_selected_answer = None
        st.rerun()

    topic = GRAMMAR[selected_topic]
    questions = topic["questions"]

    st.markdown(
        f"""
        <div style="
            background:{topic['color']};
            border:2px solid {topic['border']};
            border-radius:20px;
            padding:25px;
            margin:20px 0;
        ">
            <h2 style="color:#303451;">{topic['emoji']} {selected_topic}</h2>
            <p style="color:#68718F;font-size:17px;"><b>💡 Explanation:</b> {topic['explanation']}</p>
            <p style="color:#68718F;font-size:17px;"><b>📝 Rule:</b> {topic['rule']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    question_index = st.session_state.grammar_question
    question_data = questions[question_index]

    total_questions = len(questions)
    current_number = question_index + 1

    st.markdown(f"### ❓ Question {current_number} of {total_questions}")

    st.markdown(
        f"""
        <div style="
            background:white;
            border:2px solid {topic['border']};
            border-radius:18px;
            padding:25px;
            margin:15px 0;
        ">
            <h3 style="color:#303451;">{question_data['question']}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    options = question_data["options"]

    if not st.session_state.grammar_answered:
        selected = st.radio(
            "Choose your answer:",
            options,
            key=f"grammar_option_{selected_topic}_{question_index}"
        )

        if st.button("🎯 Check Answer", key=f"grammar_check_{selected_topic}_{question_index}"):
            st.session_state.grammar_selected_answer = selected
            st.session_state.grammar_answered = True

            if selected == question_data["correct_answer"]:
                st.session_state.grammar_score += 1

            st.rerun()

    else:
        selected = st.session_state.grammar_selected_answer

        if selected == question_data["correct_answer"]:
            st.success("🎉 Correct! Excellent work.")
        else:
            st.error("❌ Not quite. Keep practicing!")

        st.info(f"✅ Correct answer: **{question_data['correct_answer']}**")

        answered = current_number
        percentage = calculate_percentage(st.session_state.grammar_score, answered)

        st.markdown(
            f"""
            <div style="
                background:{topic['color']};
                border-radius:18px;
                padding:20px;
                text-align:center;
                margin:20px 0;
            ">
                <h3 style="color:#303451;">📊 Current Score</h3>
                <h2 style="color:#303451;">
                    {st.session_state.grammar_score} / {answered}
                </h2>
                <p style="color:#68718F;font-size:18px;">{percentage}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if question_index < total_questions - 1:
            if st.button("➡️ Next Question", key=f"grammar_next_{selected_topic}_{question_index}"):
                st.session_state.grammar_question += 1
                st.session_state.grammar_answered = False
                st.session_state.grammar_selected_answer = None
                st.rerun()
        else:
            final_percentage = calculate_percentage(
                st.session_state.grammar_score,
                total_questions
            )

            st.success(
                f"🏁 Topic completed! "
                f"Your score is {st.session_state.grammar_score}/{total_questions} "
                f"({final_percentage}%). "
                f"{get_score_message(final_percentage)}"
            )

            if st.button("🔄 Practice This Topic Again", key=f"grammar_restart_{selected_topic}"):
                st.session_state.grammar_question = 0
                st.session_state.grammar_score = 0
                st.session_state.grammar_answered = False
                st.session_state.grammar_selected_answer = None
                st.rerun()

import streamlit as st

from data.english_rules_data import ENGLISH_RULES
from utils.scoring import calculate_percentage, get_score_message


CREAM = "#F5E1A6"
MINT = "#6ECDB9"
LAVENDER = "#C5B3E3"
DARK = "#303451"
TEXT = "#68718F"


def _prepare_questions():
    questions = []

    for topic_name, topic_data in ENGLISH_RULES.items():
        for question in topic_data.get("questions", []):
            item = question.copy()
            item["topic"] = topic_name
            item["topic_emoji"] = topic_data.get("emoji", "📋")
            item["topic_color"] = topic_data.get("color", "#FFF9E8")
            item["topic_border"] = topic_data.get("border", CREAM)
            questions.append(item)

    return questions


def show_english_rules():

    if "english_rule_index" not in st.session_state:
        st.session_state.english_rule_index = 0

    if "english_rule_answers" not in st.session_state:
        st.session_state.english_rule_answers = {}

    # --------------------------------------------------
    # PAGE STYLES
    # --------------------------------------------------

    st.html(
        f"""
        <style>
            .rules-hero {{
                background-color: {CREAM};
                border-radius: 25px;
                padding: 40px 30px;
                text-align: center;
                margin-bottom: 30px;
            }}

            .rules-card {{
                border-radius: 22px;
                padding: 30px;
                margin: 20px 0;
            }}

            .example-box {{
                background-color: white;
                border-radius: 18px;
                padding: 20px;
                margin-top: 20px;
                color: {DARK};
                line-height: 1.8;
            }}

            .quiz-box {{
                background-color: #F4F0FA;
                border: 3px solid {LAVENDER};
                border-radius: 20px;
                padding: 25px;
                margin-top: 20px;
            }}

            .score-box {{
                background-color: #EBF8F5;
                border: 3px solid {MINT};
                border-radius: 20px;
                padding: 30px;
                text-align: center;
                margin-top: 30px;
            }}
        </style>
        """
    )

    # --------------------------------------------------
    # HERO
    # --------------------------------------------------

    st.html(
        f"""
        <div class="rules-hero">
            <div style="
                font-size:40px;
                font-weight:700;
                color:{DARK};
            ">
                📋 Simple English Rules
            </div>

            <div style="
                font-size:18px;
                color:{DARK};
                margin-top:10px;
            ">
                Learn simple English rules step by step.
            </div>
        </div>
        """
    )

    # --------------------------------------------------
    # BACK TO HOME
    # --------------------------------------------------

    if st.button("⬅️ Back to Home", key="english_rules_back"):
        st.session_state.page = "home"
        st.rerun()

    # --------------------------------------------------
    # PREPARE QUESTIONS
    # --------------------------------------------------

    questions = _prepare_questions()

    if not questions:
        st.warning("No English Rules questions found.")
        return

    total = len(questions)

    if st.session_state.english_rule_index >= total:
        st.session_state.english_rule_index = total - 1

    if st.session_state.english_rule_index < 0:
        st.session_state.english_rule_index = 0

    index = st.session_state.english_rule_index
    question_data = questions[index]

    question_id = str(question_data["id"])

    # --------------------------------------------------
    # SCORE
    # --------------------------------------------------

    score = 0
    answered = 0

    for item in questions:
        item_id = str(item["id"])

        if item_id in st.session_state.english_rule_answers:
            answered += 1

            if (
                st.session_state.english_rule_answers[item_id]
                == item["correct_answer"]
            ):
                score += 1

    st.success(
        f"📋 English Rules | 📊 Score: {score}/{total} | "
        f"✅ Answered: {answered}/{total}"
    )

    # --------------------------------------------------
    # TOPIC
    # --------------------------------------------------

    st.html(
        f"""
        <h2 style="
            color:{DARK};
            margin-bottom:5px;
        ">
            {question_data["topic_emoji"]} {question_data["topic"]}
        </h2>

        <p style="
            color:{TEXT};
            font-size:17px;
            margin-top:0;
        ">
            Question {index + 1} of {total}
        </p>
        """
    )

    st.progress((index + 1) / total)

    # --------------------------------------------------
    # RULE CARD
    # --------------------------------------------------

    topic_color = question_data["topic_color"]
    topic_border = question_data["topic_border"]

    st.html(
        f"""
        <div class="rules-card"
             style="
                background-color:{topic_color};
                border:3px solid {topic_border};
             ">

            <div style="
                color:{TEXT};
                font-size:15px;
                margin-bottom:10px;
            ">
                English Rule
            </div>

            <div style="
                font-size:26px;
                font-weight:700;
                color:{DARK};
            ">
                {question_data["rule"]}
            </div>

            <div class="example-box">
                <b>📝 Example:</b><br>
                {question_data["example"]}
            </div>

        </div>
        """
    )

    # --------------------------------------------------
    # QUIZ
    # --------------------------------------------------

    st.html(
        f"""
        <div class="quiz-box">

            <div style="
                font-size:24px;
                font-weight:700;
                color:{DARK};
            ">
                🎯 Quick Quiz
            </div>

            <div style="
                font-size:18px;
                color:{TEXT};
                margin-top:12px;
            ">
                {question_data["question"]}
            </div>

        </div>
        """
    )

    # --------------------------------------------------
    # ANSWER
    # --------------------------------------------------

    saved_answer = st.session_state.english_rule_answers.get(question_id)

    if saved_answer is not None:

        selected_answer = st.radio(
            "Choose the correct answer:",
            question_data["options"],
            index=question_data["options"].index(saved_answer),
            key=f"english_rule_radio_{question_id}"
        )

        if saved_answer == question_data["correct_answer"]:
            st.success("✅ Correct answer!")
        else:
            st.error("❌ Incorrect answer.")
            st.info(
                f"✅ Correct answer: {question_data['correct_answer']}"
            )

        if selected_answer != saved_answer:

            if st.button(
                "💾 Save Changed Answer",
                key=f"english_rule_change_{question_id}",
                use_container_width=True
            ):
                st.session_state.english_rule_answers[question_id] = selected_answer
                st.rerun()

    else:

        selected_answer = st.radio(
            "Choose the correct answer:",
            question_data["options"],
            key=f"english_rule_radio_{question_id}"
        )

        if st.button(
            "🎯 Check Answer",
            key=f"english_rule_check_{question_id}",
            use_container_width=True
        ):
            st.session_state.english_rule_answers[question_id] = selected_answer
            st.rerun()

    # --------------------------------------------------
    # PREVIOUS / NEXT
    # --------------------------------------------------

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if index > 0:
            if st.button(
                "⬅️ Previous Rule",
                key=f"english_rule_previous_{question_id}",
                use_container_width=True
            ):
                st.session_state.english_rule_index -= 1
                st.rerun()

    with col2:
        if index < total - 1:
            if st.button(
                "➡️ Next Rule",
                key=f"english_rule_next_{question_id}",
                use_container_width=True
            ):
                st.session_state.english_rule_index += 1
                st.rerun()

    # --------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------

    if answered == total:

        percentage = calculate_percentage(score, total)
        message = get_score_message(percentage)

        st.html(
            f"""
            <div class="score-box">

                <div style="
                    font-size:30px;
                    font-weight:700;
                    color:{DARK};
                ">
                    🏆 English Rules Completed!
                </div>

                <div style="
                    font-size:25px;
                    margin-top:15px;
                    color:{DARK};
                ">
                    Score: {score}/{total}
                </div>

                <div style="
                    font-size:22px;
                    margin-top:10px;
                    color:{TEXT};
                ">
                    Percentage: {percentage}%
                </div>

                <div style="
                    font-size:22px;
                    margin-top:10px;
                    color:{DARK};
                ">
                    {message}
                </div>

            </div>
            """
        )

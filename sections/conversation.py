import streamlit as st

from data.conversation_data import (
    CONVERSATION_TOPICS,
    CONVERSATION_QUESTIONS
)

from utils.scoring import (
    calculate_percentage,
    get_score_message
)


# =========================================================
# COLORS
# =========================================================

PINK = "#CF93B7"
MINT = "#6ECDB9"
LIGHT_BLUE = "#9BCEEC"
LAVENDER = "#C5B3E3"
CREAM = "#F5E1A6"

DARK = "#303451"
TEXT = "#68718F"


# =========================================================
# SHOW CONVERSATION
# =========================================================

def show_conversation():

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "conversation_topic" not in st.session_state:
        st.session_state.conversation_topic = list(
            CONVERSATION_TOPICS.keys()
        )[0]

    if "conversation_index" not in st.session_state:
        st.session_state.conversation_index = 0

    if "conversation_answers" not in st.session_state:
        st.session_state.conversation_answers = {}


    # =====================================================
    # CSS
    # =====================================================

    st.markdown(
        f"""
        <style>

        .conversation-hero {{
            background-color: {LIGHT_BLUE};
            border-radius: 25px;
            padding: 40px 30px;
            text-align: center;
            margin-bottom: 30px;
        }}

        .conversation-card {{
            background-color: #EEF8FC;
            border: 3px solid {LIGHT_BLUE};
            border-radius: 22px;
            padding: 30px;
            margin: 20px 0;
        }}

        .dialogue-box {{
            background-color: white;
            border-radius: 18px;
            padding: 22px;
            margin-top: 18px;
            color: {DARK};
            line-height: 1.7;
        }}

        .score-box {{
            background-color: #F4F0FA;
            border: 3px solid {LAVENDER};
            border-radius: 20px;
            padding: 28px;
            text-align: center;
            margin-top: 25px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # HERO
    # =====================================================

    st.html(
        f"""
        <div class="conversation-hero">

            <div style="
                font-size:40px;
                font-weight:700;
                color:{DARK};
            ">
                💬 Daily Conversation
            </div>

            <div style="
                font-size:18px;
                color:{DARK};
                margin-top:10px;
            ">
                Practice real-life English conversations step by step.
            </div>

        </div>
        """
    )


    # =====================================================
    # BACK TO HOME
    # =====================================================

    if st.button(
        "⬅️ Back to Home",
        key="conversation_back"
    ):

        st.session_state.page = "home"
        st.rerun()


    # =====================================================
    # TOPIC SELECTION
    # =====================================================

    topic_names = list(CONVERSATION_TOPICS.keys())

    current_topic = st.session_state.conversation_topic

    selected_topic = st.selectbox(
        "🗂️ Choose a conversation topic",
        topic_names,
        index=topic_names.index(current_topic),
        key="conversation_topic_select"
    )


    # If topic changed
    if selected_topic != st.session_state.conversation_topic:

        st.session_state.conversation_topic = selected_topic

        st.session_state.conversation_index = 0

        st.rerun()


    # =====================================================
    # GET QUESTIONS
    # =====================================================

    topic_questions = CONVERSATION_TOPICS[selected_topic]

    total = len(topic_questions)


    # =====================================================
    # CALCULATE SCORE
    # =====================================================

    topic_score = 0
    answered = 0

    for question in topic_questions:

        question_id = str(question["id"])

        answer = st.session_state.conversation_answers.get(
            question_id
        )

        if answer is not None:

            answered += 1

            if answer == question["correct_answer"]:
                topic_score += 1


    # =====================================================
    # SCORE DISPLAY
    # =====================================================

    st.success(
        f"💬 {selected_topic}  |  "
        f"📊 Score: {topic_score}/{total}  |  "
        f"✅ Answered: {answered}/{total}"
    )


    # =====================================================
    # CURRENT QUESTION
    # =====================================================

    index = st.session_state.conversation_index


    # Safety check

    if index >= total:
        index = total - 1
        st.session_state.conversation_index = index


    question = topic_questions[index]

    question_id = str(question["id"])


    # =====================================================
    # QUESTION TITLE
    # =====================================================

    st.markdown(
        f"""
        <h2 style="color:{DARK};">
            🎯 Conversation {index + 1} of {total}
        </h2>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # PROGRESS BAR
    # =====================================================

    st.progress((index + 1) / total)


    # =====================================================
    # QUESTION CARD
    # =====================================================

    st.html(
        f"""
        <div class="conversation-card">

            <div style="
                color:{TEXT};
                font-size:15px;
            ">
                Difficulty: {question["difficulty"]}
            </div>


            <div class="dialogue-box">

                <div style="
                    font-size:20px;
                    font-weight:700;
                    color:{DARK};
                ">
                    👤 Person A:
                </div>


                <div style="
                    font-size:22px;
                    margin-top:8px;
                    color:{DARK};
                ">
                    {question["question"]}
                </div>


                <hr>


                <div style="
                    font-size:18px;
                    color:{TEXT};
                ">
                    💭 What should Person B say?
                </div>

            </div>

        </div>
        """
    )


    # =====================================================
    # CHECK WHETHER ANSWER ALREADY EXISTS
    # =====================================================

    saved_answer = st.session_state.conversation_answers.get(
        question_id
    )


    # =====================================================
    # ANSWER OPTIONS
    # =====================================================

    if saved_answer is not None:

        selected_answer = st.radio(
            "Choose the best reply:",
            question["options"],
            index=question["options"].index(saved_answer),
            key=f"conversation_radio_{question_id}"
        )


        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        if saved_answer == question["correct_answer"]:

            st.success("✅ Correct!")

        else:

            st.error("❌ Incorrect!")

            st.info(
                f"✅ Correct reply: "
                f"{question['correct_answer']}"
            )


        # -------------------------------------------------
        # SHOW CORRECT CONVERSATION
        # -------------------------------------------------

        st.html(
            f"""
            <div class="dialogue-box">

                <b>💬 Conversation</b>

                <br><br>

                <b>Person A:</b>
                {question["question"]}

                <br><br>

                <b>Person B:</b>
                {question["correct_answer"]}

            </div>
            """
        )


        # -------------------------------------------------
        # CHANGE ANSWER
        # -------------------------------------------------

        if selected_answer != saved_answer:

            if st.button(
                "💾 Save Changed Answer",
                key=f"conversation_change_{question_id}",
                use_container_width=True
            ):

                st.session_state.conversation_answers[
                    question_id
                ] = selected_answer

                st.rerun()


    # =====================================================
    # NEW QUESTION
    # =====================================================

    else:

        selected_answer = st.radio(
            "Choose the best reply:",
            question["options"],
            key=f"conversation_radio_{question_id}"
        )


        if st.button(
            "🎯 Check Answer",
            key=f"conversation_check_{question_id}",
            use_container_width=True
        ):

            st.session_state.conversation_answers[
                question_id
            ] = selected_answer

            st.rerun()


    # =====================================================
    # PREVIOUS / NEXT
    # =====================================================

    st.write("")


    col1, col2 = st.columns(2)


    # =====================================================
    # PREVIOUS
    # =====================================================

    with col1:

        if index > 0:

            if st.button(
                "⬅️ Previous Conversation",
                key=f"conversation_previous_{question_id}",
                use_container_width=True
            ):

                st.session_state.conversation_index -= 1

                st.rerun()


    # =====================================================
    # NEXT
    # =====================================================

    with col2:

        if index < total - 1:

            if st.button(
                "➡️ Next Conversation",
                key=f"conversation_next_{question_id}",
                use_container_width=True
            ):

                st.session_state.conversation_index += 1

                st.rerun()


    # =====================================================
    # FINAL SCORE
    # =====================================================

    if answered == total:

        percentage = calculate_percentage(
            topic_score,
            total
        )

        message = get_score_message(
            percentage
        )


        st.html(
            f"""
            <div class="score-box">

                <div style="
                    font-size:30px;
                    font-weight:700;
                    color:{DARK};
                ">
                    🏆 Topic Completed!
                </div>


                <div style="
                    font-size:24px;
                    margin-top:12px;
                    color:{DARK};
                ">
                    Score: {topic_score}/{total}
                </div>


                <div style="
                    font-size:21px;
                    margin-top:8px;
                    color:{TEXT};
                ">
                    Percentage: {percentage}%
                </div>


                <div style="
                    font-size:21px;
                    margin-top:8px;
                    color:{DARK};
                ">
                    {message}
                </div>

            </div>
            """
        )
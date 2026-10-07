import streamlit as st

from data.story_data import STORY_DATA
from utils.scoring import calculate_percentage, get_score_message


CREAM = "#F5E1A6"
MINT = "#6ECDB9"
LAVENDER = "#C5B3E3"
LIGHT_BLUE = "#9BCEEC"
DARK = "#303451"
TEXT = "#68718F"


def show_story_understanding():

    # --------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------

    if "story_index" not in st.session_state:
        st.session_state.story_index = 0

    if "story_question_index" not in st.session_state:
        st.session_state.story_question_index = 0

    if "story_answers" not in st.session_state:
        st.session_state.story_answers = {}

    if "story_selected_story" not in st.session_state:
        st.session_state.story_selected_story = 0


    # --------------------------------------------------
    # PAGE STYLES
    # --------------------------------------------------

    st.html(
        f"""
        <style>

        .story-hero {{
            background-color: {LIGHT_BLUE};
            border-radius: 25px;
            padding: 40px 30px;
            text-align: center;
            margin-bottom: 30px;
        }}

        .story-card {{
            background-color: #F3F9FD;
            border: 3px solid {LIGHT_BLUE};
            border-radius: 22px;
            padding: 30px;
            margin: 20px 0;
        }}

        .question-card {{
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
        <div class="story-hero">

            <div style="
                font-size:40px;
                font-weight:700;
                color:{DARK};
            ">
                📖 Story Understanding
            </div>

            <div style="
                font-size:18px;
                color:{DARK};
                margin-top:10px;
            ">
                Read simple English stories and answer questions.
            </div>

        </div>
        """
    )


    # --------------------------------------------------
    # BACK TO HOME
    # --------------------------------------------------

    if st.button(
        "⬅️ Back to Home",
        key="story_back_home"
    ):
        st.session_state.page = "home"
        st.rerun()


    # --------------------------------------------------
    # CHECK DATA
    # --------------------------------------------------

    if not STORY_DATA:
        st.warning("No stories found.")
        return


    total_stories = len(STORY_DATA)


    # --------------------------------------------------
    # STORY SELECTOR
    # --------------------------------------------------

    st.markdown(
        f"### 📚 Choose a Story",
    )

    story_titles = [
        f"Story {story['id']}: {story['title']}"
        for story in STORY_DATA
    ]

    selected_story = st.selectbox(
        "Select a story to read:",
        range(total_stories),
        format_func=lambda x: story_titles[x],
        index=st.session_state.story_selected_story,
        key="story_selector"
    )

    if selected_story != st.session_state.story_selected_story:

        st.session_state.story_selected_story = selected_story
        st.session_state.story_question_index = 0
        st.session_state.story_answers = {}
        st.rerun()


    story = STORY_DATA[selected_story]


    # --------------------------------------------------
    # STORY INFORMATION
    # --------------------------------------------------

    questions = story.get("questions", [])

    if not questions:
        st.warning("This story does not have any questions.")
        return


    total_questions = len(questions)


    # --------------------------------------------------
    # STORY CARD
    # --------------------------------------------------

    st.html(
        f"""
        <div class="story-card">

            <div style="
                color:{TEXT};
                font-size:15px;
                margin-bottom:10px;
            ">
                Story {story["id"]} of {total_stories}
            </div>

            <div style="
                font-size:30px;
                font-weight:700;
                color:{DARK};
                margin-bottom:20px;
            ">
                📖 {story["title"]}
            </div>

            <div style="
                font-size:18px;
                color:{TEXT};
                line-height:1.9;
            ">
                {story["story"]}
            </div>

        </div>
        """
    )


    # --------------------------------------------------
    # STORY SCORE
    # --------------------------------------------------

    score = 0
    answered = 0

    for i, question in enumerate(questions):

        key = f"{story['id']}_{i}"

        if key in st.session_state.story_answers:

            answered += 1

            if (
                st.session_state.story_answers[key]
                == question["correct_answer"]
            ):
                score += 1


    st.success(
        f"📖 {story['title']} | "
        f"📊 Score: {score}/{total_questions} | "
        f"✅ Answered: {answered}/{total_questions}"
    )


    # --------------------------------------------------
    # QUESTION INDEX
    # --------------------------------------------------

    question_index = st.session_state.story_question_index

    if question_index >= total_questions:
        question_index = total_questions - 1
        st.session_state.story_question_index = question_index


    question = questions[question_index]

    answer_key = f"{story['id']}_{question_index}"


    # --------------------------------------------------
    # QUESTION PROGRESS
    # --------------------------------------------------

    st.html(
        f"""
        <div style="
            color:{DARK};
            font-size:24px;
            font-weight:700;
            margin-top:25px;
        ">
            ❓ Question {question_index + 1} of {total_questions}
        </div>
        """
    )

    st.progress((question_index + 1) / total_questions)


    # --------------------------------------------------
    # QUESTION CARD
    # --------------------------------------------------

    st.html(
        f"""
        <div class="question-card">

            <div style="
                font-size:20px;
                font-weight:700;
                color:{DARK};
            ">
                {question["question"]}
            </div>

        </div>
        """
    )


    # --------------------------------------------------
    # ANSWER
    # --------------------------------------------------

    saved_answer = st.session_state.story_answers.get(answer_key)


    if saved_answer is not None:

        selected_answer = st.radio(
            "Choose the correct answer:",
            question["options"],
            index=question["options"].index(saved_answer),
            key=f"story_radio_{answer_key}"
        )

        if saved_answer == question["correct_answer"]:

            st.success("✅ Correct answer!")

        else:

            st.error("❌ Incorrect answer.")

            st.info(
                f"✅ Correct answer: "
                f"{question['correct_answer']}"
            )


        if selected_answer != saved_answer:

            if st.button(
                "💾 Save Changed Answer",
                key=f"story_change_{answer_key}",
                use_container_width=True
            ):

                st.session_state.story_answers[
                    answer_key
                ] = selected_answer

                st.rerun()


    else:

        selected_answer = st.radio(
            "Choose the correct answer:",
            question["options"],
            key=f"story_radio_{answer_key}"
        )


        if st.button(
            "🎯 Check Answer",
            key=f"story_check_{answer_key}",
            use_container_width=True
        ):

            st.session_state.story_answers[
                answer_key
            ] = selected_answer

            st.rerun()


    # --------------------------------------------------
    # PREVIOUS / NEXT
    # --------------------------------------------------

    st.write("")

    col1, col2 = st.columns(2)


    with col1:

        if question_index > 0:

            if st.button(
                "⬅️ Previous Question",
                key=f"story_previous_{answer_key}",
                use_container_width=True
            ):

                st.session_state.story_question_index -= 1
                st.rerun()


    with col2:

        if question_index < total_questions - 1:

            if st.button(
                "➡️ Next Question",
                key=f"story_next_{answer_key}",
                use_container_width=True
            ):

                st.session_state.story_question_index += 1
                st.rerun()


    # --------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------

    if answered == total_questions:

        percentage = calculate_percentage(
            score,
            total_questions
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
                    🏆 Story Completed!
                </div>

                <div style="
                    font-size:25px;
                    margin-top:15px;
                    color:{DARK};
                ">
                    Score: {score}/{total_questions}
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

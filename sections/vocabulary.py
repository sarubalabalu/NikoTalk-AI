import streamlit as st

from data.vocabulary_data import VOCABULARY
from utils.scoring import calculate_percentage, get_score_message


def show_vocabulary():

    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.html("""
        <div style="
            background-color:#C5B3E3;
            border-radius:25px;
            padding:35px;
            text-align:center;
            margin-bottom:30px;
        ">
            <div style="
                font-size:38px;
                font-weight:700;
                color:#303451;
            ">
                📚 Vocabulary Practice
            </div>

            <div style="
                font-size:17px;
                color:#303451;
                margin-top:10px;
            ">
                Learn useful English words and test your understanding.
            </div>
        </div>
    """)

    # =====================================================
    # BACK TO HOME
    # =====================================================

    if st.button(
        "⬅️ Back to Home",
        key="vocab_back"
    ):
        st.session_state.page = "home"
        st.rerun()

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "vocab_topic" not in st.session_state:
        st.session_state.vocab_topic = list(VOCABULARY.keys())[0]

    if "vocab_index" not in st.session_state:
        st.session_state.vocab_index = 0

    if "vocab_score" not in st.session_state:
        st.session_state.vocab_score = 0

    if "vocab_total" not in st.session_state:
        st.session_state.vocab_total = 0

    if "vocab_answered" not in st.session_state:
        st.session_state.vocab_answered = False

    # =====================================================
    # TOPIC SELECTION
    # =====================================================

    st.subheader("🎯 Choose a Vocabulary Topic")

    topics = list(VOCABULARY.keys())

    selected_topic = st.selectbox(
        "Select a topic:",
        topics,
        index=topics.index(st.session_state.vocab_topic),
        key="topic_selector"
    )

    # =====================================================
    # RESET WHEN TOPIC CHANGES
    # =====================================================

    if selected_topic != st.session_state.vocab_topic:

        st.session_state.vocab_topic = selected_topic
        st.session_state.vocab_index = 0
        st.session_state.vocab_score = 0
        st.session_state.vocab_total = 0
        st.session_state.vocab_answered = False

        st.rerun()

    # =====================================================
    # GET CURRENT TOPIC
    # =====================================================

    topic_data = VOCABULARY[selected_topic]

    words = topic_data["words"]

    total_words = len(words)

    current_index = st.session_state.vocab_index

    current_word = words[current_index]

    # =====================================================
    # PROGRESS
    # =====================================================

    progress = (current_index + 1) / total_words

    st.progress(progress)

    st.write(
        f"**Word {current_index + 1} of {total_words}**"
    )

    # =====================================================
    # WORD CARD
    # =====================================================

    word_color = topic_data["color"]
    border_color = topic_data["border"]
    emoji = topic_data["emoji"]

    word = current_word["word"]
    pronunciation = current_word["pronunciation"]

    st.html(f"""
        <div style="
            background-color:{word_color};
            border:3px solid {border_color};
            border-radius:25px;
            padding:35px;
            text-align:center;
            margin:25px 0;
        ">

            <div style="
                font-size:17px;
                font-weight:600;
                color:#68718F;
                margin-bottom:15px;
            ">
                {emoji} WORD
            </div>

            <div style="
                font-size:42px;
                font-weight:700;
                color:#303451;
                margin-bottom:20px;
            ">
                {word}
            </div>

            <div style="
                font-size:18px;
                color:#303451;
                font-weight:600;
            ">
                🗣️ {pronunciation}
            </div>

        </div>
    """)

    # =====================================================
    # MEANING
    # =====================================================

    st.subheader("📖 Meaning")

    st.write(
        current_word["meaning"]
    )

    # =====================================================
    # EXAMPLES
    # =====================================================

    st.subheader("✍️ Example Sentences")

    st.write(
        f"**1.** {current_word['example1']}"
    )

    st.write(
        f"**2.** {current_word['example2']}"
    )

    # =====================================================
    # QUIZ
    # =====================================================

    st.divider()

    st.subheader("🧠 Quick Quiz")

    st.write(
        f"What does **{word}** mean?"
    )

    answer = st.radio(
        "Choose the correct answer:",
        current_word["options"],
        key=f"answer_{selected_topic}_{current_index}"
    )

    # =====================================================
    # CHECK ANSWER
    # =====================================================

    if not st.session_state.vocab_answered:

        if st.button(
            "✅ Check Answer",
            key=f"check_{selected_topic}_{current_index}",
            use_container_width=True
        ):

            st.session_state.vocab_total += 1

            if answer == current_word["correct_answer"]:

                st.session_state.vocab_score += 1

                st.success(
                    "🎉 Correct! Excellent work!"
                )

            else:

                st.error(
                    "❌ Incorrect. Keep practicing!"
                )

                st.info(
                    f"Correct answer: {current_word['correct_answer']}"
                )

            st.session_state.vocab_answered = True

            st.rerun()

    # =====================================================
    # SCORE
    # =====================================================

    if st.session_state.vocab_answered:

        st.divider()

        percentage = calculate_percentage(
            st.session_state.vocab_score,
            st.session_state.vocab_total
        )

        st.write(
            f"### 🏆 Score: "
            f"{st.session_state.vocab_score} / "
            f"{st.session_state.vocab_total}"
        )

        st.write(
            f"### 📊 Percentage: {percentage}%"
        )

        st.info(
            get_score_message(percentage)
        )

        # =================================================
        # NEXT WORD
        # =================================================

        if current_index < total_words - 1:

            if st.button(
                "➡️ Next Word",
                key=f"next_{selected_topic}_{current_index}",
                use_container_width=True
            ):

                st.session_state.vocab_index += 1

                st.session_state.vocab_answered = False

                st.rerun()

        # =================================================
        # FINISHED ALL WORDS
        # =================================================

        else:

            st.success(
                "🎊 You completed all the words in this topic!"
            )

            final_percentage = calculate_percentage(
                st.session_state.vocab_score,
                st.session_state.vocab_total
            )

            st.write(
                f"## 🏆 Final Score: "
                f"{st.session_state.vocab_score} / "
                f"{st.session_state.vocab_total}"
            )

            st.write(
                f"## 📊 Final Percentage: "
                f"{final_percentage}%"
            )

            st.write(
                get_score_message(final_percentage)
            )

            # =============================================
            # RESTART
            # =============================================

            if st.button(
                "🔄 Practice This Topic Again",
                key="restart_topic",
                use_container_width=True
            ):

                st.session_state.vocab_index = 0
                st.session_state.vocab_score = 0
                st.session_state.vocab_total = 0
                st.session_state.vocab_answered = False

                st.rerun()
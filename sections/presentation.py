import streamlit as st

from data.presentation_data import PRESENTATION_TOPICS
from utils.speech_scoring import analyze_recording


LIGHT_BLUE = "#EAF4FB"
BLUE = "#9BCEEC"
LAVENDER = "#C5B3E3"
DARK = "#303451"
TEXT = "#68718F"


def show_presentation():

    if "presentation_topic_index" not in st.session_state:
        st.session_state.presentation_topic_index = 0

    if "presentation_notes" not in st.session_state:
        st.session_state.presentation_notes = {}

    if "presentation_score" not in st.session_state:
        st.session_state.presentation_score = {}

    if "presentation_recording_results" not in st.session_state:
        st.session_state.presentation_recording_results = {}

    st.html(
        f"""
        <style>

        .presentation-hero {{
            background-color: {BLUE};
            border-radius: 25px;
            padding: 40px 30px;
            text-align: center;
            margin-bottom: 30px;
        }}

        .presentation-card {{
            background-color: {LIGHT_BLUE};
            border: 3px solid {BLUE};
            border-radius: 22px;
            padding: 30px;
            margin: 20px 0;
        }}

        .presentation-tip {{
            background-color: #F4F0FA;
            border: 3px solid {LAVENDER};
            border-radius: 20px;
            padding: 25px;
            margin-top: 20px;
        }}

        .presentation-score {{
            background-color: #EBF8F5;
            border: 3px solid #6ECDB9;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            margin-top: 30px;
        }}

        </style>
        """
    )

    st.html(
        f"""
        <div class="presentation-hero">

            <div style="
                font-size:40px;
                font-weight:700;
                color:{DARK};
            ">
                🖼️ Presentation Practice
            </div>

            <div style="
                font-size:18px;
                color:{DARK};
                margin-top:10px;
            ">
                Practice presenting English topics clearly and confidently.
            </div>

        </div>
        """
    )

    if st.button(
        "⬅️ Back to Home",
        key="presentation_back_home",
        use_container_width=True
    ):
        st.session_state.page = "home"
        st.rerun()

    total_topics = len(PRESENTATION_TOPICS)

    if total_topics == 0:
        st.warning("No presentation topics found.")
        return

    selected_topic = st.selectbox(
        "🎯 Choose a presentation topic:",
        range(total_topics),
        index=st.session_state.presentation_topic_index,
        format_func=lambda x:
            f"Topic {PRESENTATION_TOPICS[x]['id']}: "
            f"{PRESENTATION_TOPICS[x]['title']}",
        key="presentation_topic_selector"
    )

    if selected_topic != st.session_state.presentation_topic_index:
        st.session_state.presentation_topic_index = selected_topic
        st.rerun()

    topic = PRESENTATION_TOPICS[selected_topic]
    topic_id = str(topic["id"])

    st.html(
        f"""
        <div class="presentation-card">

            <div style="
                color:{TEXT};
                font-size:15px;
                margin-bottom:10px;
            ">
                Topic {topic["id"]} of {total_topics}
            </div>

            <div style="
                font-size:30px;
                font-weight:700;
                color:{DARK};
            ">
                🖼️ {topic["title"]}
            </div>

            <div style="
                font-size:18px;
                color:{TEXT};
                line-height:1.8;
                margin-top:18px;
            ">
                {topic["description"]}
            </div>

        </div>
        """
    )

    st.html(
        f"""
        <div class="presentation-tip">

            <div style="
                font-size:22px;
                font-weight:700;
                color:{DARK};
            ">
                💡 Presentation Structure
            </div>

            <div style="
                color:{TEXT};
                line-height:1.9;
                margin-top:12px;
            ">
                <b>1. Introduction:</b> Introduce your topic.<br>
                <b>2. Main Point:</b> Explain the first important idea.<br>
                <b>3. Supporting Points:</b> Give examples or details.<br>
                <b>4. Conclusion:</b> Summarize your presentation.
            </div>

        </div>
        """
    )

    notes = st.text_area(
        "📝 Write your presentation here:",
        value=st.session_state.presentation_notes.get(topic_id, ""),
        height=240,
        key=f"presentation_notes_{topic_id}",
        placeholder="Write your introduction, main points, examples, and conclusion..."
    )

    if st.button(
        "💾 Save Presentation",
        key=f"presentation_save_{topic_id}",
        use_container_width=True
    ):
        st.session_state.presentation_notes[topic_id] = notes
        st.success("✅ Your presentation has been saved!")

    st.write("")

    st.html(
        """
        <div style="
            background:#EAF4FB;
            border:2px solid #9BCEEC;
            border-radius:18px;
            padding:20px;
            margin:18px 0;
        ">
            <div style="font-size:22px;font-weight:700;color:#303451;">
                🎙️ Record Your Presentation
            </div>
            <div style="color:#68718F;margin-top:8px;line-height:1.6;">
                Speak your presentation naturally. Then analyze the
                recording to receive speaking and pronunciation/clarity scores.
            </div>
        </div>
        """
    )

    presentation_audio = st.audio_input(
        "🎙️ Record your presentation",
        sample_rate=16000,
        key=f"presentation_audio_{topic_id}"
    )

    if presentation_audio is not None:
        st.audio(presentation_audio, format="audio/wav")

        if st.button(
            "🤖 Analyze My Presentation",
            key=f"presentation_analyze_{topic_id}",
            use_container_width=True
        ):
            expected = st.session_state.presentation_notes.get(
                topic_id, notes
            ).strip()

            result = analyze_recording(
                presentation_audio.getvalue(),
                expected_text=expected
            )

            st.session_state.presentation_recording_results[topic_id] = result

            if result["success"]:
                st.success("✅ Presentation analyzed successfully!")
            else:
                st.error(result["error"])

    result = st.session_state.presentation_recording_results.get(topic_id)

    if result and result.get("success"):
        score_col1, score_col2 = st.columns(2)

        with score_col1:
            st.metric(
                "🗣️ Speaking Skill",
                f'{result["speaking_score"]}/100'
            )

        with score_col2:
            st.metric(
                "🔊 Pronunciation / Clarity",
                f'{result["pronunciation_score"]}/100'
            )

        st.write(
            f'⏱️ Speaking time: **{result["duration"]:.1f} seconds**'
        )
        st.write(
            f'💬 Words recognized: **{result["word_count"]}** '
            f'| Speaking rate: **{result["wpm"]} words/min**'
        )

        st.write("### 📝 What the app heard")
        st.info(result["transcript"])

        st.caption(
            "The pronunciation/clarity score is an automatic estimate "
            "based on speech recognition and comparison with your written presentation."
        )

    score = st.slider(
        "⭐ Rate your presentation",
        min_value=1,
        max_value=5,
        value=st.session_state.presentation_score.get(topic_id, 3),
        help="1 = Need more practice, 5 = Excellent"
    )

    if st.button(
        "📊 Save My Score",
        key=f"presentation_score_{topic_id}",
        use_container_width=True
    ):
        st.session_state.presentation_score[topic_id] = score
        st.success(f"⭐ Score saved: {score}/5")

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if selected_topic > 0:
            if st.button(
                "⬅️ Previous Topic",
                key=f"presentation_previous_{topic_id}",
                use_container_width=True
            ):
                st.session_state.presentation_topic_index -= 1
                st.rerun()

    with col2:
        if selected_topic < total_topics - 1:
            if st.button(
                "➡️ Next Topic",
                key=f"presentation_next_{topic_id}",
                use_container_width=True
            ):
                st.session_state.presentation_topic_index += 1
                st.rerun()

    completed = len(st.session_state.presentation_score)

    if completed > 0:

        total_score = sum(st.session_state.presentation_score.values())
        average = round(total_score / completed, 1)

        st.html(
            f"""
            <div class="presentation-score">

                <div style="
                    font-size:28px;
                    font-weight:700;
                    color:{DARK};
                ">
                    📊 Presentation Progress
                </div>

                <div style="
                    font-size:22px;
                    color:{DARK};
                    margin-top:12px;
                ">
                    Topics Practiced: {completed}/{total_topics}
                </div>

                <div style="
                    font-size:22px;
                    color:{TEXT};
                    margin-top:8px;
                ">
                    Average Self-Score: {average}/5
                </div>

            </div>
            """
        )

import streamlit as st

from data.jam_data import JAM_TOPICS
from utils.speech_scoring import analyze_recording


MINT = "#6ECDB9"
LIGHT_MINT = "#EAF8F5"
LAVENDER = "#C5B3E3"
DARK = "#303451"
TEXT = "#68718F"
BACKGROUND = "#F8F9FD"


def show_jam():

    if "jam_topic_index" not in st.session_state:
        st.session_state.jam_topic_index = 0

    if "jam_started" not in st.session_state:
        st.session_state.jam_started = False

    if "jam_speech" not in st.session_state:
        st.session_state.jam_speech = {}

    if "jam_self_score" not in st.session_state:
        st.session_state.jam_self_score = {}

    if "jam_recording_results" not in st.session_state:
        st.session_state.jam_recording_results = {}

    st.html(
        f"""
        <style>

        .jam-hero {{
            background-color: {MINT};
            border-radius: 25px;
            padding: 40px 30px;
            text-align: center;
            margin-bottom: 30px;
        }}

        .jam-topic-card {{
            background-color: {LIGHT_MINT};
            border: 3px solid {MINT};
            border-radius: 22px;
            padding: 30px;
            margin: 20px 0;
        }}

        .jam-tip-card {{
            background-color: #F4F0FA;
            border: 3px solid {LAVENDER};
            border-radius: 20px;
            padding: 25px;
            margin-top: 20px;
        }}

        .jam-score-card {{
            background-color: #FFF9E8;
            border: 3px solid #F5E1A6;
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
        <div class="jam-hero">

            <div style="
                font-size:40px;
                font-weight:700;
                color:{DARK};
            ">
                🎤 JAM - Just A Minute
            </div>

            <div style="
                font-size:18px;
                color:{DARK};
                margin-top:10px;
            ">
                Speak about a topic for one minute and build your confidence.
            </div>

        </div>
        """
    )

    if st.button(
        "⬅️ Back to Home",
        key="jam_back_home",
        use_container_width=True
    ):
        st.session_state.page = "home"
        st.session_state.jam_started = False
        st.rerun()

    if not JAM_TOPICS:
        st.warning("No JAM topics found.")
        return

    total_topics = len(JAM_TOPICS)

    selected_topic = st.selectbox(
        "🎯 Choose a JAM topic:",
        range(total_topics),
        index=st.session_state.jam_topic_index,
        format_func=lambda x: (
            f"Topic {JAM_TOPICS[x]['id']}: {JAM_TOPICS[x]['title']}"
        ),
        key="jam_topic_selector"
    )

    if selected_topic != st.session_state.jam_topic_index:
        st.session_state.jam_topic_index = selected_topic
        st.session_state.jam_started = False
        st.rerun()

    topic = JAM_TOPICS[selected_topic]
    topic_id = str(topic["id"])

    st.html(
        f"""
        <div class="jam-topic-card">

            <div style="
                color:{TEXT};
                font-size:15px;
                margin-bottom:10px;
            ">
                JAM Topic {topic["id"]} of {total_topics}
            </div>

            <div style="
                font-size:30px;
                font-weight:700;
                color:{DARK};
            ">
                🎤 {topic["title"]}
            </div>

            <div style="
                font-size:18px;
                color:{TEXT};
                line-height:1.8;
                margin-top:18px;
            ">
                {topic["prompt"]}
            </div>

        </div>
        """
    )

    st.html(
        f"""
        <div class="jam-tip-card">

            <div style="
                font-size:22px;
                font-weight:700;
                color:{DARK};
            ">
                💡 How to speak
            </div>

            <div style="
                color:{TEXT};
                line-height:1.8;
                margin-top:12px;
            ">
                1. Start with a simple introduction.<br>
                2. Give 2 or 3 main points.<br>
                3. Add a small example or personal experience.<br>
                4. Finish with a short conclusion.
            </div>

        </div>
        """
    )

    st.write("")

    if not st.session_state.jam_started:

        if st.button(
            "🎤 Start My 1-Minute Practice",
            key=f"jam_start_{topic_id}",
            use_container_width=True
        ):
            st.session_state.jam_started = True
            st.rerun()

    else:

        st.success(
            "🎤 Your 1-minute practice has started! "
            "Speak aloud about the topic."
        )

        st.info(
            "⏱️ Use a phone timer or stopwatch for 1 minute while speaking."
        )

        st.html(
            """
            <div style="
                background:#EAF8F5;
                border:2px solid #6ECDB9;
                border-radius:18px;
                padding:20px;
                margin:18px 0;
            ">
                <div style="font-size:22px;font-weight:700;color:#303451;">
                    🎙️ Record Your Speaking
                </div>
                <div style="color:#68718F;margin-top:8px;line-height:1.6;">
                    Click the microphone, speak about the topic, then stop.
                    Your recording will be analyzed for speaking performance
                    and pronunciation/clarity.
                </div>
            </div>
            """
        )

        jam_audio = st.audio_input(
            "🎙️ Record your 1-minute answer",
            sample_rate=16000,
            key=f"jam_audio_{topic_id}"
        )

        if jam_audio is not None:
            st.audio(jam_audio, format="audio/wav")

            if st.button(
                "🤖 Analyze My Recording",
                key=f"jam_analyze_{topic_id}",
                use_container_width=True
            ):
                expected = st.session_state.jam_speech.get(
                    topic_id, ""
                ).strip()

                result = analyze_recording(
                    jam_audio.getvalue(),
                    expected_text=expected
                )

                st.session_state.jam_recording_results[topic_id] = result

                if result["success"]:
                    st.success("✅ Recording analyzed successfully!")
                else:
                    st.error(result["error"])

        result = st.session_state.jam_recording_results.get(topic_id)

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
                "based on speech recognition and, when available, comparison "
                "with your written practice."
            )

        speech = st.text_area(
            "📝 After speaking, type a short version of what you said:",
            value=st.session_state.jam_speech.get(topic_id, ""),
            height=180,
            key=f"jam_speech_{topic_id}",
            placeholder="Write a few sentences about the topic..."
        )

        if st.button(
            "💾 Save My Practice",
            key=f"jam_save_{topic_id}",
            use_container_width=True
        ):
            st.session_state.jam_speech[topic_id] = speech
            st.success("✅ Your JAM practice has been saved!")

        st.write("")

        self_score = st.slider(
            "⭐ How well did you speak?",
            min_value=1,
            max_value=5,
            value=st.session_state.jam_self_score.get(topic_id, 3),
            help="1 = Need more practice, 5 = Excellent"
        )

        if st.button(
            "📊 Save My Score",
            key=f"jam_score_{topic_id}",
            use_container_width=True
        ):
            st.session_state.jam_self_score[topic_id] = self_score
            st.success(
                f"⭐ Score saved: {self_score}/5"
            )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            if selected_topic > 0:

                if st.button(
                    "⬅️ Previous Topic",
                    key=f"jam_previous_{topic_id}",
                    use_container_width=True
                ):
                    st.session_state.jam_topic_index -= 1
                    st.session_state.jam_started = False
                    st.rerun()

        with col2:

            if selected_topic < total_topics - 1:

                if st.button(
                    "➡️ Next Topic",
                    key=f"jam_next_{topic_id}",
                    use_container_width=True
                ):
                    st.session_state.jam_topic_index += 1
                    st.session_state.jam_started = False
                    st.rerun()

    completed = len(st.session_state.jam_self_score)

    if completed > 0:

        total_score = sum(st.session_state.jam_self_score.values())
        average = round(total_score / completed, 1)

        st.html(
            f"""
            <div class="jam-score-card">

                <div style="
                    font-size:28px;
                    font-weight:700;
                    color:{DARK};
                ">
                    📊 JAM Progress
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

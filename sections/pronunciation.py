import streamlit as st
import streamlit.components.v1 as components

from data.pronunciation_data import PRONUNCIATION_TOPICS
from utils.speech_scoring import analyze_recording


def speak_text(text):
    """
    Create a browser-based pronunciation button using JavaScript.
    The sound is produced by the user's browser, so no audio file
    needs to be downloaded or stored.
    """

    safe_text = (
        text.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", " ")
        .replace("\r", " ")
    )

    html = f"""
    <div style="
        display:flex;
        justify-content:center;
        margin:12px 0 20px 0;
    ">
        <button onclick="speakWord()"
            style="
                background:#CF93B7;
                color:#303451;
                border:none;
                border-radius:14px;
                padding:12px 24px;
                font-size:17px;
                font-weight:700;
                cursor:pointer;
                box-shadow:0 3px 8px rgba(0,0,0,0.10);
            ">
            🔊 Listen to Pronunciation
        </button>
    </div>

    <script>
        function speakWord() {{
            const text = '{safe_text}';

            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();

                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                utterance.rate = 0.75;
                utterance.pitch = 1;

                window.speechSynthesis.speak(utterance);
            }} else {{
                alert("Your browser does not support text-to-speech.");
            }}
        }}
    </script>
    """

    components.html(html, height=80)


def show_pronunciation():

    # ---------------------------------------------------------
    # SESSION STATE
    # ---------------------------------------------------------

    if "pronunciation_topic_index" not in st.session_state:
        st.session_state.pronunciation_topic_index = 0

    if "pronunciation_notes" not in st.session_state:
        st.session_state.pronunciation_notes = {}

    if "pronunciation_scores" not in st.session_state:
        st.session_state.pronunciation_scores = {}

    if "pronunciation_recording_results" not in st.session_state:
        st.session_state.pronunciation_recording_results = {}

    # ---------------------------------------------------------
    # CURRENT TOPIC
    # ---------------------------------------------------------

    topics = PRONUNCIATION_TOPICS

    current_index = st.session_state.pronunciation_topic_index
    current_topic = topics[current_index]

    # ---------------------------------------------------------
    # HERO
    # ---------------------------------------------------------

    st.html(
        """
        <div class="hero" style="background-color:#F4E0EA;">
            <div class="hero-title">🗣️ Pronunciation Practice</div>
            <div class="hero-text">
                Listen, repeat and improve your English pronunciation.
            </div>
        </div>
        """
    )

    # ---------------------------------------------------------
    # BACK TO HOME
    # ---------------------------------------------------------

    if st.button("⬅️ Back to Home", key="pronunciation_home"):
        st.session_state.page = "home"
        st.rerun()

    # ---------------------------------------------------------
    # TOPIC SELECTOR
    # ---------------------------------------------------------

    topic_titles = [topic["title"] for topic in topics]

    selected_title = st.selectbox(
        "📚 Choose a pronunciation topic",
        topic_titles,
        index=current_index,
        key="pronunciation_topic_selector"
    )

    selected_index = topic_titles.index(selected_title)

    if selected_index != st.session_state.pronunciation_topic_index:
        st.session_state.pronunciation_topic_index = selected_index
        st.rerun()

    current_index = st.session_state.pronunciation_topic_index
    current_topic = topics[current_index]

    # ---------------------------------------------------------
    # TOPIC INFORMATION
    # ---------------------------------------------------------

    st.html(
        f"""
        <div style="
            background-color:#F8F9FD;
            border:2px solid #CF93B7;
            border-radius:20px;
            padding:25px;
            margin:20px 0;
        ">
            <div style="
                font-size:28px;
                font-weight:700;
                color:#303451;
            ">
                🎯 {current_topic["title"]}
            </div>

            <div style="
                color:#68718F;
                font-size:17px;
                margin-top:10px;
                line-height:1.6;
            ">
                {current_topic["description"]}
            </div>
        </div>
        """
    )

    # ---------------------------------------------------------
    # INSTRUCTIONS
    # ---------------------------------------------------------

    st.html(
        """
        <div style="
            background-color:#F5E1A6;
            border-radius:18px;
            padding:20px;
            margin:20px 0;
        ">
            <div style="
                font-size:21px;
                font-weight:700;
                color:#303451;
            ">
                💡 How to practice
            </div>

            <div style="
                color:#303451;
                line-height:1.8;
                margin-top:10px;
            ">
                1️⃣ Click 🔊 Listen to Pronunciation.<br>
                2️⃣ Listen carefully.<br>
                3️⃣ Repeat the word or sentence aloud.<br>
                4️⃣ Repeat 2–3 times.<br>
                5️⃣ Try to speak naturally.
            </div>
        </div>
        """
    )

    # ---------------------------------------------------------
    # WORD / SENTENCE PRACTICE
    # ---------------------------------------------------------

    st.html(
        """
        <div class="section-heading">
            🔊 Practice Words & Sentences
        </div>

        <div class="section-description">
            Listen to each item and repeat it aloud.
        </div>
        """
    )

    words = current_topic.get("words", [])

    for number, item in enumerate(words, start=1):

        # Existing topics use simple strings.
        # The 100 Difficult Words topic uses dictionaries
        # containing both the word and the easy pronunciation.
        if isinstance(item, dict):
            word = item["word"]
            easy_pronunciation = item["pronunciation"]
        else:
            word = item
            easy_pronunciation = ""

        st.html(
            f"""
            <div style="
                background-color:#F4E0EA;
                border-radius:18px;
                padding:18px 22px;
                margin:12px 0 0 0;
                border:1px solid #CF93B7;
            ">
                <div style="
                    color:#68718F;
                    font-size:14px;
                    margin-bottom:5px;
                ">
                    Word {number}
                </div>

                <div style="
                    color:#303451;
                    font-size:25px;
                    font-weight:700;
                ">
                    {word}
                </div>

                {
                    f'<div style="color:#CF93B7; font-size:18px; font-weight:700; margin-top:8px;">🗣️ {easy_pronunciation}</div>'
                    if easy_pronunciation else ""
                }
            </div>
            """
        )

        speak_text(word)

    # ---------------------------------------------------------
    # RECORDING + AUTOMATIC SCORE
    # ---------------------------------------------------------

    st.html(
        """
        <div style="
            background:#F4E0EA;
            border:2px solid #CF93B7;
            border-radius:18px;
            padding:20px;
            margin:24px 0 18px 0;
        ">
            <div style="font-size:22px;font-weight:700;color:#303451;">
                🎙️ Record Your Pronunciation
            </div>
            <div style="color:#68718F;margin-top:8px;line-height:1.6;">
                First listen to the words above. Then click the microphone
                and pronounce the words aloud. The app will convert your
                speech to text and calculate a pronunciation/clarity estimate.
            </div>
        </div>
        """
    )

    pronunciation_audio = st.audio_input(
        "🎙️ Record your pronunciation",
        sample_rate=16000,
        key=f"pronunciation_audio_{current_index}"
    )

    if pronunciation_audio is not None:
        st.audio(pronunciation_audio, format="audio/wav")

        if st.button(
            "🤖 Analyze My Pronunciation",
            key=f"analyze_pronunciation_{current_index}",
            use_container_width=True
        ):
            expected_items = []

            for item in words:
                if isinstance(item, dict):
                    expected_items.append(item["word"])
                else:
                    expected_items.append(item)

            expected_text = " ".join(expected_items)

            result = analyze_recording(
                pronunciation_audio.getvalue(),
                expected_text=expected_text
            )

            st.session_state.pronunciation_recording_results[
                current_index
            ] = result

            if result["success"]:
                st.success("✅ Pronunciation analyzed successfully!")
            else:
                st.error(result["error"])

    result = st.session_state.pronunciation_recording_results.get(
        current_index
    )

    if result and result.get("success"):
        score_col1, score_col2 = st.columns(2)

        with score_col1:
            st.metric(
                "🔊 Pronunciation / Clarity",
                f'{result["pronunciation_score"]}/100'
            )

        with score_col2:
            st.metric(
                "🗣️ Speaking Skill",
                f'{result["speaking_score"]}/100'
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
            "This is an automatic pronunciation/clarity estimate based on "
            "speech recognition and how closely the recognized words match the practice words."
        )

    # ---------------------------------------------------------
    # NOTES
    # ---------------------------------------------------------

    st.html(
        """
        <div class="section-heading">
            📝 My Practice Notes
        </div>

        <div class="section-description">
            Write any pronunciation difficulty or improvement you noticed.
        </div>
        """
    )

    saved_note = st.session_state.pronunciation_notes.get(
        current_index,
        ""
    )

    notes = st.text_area(
        "Practice notes",
        value=saved_note,
        height=120,
        placeholder="Example: I find the R sound difficult.",
        key=f"pronunciation_notes_{current_index}",
        label_visibility="collapsed"
    )

    if st.button(
        "💾 Save Notes",
        key=f"save_pronunciation_notes_{current_index}",
        use_container_width=True
    ):
        st.session_state.pronunciation_notes[current_index] = notes
        st.success("✅ Your notes were saved!")

    # ---------------------------------------------------------
    # SELF SCORE
    # ---------------------------------------------------------

    st.html(
        """
        <div class="section-heading">
            ⭐ How did you pronounce it?
        </div>

        <div class="section-description">
            Give yourself a score from 1 to 5.
        </div>
        """
    )

    current_score = st.session_state.pronunciation_scores.get(
        current_index,
        0
    )

    score = st.radio(
        "Pronunciation score",
        [1, 2, 3, 4, 5],
        index=(current_score - 1 if current_score else None),
        horizontal=True,
        key=f"pronunciation_score_{current_index}",
        label_visibility="collapsed"
    )

    if st.button(
        "⭐ Save Score",
        key=f"save_pronunciation_score_{current_index}",
        use_container_width=True
    ):
        st.session_state.pronunciation_scores[current_index] = score
        st.success(f"Score saved: {score}/5")

    # ---------------------------------------------------------
    # PROGRESS
    # ---------------------------------------------------------

    completed = len(st.session_state.pronunciation_scores)
    total = len(topics)

    st.progress(
        completed / total if total else 0
    )

    st.write(
        f"📊 Pronunciation Progress: **{completed}/{total} topics completed**"
    )

    # ---------------------------------------------------------
    # NAVIGATION
    # ---------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅️ Previous Topic",
            key="pronunciation_previous",
            use_container_width=True,
            disabled=(current_index == 0)
        ):
            st.session_state.pronunciation_topic_index -= 1
            st.rerun()

    with col2:

        if st.button(
            "Next Topic ➡️",
            key="pronunciation_next",
            use_container_width=True,
            disabled=(current_index == total - 1)
        ):
            st.session_state.pronunciation_topic_index += 1
            st.rerun()

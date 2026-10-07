import json
from pathlib import Path
import streamlit as st
from data.sentence_data import SENTENCE_TASKS
from utils.scoring import calculate_percentage, get_score_message

PINK = "#CF93B7"
MINT = "#6ECDB9"
LIGHT_BLUE = "#9BCEEC"
LAVENDER = "#C5B3E3"
DARK = "#303451"
TEXT = "#68718F"

PROGRESS_FILE = Path(__file__).resolve().parent.parent / "student_progress.json"


def load_all_progress():
    if not PROGRESS_FILE.exists():
        return {}
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_all_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as file:
        json.dump(progress, file, indent=4, ensure_ascii=False)


def load_student_progress(profile_name):
    all_progress = load_all_progress()
    saved = all_progress.get(profile_name, {"current_index": 0, "answers": {}})
    return {
        "current_index": saved.get("current_index", 0),
        "answers": saved.get("answers", {})
    }


def save_student_progress(profile_name, current_index, answers):
    all_progress = load_all_progress()
    all_progress[profile_name] = {
        "current_index": current_index,
        "answers": answers
    }
    save_all_progress(all_progress)


def reset_student_progress(profile_name):
    all_progress = load_all_progress()
    all_progress[profile_name] = {"current_index": 0, "answers": {}}
    save_all_progress(all_progress)


def show_sentence_formation():
    if "sentence_profile" not in st.session_state:
        st.session_state.sentence_profile = ""
    if "sentence_profile_loaded" not in st.session_state:
        st.session_state.sentence_profile_loaded = False
    if "sentence_index" not in st.session_state:
        st.session_state.sentence_index = 0
    if "sentence_answers" not in st.session_state:
        st.session_state.sentence_answers = {}

    st.markdown(f"""
    <style>
    .sentence-hero {{ background-color:{MINT}; border-radius:25px; padding:35px 30px; text-align:center; margin-bottom:25px; }}
    .sentence-card {{ background-color:#F1FAF8; border:3px solid {MINT}; border-radius:22px; padding:28px; margin:20px 0; }}
    .scramble-box {{ background-color:#EEF8FC; border:2px solid {LIGHT_BLUE}; border-radius:18px; padding:22px; font-size:20px; line-height:1.8; color:{DARK}; }}
    .score-box {{ background-color:#F4F0FA; border:3px solid {LAVENDER}; border-radius:20px; padding:28px; text-align:center; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sentence-hero">
        <div style="font-size:38px;font-weight:700;color:{DARK};">✍️ Sentence Formation</div>
        <div style="font-size:17px;color:{DARK};margin-top:10px;">Arrange the words and build correct English sentences.</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Back to Home", key="sentence_back"):
        st.session_state.page = "home"
        st.session_state.sentence_profile_loaded = False
        st.rerun()

    st.markdown(f"<h3 style='color:{DARK};'>👤 Student Profile</h3><p style='color:{TEXT};'>Enter the student's profile name. Progress is saved separately for each person.</p>", unsafe_allow_html=True)

    profile_name = st.text_input("Profile Name", value=st.session_state.sentence_profile, placeholder="Example: Sarubala", key="sentence_profile_input").strip()

    if profile_name != st.session_state.sentence_profile:
        st.session_state.sentence_profile = profile_name
        st.session_state.sentence_profile_loaded = False

    if not profile_name:
        st.info("👤 Please enter a profile name to start Sentence Formation.")
        return

    if not st.session_state.sentence_profile_loaded:
        saved = load_student_progress(profile_name)
        st.session_state.sentence_index = min(saved["current_index"], len(SENTENCE_TASKS) - 1)
        st.session_state.sentence_answers = saved["answers"]
        st.session_state.sentence_profile_loaded = True

    answers = st.session_state.sentence_answers
    score = sum(1 for task in SENTENCE_TASKS if answers.get(str(task["id"])) == task["correct_answer"])
    total_answered = len(answers)

    st.success(f"👤 Profile: **{profile_name}**  |  📊 Score: **{score}/{len(SENTENCE_TASKS)}**  |  ✅ Answered: **{total_answered}/{len(SENTENCE_TASKS)}**")

    if st.button("🔄 Reset My Sentence Progress", key="sentence_reset"):
        reset_student_progress(profile_name)
        st.session_state.sentence_index = 0
        st.session_state.sentence_answers = {}
        st.rerun()

    task = SENTENCE_TASKS[st.session_state.sentence_index]
    current = st.session_state.sentence_index + 1
    total = len(SENTENCE_TASKS)
    task_id = str(task["id"])

    st.markdown(f"<h2 style='color:{DARK};'>🎯 Question {current} of {total}</h2>", unsafe_allow_html=True)
    st.progress(current / total)

    st.markdown(f"""
    <div class="sentence-card">
        <div style="color:{TEXT};font-size:16px;margin-bottom:12px;">📝 {task["instruction"]}</div>
        <div style="color:{TEXT};font-size:14px;margin-bottom:10px;">Difficulty: {task["difficulty"]}</div>
        <div class="scramble-box"><b>🔤 Arrange these words:</b><br><br>{"  |  ".join(task["words"])}</div>
    </div>
    """, unsafe_allow_html=True)

    saved_answer = answers.get(task_id)

    if saved_answer is not None:
        selected = st.radio("Choose the correct sentence:", task["options"], index=task["options"].index(saved_answer), key=f"sentence_option_{task_id}")
        if st.button("💾 Save Changed Answer", key=f"sentence_save_{task_id}", use_container_width=True):
            answers[task_id] = selected
            save_student_progress(profile_name, st.session_state.sentence_index, answers)
            st.rerun()
        if saved_answer == task["correct_answer"]:
            st.success("✅ Correct! Excellent sentence formation.")
        else:
            st.error("❌ Not quite correct.")
            st.info(f"✅ Correct answer: {task['correct_answer']}")
    else:
        selected = st.radio("Choose the correct sentence:", task["options"], key=f"sentence_option_{task_id}")
        if st.button("🎯 Check Answer", key=f"sentence_check_{task_id}", use_container_width=True):
            answers[task_id] = selected
            save_student_progress(profile_name, st.session_state.sentence_index, answers)
            st.rerun()

    st.markdown(f"<div style='background-color:#F8F9FD;border-radius:15px;padding:18px;margin-top:15px;'><b>Correct sentence:</b><br><span style='font-size:19px;color:{DARK};'>{task['sentence']}</span></div>", unsafe_allow_html=True)

    previous_col, next_col = st.columns(2)

    with previous_col:
        if st.session_state.sentence_index > 0:
            if st.button("⬅️ Previous Question", key=f"sentence_previous_{task_id}", use_container_width=True):
                st.session_state.sentence_index -= 1
                save_student_progress(profile_name, st.session_state.sentence_index, answers)
                st.rerun()

    with next_col:
        if st.session_state.sentence_index < total - 1:
            if st.button("➡️ Next Question", key=f"sentence_next_{task_id}", use_container_width=True):
                st.session_state.sentence_index += 1
                save_student_progress(profile_name, st.session_state.sentence_index, answers)
                st.rerun()
        elif len(answers) == total:
            percentage = calculate_percentage(score, total)
            message = get_score_message(percentage)
            st.markdown(f"<div class='score-box'><div style='font-size:30px;font-weight:700;color:{DARK};'>🏆 Sentence Formation Completed!</div><div style='font-size:24px;margin-top:15px;color:{DARK};'>Score: {score} / {total}</div><div style='font-size:20px;margin-top:10px;color:{TEXT};'>Percentage: {percentage}%</div><div style='font-size:20px;margin-top:10px;color:{DARK};'>{message}</div></div>", unsafe_allow_html=True)
        else:
            st.info("📝 Answer all 500 questions before viewing the final score.")

import streamlit as st
import base64
from pathlib import Path

from utils.styles import load_styles

from sections.vocabulary import show_vocabulary
from sections.grammar import show_grammar
from sections.sentence_formation import show_sentence_formation
from sections.conversation import show_conversation
from sections.english_rules import show_english_rules
from sections.stories import show_story_understanding
from sections.jam import show_jam
from sections.presentation import show_presentation
from sections.pronunciation import show_pronunciation


st.set_page_config(
    page_title="NikoTalk AI",
    page_icon="🗣️",
    layout="wide"
)

load_styles()

if "page" not in st.session_state:
    st.session_state.page = "home"


def image_base64(filename):
    path = Path(__file__).parent / "assets" / filename

    if not path.exists():
        return ""

    return base64.b64encode(path.read_bytes()).decode("utf-8")


def card(icon, title, description, color):
    icon64 = image_base64(icon)

    st.html(
        f"""
        <div class="card" style="background:{color};">
            <img
                src="data:image/png;base64,{icon64}"
                class="card-icon"
            >

            <div class="card-title">{title}</div>

            <div class="card-text">
                {description}
            </div>
        </div>
        """
    )


def button(label, key, css_class, page):
    st.markdown(f'<div class="home-button {css_class}">', unsafe_allow_html=True)

    if st.button(
        f"{label}   →",
        key=key,
        use_container_width=True
    ):
        st.session_state.page = page
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def show_home():

    lion64 = image_base64("lion.png")

    st.html(
        f"""
        <div class="hero">

            <img
                src="data:image/png;base64,{lion64}"
                class="lion-mascot"
            >

            <div class="hero-content">
                <div class="hero-title">
                    🗣️ NikoTalk AI
                </div>

                <div class="hero-text">
                    Improve your English communication skills step by step.
                </div>
            </div>

        </div>
        """
    )

    st.html(
        """
        <div class="section-heading">📚 Learn & Practice</div>

        <div class="section-description">
            Choose a section and start improving your English.
        </div>
        """
    )

    # ROW 1
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        card(
            "vocabulary.png",
            "Vocabulary",
            "Learn new English words with meaning,<br>"
            "pronunciation and examples.",
            "#FFF3C9"
        )
        button("Start Vocabulary", "vocab_btn", "yellow-btn", "vocabulary")

    with c2:
        card(
            "grammar.png",
            "Grammar",
            "Learn English grammar with simple<br>"
            "explanations and examples.",
            "#EEE7FF"
        )
        button("Start Grammar", "grammar_btn", "purple-btn", "grammar")

    with c3:
        card(
            "sentence.png",
            "Sentence Formation",
            "Learn how to make correct and meaningful<br>"
            "sentences.",
            "#FFE1EB"
        )
        button(
            "Start Sentence Formation",
            "sentence_btn",
            "pink-btn",
            "sentence_formation"
        )

    # ROW 2
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        card(
            "conversation.png",
            "Daily Conversation",
            "Practice everyday conversations and<br>"
            "choose the best response.",
            "#CFE9FF"
        )
        button(
            "Start Conversation",
            "conversation_btn",
            "blue-btn",
            "conversation"
        )

    with c2:
        card(
            "rules.png",
            "Simple English Rules",
            "Learn simple English rules and test<br>"
            "your understanding.",
            "#FFF0BE"
        )
        button(
            "Start English Rules",
            "rules_btn",
            "yellow-btn",
            "english_rules"
        )

    with c3:
        card(
            "story.png",
            "Story Understanding",
            "Read short stories and answer questions<br>"
            "to improve reading comprehension.",
            "#E8DDFF"
        )
        button("Start Stories", "stories_btn", "purple-btn", "story")

    # ROW 3
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        card(
            "jam.png",
            "JAM – Just A Minute",
            "Practice speaking for one minute on<br>"
            "different topics.",
            "#D4F5E7"
        )
        button("Start JAM", "jam_btn", "green-btn", "jam")

    with c2:
        card(
            "presentation.png",
            "Presentation Practice",
            "Practice preparing and delivering<br>"
            "short English presentations.",
            "#D2E9FF"
        )
        button(
            "Start Presentation",
            "presentation_btn",
            "blue-btn",
            "presentation"
        )

    with c3:
        card(
            "pronunciation.png",
            "Pronunciation Practice",
            "Practice difficult English words, listen<br>"
            "to pronunciation and improve speaking confidence.",
            "#FFE1EB"
        )
        button(
            "Start Pronunciation",
            "pronunciation_btn",
            "pink-btn",
            "pronunciation"
        )


if st.session_state.page == "home":
    show_home()

elif st.session_state.page == "vocabulary":
    show_vocabulary()

elif st.session_state.page == "grammar":
    show_grammar()

elif st.session_state.page == "sentence_formation":
    show_sentence_formation()

elif st.session_state.page == "conversation":
    show_conversation()

elif st.session_state.page == "english_rules":
    show_english_rules()

elif st.session_state.page == "story":
    show_story_understanding()

elif st.session_state.page == "jam":
    show_jam()

elif st.session_state.page == "presentation":
    show_presentation()

elif st.session_state.page == "pronunciation":
    show_pronunciation()

else:
    st.session_state.page = "home"
    st.rerun()

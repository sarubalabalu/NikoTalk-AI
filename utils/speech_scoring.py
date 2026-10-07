import io
import re
import wave
from difflib import SequenceMatcher

try:
    import speech_recognition as sr
except ImportError:
    sr = None


def get_audio_duration(audio_bytes):
    """Return WAV duration in seconds."""
    try:
        with wave.open(io.BytesIO(audio_bytes), "rb") as wav:
            frames = wav.getnframes()
            rate = wav.getframerate()

            if rate:
                return frames / float(rate)

    except Exception:
        pass

    return 0.0


def normalize_words(text):
    return re.findall(
        r"[a-zA-Z']+",
        (text or "").lower()
    )


def transcribe_audio(audio_bytes):
    """
    Convert the recorded WAV audio to text.

    SpeechRecognition uses Google's speech-recognition service here.
    An internet connection is required for the transcription step.
    """

    if sr is None:
        return "", "SpeechRecognition is not installed."

    try:
        recognizer = sr.Recognizer()

        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio = recognizer.record(source)

        transcript = recognizer.recognize_google(audio)

        return transcript, ""

    except sr.UnknownValueError:
        return "", "I could not clearly understand the recording."

    except sr.RequestError:
        return (
            "",
            "Speech recognition service is unavailable. "
            "Please check your internet connection."
        )

    except Exception as exc:
        return "", f"Could not analyze the recording: {exc}"


def text_similarity(expected_text, transcript):
    expected = normalize_words(expected_text)
    actual = normalize_words(transcript)

    if not expected or not actual:
        return 0

    return round(
        SequenceMatcher(
            None,
            expected,
            actual
        ).ratio() * 100
    )


def pronunciation_score(expected_text, transcript):
    """
    Estimate pronunciation/clarity by comparing the recognized
    words with the words the learner was expected to say.

    This is not phoneme-level pronunciation grading.
    """

    if not expected_text:
        return 70

    return max(
        0,
        min(
            100,
            text_similarity(
                expected_text,
                transcript
            )
        )
    )


def speaking_score(transcript, duration_seconds):
    """
    Estimate speaking skill from:
    - speaking duration
    - amount of speech
    - speaking rate
    """

    words = normalize_words(transcript)
    word_count = len(words)

    if duration_seconds > 0:
        wpm = (word_count / duration_seconds) * 60
    else:
        wpm = 0

    if duration_seconds >= 45:
        length_score = 100
    elif duration_seconds >= 30:
        length_score = 85
    elif duration_seconds >= 15:
        length_score = 70
    else:
        length_score = 50

    if word_count >= 120:
        content_score = 100
    elif word_count >= 80:
        content_score = 90
    elif word_count >= 40:
        content_score = 75
    elif word_count >= 15:
        content_score = 60
    else:
        content_score = 40

    if 100 <= wpm <= 160:
        pace_score = 100
    elif 80 <= wpm < 100 or 160 < wpm <= 190:
        pace_score = 85
    elif 60 <= wpm < 80 or 190 < wpm <= 220:
        pace_score = 70
    else:
        pace_score = 55

    score = round(
        (length_score * 0.30)
        + (content_score * 0.35)
        + (pace_score * 0.35)
    )

    return (
        max(0, min(100, score)),
        word_count,
        round(wpm)
    )


def analyze_recording(audio_bytes, expected_text=""):
    """
    Complete recording analysis.
    """

    duration = get_audio_duration(audio_bytes)

    transcript, error = transcribe_audio(audio_bytes)

    if error:
        return {
            "success": False,
            "error": error,
            "duration": duration,
            "transcript": "",
            "pronunciation_score": 0,
            "speaking_score": 0,
            "word_count": 0,
            "wpm": 0,
        }

    pron_score = pronunciation_score(
        expected_text,
        transcript
    )

    speak_score, word_count, wpm = speaking_score(
        transcript,
        duration
    )

    return {
        "success": True,
        "error": "",
        "duration": duration,
        "transcript": transcript,
        "pronunciation_score": pron_score,
        "speaking_score": speak_score,
        "word_count": word_count,
        "wpm": wpm,
    }

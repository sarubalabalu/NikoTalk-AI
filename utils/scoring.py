def calculate_percentage(score, total):
    if total == 0:
        return 0

    return round((score / total) * 100)


def get_score_message(percentage):

    if percentage >= 90:
        return "🏆 Excellent!"

    elif percentage >= 75:
        return "🌟 Very Good!"

    elif percentage >= 50:
        return "👍 Good! Keep practicing."

    else:
        return "💪 Keep practicing. You can improve!"
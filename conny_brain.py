from conny_responses import RESPONSES
import datetime
from conny_calculator import calculate


def get_response(user_input):

    text = user_input.lower().strip()


    # Goodbye detection
    goodbye_words = [
        "bye",
        "goodbye",
        "good bye",
        "ok bye",
        "okay bye",
        "see you",
        "exit",
        "quit"
    ]

    if text in goodbye_words:
        return "EXIT"


    # Greetings
    greetings = [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good evening"
    ]

    if text in greetings:
        return RESPONSES["hello"]


    # Calculator
    if "calculate" in text:

        expression = text.replace("calculate", "").strip()

        return calculate(expression)


    # Time
    if "time" in text:
        return datetime.datetime.now().strftime(
            "The current time is %H:%M:%S"
        )


    # Date
    if "date" in text:
        return str(datetime.date.today())


    # Study questions
    if "study" in text or "studying" in text:
        return (
            "I like learning technology, programming, "
            "electronics, networking and artificial intelligence."
        )


    # Search known responses
    for key in RESPONSES:

        if key in text:
            return RESPONSES[key]


    # Unknown
    return (
        "I am still learning.\n"
        "Every great intelligence starts by learning."
    )

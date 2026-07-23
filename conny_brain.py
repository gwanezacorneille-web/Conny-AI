from conny_responses import RESPONSES
import datetime
from conny_calculator import calculate
from conny_memory import remember, get_memory, forget


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

    for word in goodbye_words:
        if word in text:
            return "EXIT"



    # Greetings

    greetings = [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good evening",
        "good afternoon"
    ]

    for greeting in greetings:
        if greeting in text:
            return RESPONSES["hello"]



    # Help command

    if "help" in text or "what can you do" in text:
        return RESPONSES["help"]



    # Calculator

    if "calculate" in text:

        expression = text.replace(
            "calculate",
            ""
        ).strip()

        return calculate(expression)



    # Time

    if "time" in text:

        return datetime.datetime.now().strftime(
            "The current time is %H:%M:%S"
        )



    # Date

    if "date" in text:

        return (
            "Today's date is "
            + str(datetime.date.today())
        )



    # Study

    if "study" in text or "studying" in text:

        return RESPONSES["study"]



    # Search known responses

    for key in RESPONSES:

        if key in text:

            return RESPONSES[key]



    # Unknown

    return (
        "I am still learning, Corneille 🤖\n"
        "Try asking another question, "
        "and I will continue improving."
    )

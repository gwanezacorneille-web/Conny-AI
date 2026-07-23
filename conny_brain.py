from conny_responses import RESPONSES
from conny_network import is_online
from conny_online import search_online
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


    # Memory save

    if text.startswith("remember "):

        fact = text.replace(
            "remember ",
            "",
            1
        ).strip()


        category = "knowledge"


        if "my name" in fact:
            category = "personal"

        elif "i like" in fact or "i love" in fact:
            category = "interests"

        elif "project" in fact or "conny" in fact:
            category = "projects"


        remember(
            fact,
            category
        )


        return "I will remember that. 🧠"



    # Show memory

    if "what do you remember" in text or "show my memories" in text:

        memories = get_memory()


        if memories:

            return (
                "🧠 My memories:\n\n"
                + "\n".join(memories)
            )

        else:

            return "I don't remember anything yet."



    # Forget memory

    if text.startswith("forget "):

        fact = text.replace(
            "forget ",
            "",
            1
        ).strip()


        forget(fact)


        return "Memory removed. 🗑️"



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


    # Online search

    if is_online():

        online_answer = search_online(text)

        if online_answer not in (
            "I couldn't find a good answer online.",
            "I couldn't connect to the online knowledge service."
        ):
            return "🌐 Online Result:\n\n" + online_answer


    # Unknown

    return (
        "I am still learning, Corneille 🤖\n"
        "If I'm connected to the internet, I can also search online for newer information."
    )

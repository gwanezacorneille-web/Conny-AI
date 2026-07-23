from conny_memory import remember, get_memory, forget


def handle_memory(text):

    text = text.lower().strip()


    # Remember

    if text.startswith("remember "):

        fact = text.replace(
            "remember ",
            "",
            1
        ).strip()


        remember(fact)

        return "I will remember that. 🧠"



    # Recall

    if (
        "what do you remember" in text
        or "show my memories" in text
    ):

        memories = get_memory()


        if memories:

            return (
                "🧠 My memories:\n\n"
                + "\n".join(memories)
            )

        else:

            return "I don't remember anything yet."



    # Forget

    if text.startswith("forget "):

        fact = text.replace(
            "forget ",
            "",
            1
        ).strip()


        forget(fact)

        return "Memory removed. 🗑️"


    return None

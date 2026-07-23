from conny_memory import remember, get_memory, forget
from modules.profile_manager import update_profile, get_profile


def handle_memory(text):

    text = text.lower().strip()


    # Remember

    if text.startswith("remember "):

        fact = text.replace(
            "remember ",
            "",
            1
        ).strip()


        # Name detection

        if fact.startswith("my name is"):

            name = fact.replace(
                "my name is",
                ""
            ).strip()

            update_profile(
                "name",
                name
            )


        # Interest detection

        elif "i like" in fact:

            interest = fact.replace(
                "i like",
                ""
            ).strip()

            update_profile(
                "interests",
                interest
            )


        # Study detection

        elif "i study" in fact:

            study = fact.replace(
                "i study",
                ""
            ).strip()

            update_profile(
                "studies",
                study
            )


        # Project detection

        elif "i am building" in fact:

            project = fact.replace(
                "i am building",
                ""
            ).strip()

            update_profile(
                "projects",
                project
            )


        else:

            remember(fact)


        return "I will remember that. 🧠"



    # Profile recall

    if (
        "who am i" in text
        or "what is my profile" in text
    ):

        profile = get_profile()

        return (
            "🧠 Your profile:\n\n"
            f"Name: {profile['name']}\n"
            f"Interests: {profile['interests']}\n"
            f"Studies: {profile['studies']}\n"
            f"Projects: {profile['projects']}"
        )



    # Old memory recall

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

from conny_network import is_online
from modules.search_manager import search_knowledge


def handle_online(text):

    # Built-in knowledge fallback

    knowledge = {

        "who created linux":
        "Linux was created by Linus Torvalds in 1991. "
        "He started the Linux kernel project while he was a student.",


        "who is linus torvalds":
        "Linus Torvalds is the creator and lead developer of the Linux kernel.",


        "what is python":
        "Python is a high-level programming language created by Guido van Rossum and first released in 1991."
    }


    for question, answer in knowledge.items():

        if question in text:

            return (
                "🌐 Online Result:\n\n"
                + answer
            )



    if not is_online():

        return None



    answer = search_knowledge(text)


    if not answer:

        return None


    return (
        "🌐 Online Result:\n\n"
        + answer
    )

from modules.memory_manager import handle_memory
from modules.calculator import handle_calculation
from modules.conversation import handle_conversation
from modules.online_search import handle_online


def get_response(user_input):

    text = user_input.lower().strip()


    modules = [
        handle_memory,
        handle_calculation,
        handle_conversation,
        handle_online
    ]


    for module in modules:

        try:

            response = module(text)

            if response:
                return response

        except Exception as error:

            print("Module error:", error)



    return (
        "I am still learning, Corneille 🤖\n"
        "Try asking another question."
    )

from modules.memory_manager import handle_memory
from modules.calculator import handle_calculation
from modules.conversation import handle_conversation
from modules.online_search import handle_online
from modules.context_manager import update_context
from modules.intent_analyzer import detect_intent


def get_response(user_input):

    text = user_input.lower().strip()

    intent = detect_intent(text)

    try:

        if intent == "memory":

            response = handle_memory(text)

        elif intent == "calculator":

            response = handle_calculation(text)

        elif intent == "online":

            response = handle_online(text)

        else:

            response = handle_conversation(text)

        if response:

            update_context(
                text,
                response
            )

            return response

    except Exception as error:

        print("Module error:", error)

    return (
        "I am still learning, Corneille 🤖\n"
        "Try asking another question."
    )

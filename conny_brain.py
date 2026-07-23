from modules.memory_manager import handle_memory
from modules.calculator import handle_calculation
from modules.conversation import handle_conversation
from modules.online_search import handle_online
from modules.context_manager import update_context
from modules.context_reasoning import handle_context
from modules.intent_analyzer import detect_intent



def get_response(user_input):

    text = user_input.lower().strip()


    try:

        # 1. Check previous conversation context first

        context_response = handle_context(text)

        if context_response:

            update_context(
                text,
                context_response
            )

            return context_response



        # 2. Detect user intention

        intent = detect_intent(text)



        # 3. Select correct module

        if intent == "memory":

            response = handle_memory(text)


        elif intent == "calculator":

            response = handle_calculation(text)


        elif intent == "online":

            response = handle_online(text)


        else:

            response = handle_conversation(text)



        # 4. Save useful conversation context

        if response:


            ignored_words = [
                "hello",
                "hi",
                "hey",
                "i am still learning",
                "try asking another question"
            ]


            save_context = True


            for word in ignored_words:

                if word in text:

                    save_context = False



            if (
                save_context
                and not response.startswith(
                    "🧠 Continuing from our previous topic:"
                )
            ):

                update_context(
                    text,
                    response
                )


            return response



    except Exception as error:

        print(
            "Module error:",
            error
        )



    return (
        "I am still learning, Corneille 🤖\n"
        "Try asking another question."
    )

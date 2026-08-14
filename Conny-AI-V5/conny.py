from brain.brain import Brain
from config import APP_NAME, VERSION


conny = Brain()


print("==========================")
print(APP_NAME)
print(VERSION)
print("==========================")


while True:

    user = input("\nYou: ")


    if user.lower() == "exit":

        print("Conny: Goodbye!")
        break



    # ==============================
    # TEACH MODE MULTI-LINE INPUT
    # ==============================

    if (
        user.lower().startswith("study ")
        or user.lower().startswith("teach ")
        or user.lower().startswith("learn ")
    ):

        reply = conny.process(user)

        print("Conny:", reply)


        print("\nPaste your lesson below.")
        print("Type END on a new line when finished.\n")


        lesson_lines = []


        while True:

            line = input()


            if line.strip().upper() == "END":

                break


            lesson_lines.append(line)



        for line in lesson_lines:

            conny.learning.process_input(line)



        result = conny.learning.process_input("END")


        if result and result.get("type") == "lesson_complete":

            knowledge = result["knowledge"]


            print(
                "\nConny:"
                "\n=============================="
                "\nLearning Complete"
                "\n=============================="
                f"\nTopic: {knowledge.topic}"
                f"\nFacts found: {len(knowledge.facts)}"
                f"\nKeywords found: {len(knowledge.keywords)}"
                "\n\nReady for storage."
            )


        continue



    # ==============================
    # NORMAL CHAT
    # ==============================


    reply = conny.process(user)


    print(
        "Conny:",
        reply
    )

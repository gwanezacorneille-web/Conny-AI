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


    reply = conny.process(user)


    print(
        "Conny:",
        reply
    )

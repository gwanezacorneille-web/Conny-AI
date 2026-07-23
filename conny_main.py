from conny_brain import get_response
from conny_network import is_online
from conny_memory import remember, get_memory
import time


# ==============================
#        CONNY AI
# From a small idea to a global intelligence.
#
# Created by:
# Gwaneza Corneille Karenzi
# ==============================


print("=" * 55)
print("                 CONNY AI")
print("  From a small idea to a global intelligence.")
print()
print("  Created by Gwaneza Corneille Karenzi")
print("=" * 55)


print("\n[✓] Loading Core...")
time.sleep(0.5)

print("[✓] Loading Brain...")
time.sleep(0.5)

print("[✓] Loading Memory...")
time.sleep(0.5)

print("[✓] Checking Network...")
time.sleep(0.5)


ONLINE = is_online()


if ONLINE:
    print("\nStatus : 🟢 ONLINE")
else:
    print("\nStatus : 🔴 OFFLINE")


name = input("\nWhat is your name? ")


print(f"\nWelcome {name}!")
print("I am Conny AI.")
print()
print("Commands:")
print("- remember something")
print("- what do you remember")
print("- bye")
print()


while True:

    user = input(f"{name}: ").lower().strip()


    # Exit
    if user in ["bye", "exit", "quit", "goodbye"]:

        print(f"\nConny AI: Goodbye {name}! 👋")
        break



    # Save memory
    elif user.startswith("remember "):

        fact = user.replace("remember ", "", 1)

        remember(fact)

        print("\nConny AI: I will remember that.")

        continue



    # Show memory
    elif "what do you remember" in user:

        facts = get_memory()


        if facts:

            print("\nConny AI remembers:")

            for fact in facts:
                print("-", fact)

        else:

            print("\nConny AI: I don't remember anything yet.")


        continue



    # Internet questions
    elif any(word in user for word in ["search", "latest", "news", "weather"]):

        if ONLINE:

            print("\nConny AI: Internet features will be added soon.")

        else:

            print("\nConny AI: Sorry, but you need to be connected to a network to receive the answers you need.")


        continue



        # Normal AI response
    answer = get_response(user)

    if answer == "EXIT":
        print(f"\nConny AI: Goodbye {name}! 👋")
        break

    print("\nConny AI:", answer)

import json
import os


MEMORY_FILE = "memory/memory.json"


def load_memory():

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    else:

        return {
            "facts": []
        }



def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:

        json.dump(memory, file, indent=4)



def remember(fact):

    memory = load_memory()

    memory["facts"].append(fact)

    save_memory(memory)



def get_memory():

    memory = load_memory()

    return memory["facts"]

import json
import os


MEMORY_FILE = "memory/memory.json"


DEFAULT_MEMORY = {
    "personal": [],
    "interests": [],
    "projects": [],
    "knowledge": []
}


def load_memory():

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    else:

        save_memory(DEFAULT_MEMORY)

        return DEFAULT_MEMORY



def save_memory(memory):

    os.makedirs(
        "memory",
        exist_ok=True
    )

    with open(MEMORY_FILE, "w") as file:

        json.dump(
            memory,
            file,
            indent=4
        )



def remember(fact, category="knowledge"):

    memory = load_memory()


    if category not in memory:

        category = "knowledge"


    if fact not in memory[category]:

        memory[category].append(fact)


    save_memory(memory)



def get_memory():

    memory = load_memory()

    memories = []


    for category, facts in memory.items():

        for fact in facts:

            memories.append(
                f"{category}: {fact}"
            )


    return memories



def forget(fact):

    memory = load_memory()


    for category in memory:

        if fact in memory[category]:

            memory[category].remove(fact)


    save_memory(memory)

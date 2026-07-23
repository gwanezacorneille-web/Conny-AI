import json
import os


CONTEXT_FILE = "memory/context.json"


DEFAULT_CONTEXT = {
    "topic": "",
    "category": "",
    "question": "",
    "answer": ""
}


def load_context():

    if os.path.exists(CONTEXT_FILE):

        with open(CONTEXT_FILE, "r") as file:
            return json.load(file)

    return DEFAULT_CONTEXT



def save_context(context):

    os.makedirs(
        "memory",
        exist_ok=True
    )

    with open(CONTEXT_FILE, "w") as file:

        json.dump(
            context,
            file,
            indent=4
        )



def update_context(question, answer):

    context = {
        "topic": question,
        "category": "general",
        "question": question,
        "answer": answer
    }

    save_context(context)



def get_context():

    return load_context()

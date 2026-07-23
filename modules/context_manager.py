import json
import os


CONTEXT_FILE = "memory/context.json"


def load_context():

    if os.path.exists(CONTEXT_FILE):

        with open(CONTEXT_FILE, "r") as file:
            return json.load(file)

    return {
        "last_topic": "",
        "last_response": ""
    }



def save_context(context):

    with open(CONTEXT_FILE, "w") as file:

        json.dump(
            context,
            file,
            indent=4
        )



def update_context(topic, response):

    context = {
        "last_topic": topic,
        "last_response": response
    }

    save_context(context)



def get_context():

    return load_context()

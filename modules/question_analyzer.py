def analyze_question(text):

    text = text.lower().strip()

    patterns = {

        "who created": "creator",
        "who invented": "inventor",
        "who made": "creator",

        "who is": "person",

        "what is": "definition",
        "what are": "definition",

        "when was": "date",

        "where is": "location",

        "tell me about": "information",

        "define": "definition"

    }

    for pattern, question_type in patterns.items():

        if text.startswith(pattern):

            subject = text.replace(
                pattern,
                "",
                1
            ).strip()

            return {

                "type": question_type,

                "subject": subject

            }

    return {

        "type": "general",

        "subject": text

    }

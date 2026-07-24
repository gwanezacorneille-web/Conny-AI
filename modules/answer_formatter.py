def format_answer(question_type, answer):

    if not answer:
        return None

    sentences = answer.split(". ")

    if question_type == "definition":
        return sentences[0] + "."

    if question_type == "creator":

        keywords = [
            "created",
            "developed",
            "invented",
            "written",
            "released by",
            "by "
        ]

        for sentence in sentences:

            lower = sentence.lower()

            if any(word in lower for word in keywords):
                return sentence.strip() + "."

    if question_type == "date":

        for sentence in sentences:

            if any(str(year) in sentence for year in range(1900, 2101)):
                return sentence.strip() + "."

    if question_type == "person":
        return sentences[0] + "."

    if question_type == "location":

        for sentence in sentences:

            lower = sentence.lower()

            if (
                "located" in lower
                or " in " in lower
            ):
                return sentence.strip() + "."

    return sentences[0] + "."

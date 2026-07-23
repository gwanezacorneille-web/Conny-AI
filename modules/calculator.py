from conny_calculator import calculate


def handle_calculation(text):

    text = text.lower().strip()


    if "calculate" in text:

        expression = text.replace(
            "calculate",
            ""
        ).strip()

        return calculate(expression)


    return None

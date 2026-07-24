class CalculatorPlugin:


    def can_handle(self, message):

        text = message.lower()


        if "calculate" in text:

            return True


        if any(symbol in text for symbol in [
            "+",
            "-",
            "*",
            "/"
        ]):

            numbers = any(
                char.isdigit()
                for char in text
            )

            return numbers


        return False



    def run(self, message):

        try:

            expression = message.lower()


            expression = expression.replace(
                "calculate",
                ""
            )


            expression = expression.strip()


            result = eval(expression)


            return (
                f"The answer is {result}."
            )


        except:

            return (
                "I could not calculate that."
            )

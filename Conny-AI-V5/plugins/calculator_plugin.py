class CalculatorPlugin:


    def can_handle(self, message):

        message = message.lower()


        keywords = [
            "calculate",
            "what is",
            "+",
            "-",
            "*",
            "/"
        ]


        for word in keywords:

            if word in message:

                return True


        return False



    def run(self, message):

        try:

            expression = message.lower()


            expression = expression.replace(
                "calculate",
                ""
            )


            expression = expression.replace(
                "what is",
                ""
            )


            result = eval(expression)


            return (
                f"The answer is {result}."
            )


        except:

            return (
                "I could not calculate that."
            )

class Reasoning:

    def analyze(self, text):

        text = str(text).strip().lower()

        # ==============================================
        # SIMPLE ARITHMETIC REASONING
        # ==============================================

        if (
            "how many" in text
            and "have left" in text
        ):
            import re

            numbers = [
                int(value)
                for value in re.findall(
                    r"\d+",
                    text
                )
            ]

            if len(numbers) >= 2:
                result = numbers[0] - numbers[1]

                return (
                    f"You have {result} left."
                )

        # ==============================================
        # PHYSICS: FALLING OBJECTS
        # ==============================================

        if (
            "heavier object" in text
            and "fall faster" in text
        ):
            return (
                "In a vacuum, objects fall with the same "
                "gravitational acceleration regardless of "
                "their mass. In air, a heavier object may "
                "fall differently because air resistance "
                "affects objects differently depending on "
                "their shape, size, and speed."
            )

        # ==============================================
        # GREETINGS
        # ==============================================

        if any(
            word in text
            for word in (
                "hello",
                "hi",
                "hey"
            )
        ):
            return "greeting"

        # ==============================================
        # IDENTITY
        # ==============================================

        if (
            "who are you" in text
            or "your name" in text
        ):
            return "name"

        # ==============================================
        # MEMORY-LIKE REASONING
        # ==============================================

        if "my favourite language is" in text:
            return "favorite_language"

        if "i study" in text:
            return "study"

        return None

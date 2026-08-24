import re
import math


class CalculatorEngine:
    """
    CONNY V10 Calculator Engine

    Handles natural-language arithmetic such as:
        10 plus 5
        25 minus 7
        6 multiplied by 7
        42 divided by 6
        average of 10 and 20
        highest of 4, 9 and 2
        lowest of 4, 9 and 2
        square root of 25
        5 squared
        5 cubed
        2 to the power of 3
    """

    def calculate(self, text):
        text = text.lower().strip()

        # -------------------------
        # NUMBERS
        # -------------------------
        numbers = [
            float(x)
            for x in re.findall(r"\d+(?:\.\d+)?", text)
        ]

        if not numbers:
            return None

        # -------------------------
        # AVERAGE / MEAN
        # -------------------------
        if "average of" in text or "mean of" in text:
            return sum(numbers) / len(numbers)

        # -------------------------
        # HIGHEST / MAXIMUM
        # -------------------------
        if (
            "highest of" in text
            or "maximum of" in text
            or "largest of" in text
        ):
            return max(numbers)

        # -------------------------
        # LOWEST / MINIMUM
        # -------------------------
        if (
            "lowest of" in text
            or "minimum of" in text
            or "smallest of" in text
        ):
            return min(numbers)

        # -------------------------
        # SQUARE ROOT
        # -------------------------
        if "square root" in text:
            return math.sqrt(numbers[-1])

        # -------------------------
        # SQUARED
        # -------------------------
        if "squared" in text:
            return numbers[0] ** 2

        # -------------------------
        # CUBED
        # -------------------------
        if "cubed" in text:
            return numbers[0] ** 3

        # -------------------------
        # POWER
        # -------------------------
        if "to the power" in text or "power of" in text:
            if len(numbers) >= 2:
                return numbers[0] ** numbers[1]

        # -------------------------
        # ADDITION
        # -------------------------
        if " plus " in f" {text} ":
            if len(numbers) >= 2:
                return numbers[0] + numbers[1]

        # -------------------------
        # SUBTRACTION
        # -------------------------
        if " minus " in f" {text} ":
            if len(numbers) >= 2:
                return numbers[0] - numbers[1]

        # -------------------------
        # MULTIPLICATION
        # -------------------------
        if (
            " multiplied by " in text
            or " times " in text
        ):
            if len(numbers) >= 2:
                return numbers[0] * numbers[1]

        # -------------------------
        # DIVISION
        # -------------------------
        if " divided by " in text:
            if len(numbers) >= 2:
                if numbers[1] == 0:
                    return "I can't divide by zero."
                return numbers[0] / numbers[1]

        return None

    def format_result(self, result):
        if result is None:
            return "I could not calculate that."

        if isinstance(result, float) and result.is_integer():
            return str(int(result))

        return str(result)

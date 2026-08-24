import ast
import operator
import re
import math


class CalculatorPlugin:

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    # ==================================================
    # CAN HANDLE
    # ==================================================

    def can_handle(self, message):

        text = str(message).lower().strip()

        if not text:
            return False

        if "calculate" in text:
            return True

        if any(
            symbol in text
            for symbol in ["+", "-", "*", "/", "%", "^"]
        ):
            return any(
                char.isdigit()
                for char in text
            )

        natural_math = (
            "average of",
            "mean of",
            "sum of",
            "total of",
            "product of",
            "quotient of",
            "difference between",
            "difference of",
            "maximum of",
            "minimum of",
            "highest of",
            "lowest of",
            "square root",
            "square of",
            "cube of",
            "power of",
            "to the power",
            "increase",
            "decrease",
            "percentage",
            "percent",
        )

        if any(
            phrase in text
            for phrase in natural_math
        ):
            return any(
                char.isdigit()
                for char in text
            )

        return False

    # ==================================================
    # FORMAT RESULT
    # ==================================================

    def _format_result(self, result):

        if isinstance(result, float):

            result = round(result, 10)

            if result.is_integer():
                return int(result)

        return result

    # ==================================================
    # EXTRACT NUMBERS
    # ==================================================

    def _numbers(self, expression):

        return [
            float(value)
            for value in re.findall(
                r"-?\d+(?:\.\d+)?",
                expression
            )
        ]

    # ==================================================
    # SAFE EVALUATION
    # ==================================================

    def _evaluate(self, expression):

        tree = ast.parse(
            expression,
            mode="eval"
        )

        return self._evaluate_node(
            tree.body
        )

    # ==================================================
    # EVALUATE NODE
    # ==================================================

    def _evaluate_node(self, node):

        if isinstance(node, ast.Constant):

            if isinstance(
                node.value,
                (int, float)
            ):
                return node.value

            raise ValueError(
                "Invalid value"
            )

        if isinstance(node, ast.BinOp):

            operation = self.OPERATORS.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError(
                    "Invalid operator"
                )

            left = self._evaluate_node(
                node.left
            )

            right = self._evaluate_node(
                node.right
            )

            return operation(
                left,
                right
            )

        if isinstance(node, ast.UnaryOp):

            operation = self.OPERATORS.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError(
                    "Invalid operator"
                )

            value = self._evaluate_node(
                node.operand
            )

            return operation(
                value
            )

        raise ValueError(
            "Invalid expression"
        )

    # ==================================================
    # RUN
    # ==================================================

    def run(self, message):

        try:

            expression = (
                str(message)
                .lower()
                .replace("calculate", "")
                .strip()
            )

            # ==================================================
            # PERCENTAGE OF
            # ==================================================

            percentage_match = re.search(
                r"(-?\d+(?:\.\d+)?)\s*%\s*of\s*"
                r"(-?\d+(?:\.\d+)?)",
                expression
            )

            if percentage_match:

                percentage = float(
                    percentage_match.group(1)
                )

                number = float(
                    percentage_match.group(2)
                )

                result = (
                    percentage / 100
                ) * number

                result = self._format_result(
                    result
                )

                return (
                    f"The answer is {result}."
                )

            # ==================================================
            # PERCENTAGE INCREASE
            # ==================================================

            increase_match = re.search(
                r"increase\s+"
                r"(-?\d+(?:\.\d+)?)\s+"
                r"by\s+"
                r"(\d+(?:\.\d+)?)\s*%",
                expression
            )

            if increase_match:

                number = float(
                    increase_match.group(1)
                )

                percentage = float(
                    increase_match.group(2)
                )

                result = number * (
                    1 + percentage / 100
                )

                result = self._format_result(
                    result
                )

                return (
                    f"After the increase, "
                    f"the answer is {result}."
                )

            # ==================================================
            # PERCENTAGE DECREASE
            # ==================================================

            decrease_match = re.search(
                r"decrease\s+"
                r"(-?\d+(?:\.\d+)?)\s+"
                r"by\s+"
                r"(\d+(?:\.\d+)?)\s*%",
                expression
            )

            if decrease_match:

                number = float(
                    decrease_match.group(1)
                )

                percentage = float(
                    decrease_match.group(2)
                )

                result = number * (
                    1 - percentage / 100
                )

                result = self._format_result(
                    result
                )

                return (
                    f"After the decrease, "
                    f"the answer is {result}."
                )

            # ==================================================
            # SQUARE ROOT
            # ==================================================

            square_root_match = re.search(
                r"square\s+root\s+"
                r"(?:of\s+)?"
                r"(-?\d+(?:\.\d+)?)",
                expression
            )

            if square_root_match:

                number = float(
                    square_root_match.group(1)
                )

                if number < 0:

                    return (
                        "I cannot calculate the "
                        "square root of a negative number."
                    )

                result = math.sqrt(
                    number
                )

                result = self._format_result(
                    result
                )

                return (
                    f"The square root is {result}."
                )

            # ==================================================
            # SQUARE
            # ==================================================

            square_match = re.search(
                r"square\s+of\s+"
                r"(-?\d+(?:\.\d+)?)",
                expression
            )

            if square_match:

                number = float(
                    square_match.group(1)
                )

                result = number ** 2

                result = self._format_result(
                    result
                )

                return (
                    f"The square is {result}."
                )

            # ==================================================
            # CUBE
            # ==================================================

            cube_match = re.search(
                r"cube\s+of\s+"
                r"(-?\d+(?:\.\d+)?)",
                expression
            )

            if cube_match:

                number = float(
                    cube_match.group(1)
                )

                result = number ** 3

                result = self._format_result(
                    result
                )

                return (
                    f"The cube is {result}."
                )

            # ==================================================
            # POWER
            # ==================================================

            power_match = re.search(
                r"(-?\d+(?:\.\d+)?)\s+"
                r"(?:to\s+the\s+power\s+of|"
                r"to\s+the\s+power|"
                r"power\s+of)\s+"
                r"(-?\d+(?:\.\d+)?)",
                expression
            )

            if power_match:

                base = float(
                    power_match.group(1)
                )

                exponent = float(
                    power_match.group(2)
                )

                result = base ** exponent

                result = self._format_result(
                    result
                )

                return (
                    f"The answer is {result}."
                )

            # ==================================================
            # AVERAGE / MEAN
            # ==================================================

            if (
                "average of" in expression
                or "mean of" in expression
            ):

                numbers = self._numbers(
                    expression
                )

                if numbers:

                    result = (
                        sum(numbers)
                        / len(numbers)
                    )

                    result = self._format_result(
                        result
                    )

                    return (
                        f"The average is {result}."
                    )

            # ==================================================
            # SUM / TOTAL
            # ==================================================

            if (
                "sum of" in expression
                or "total of" in expression
            ):

                numbers = self._numbers(
                    expression
                )

                if numbers:

                    result = sum(numbers)

                    result = self._format_result(
                        result
                    )

                    return (
                        f"The sum is {result}."
                    )

            # ==================================================
            # MAXIMUM / HIGHEST
            # ==================================================

            if (
                "maximum of" in expression
                or "highest of" in expression
            ):

                numbers = self._numbers(
                    expression
                )

                if numbers:

                    result = max(numbers)

                    result = self._format_result(
                        result
                    )

                    return (
                        f"The maximum is {result}."
                    )

            # ==================================================
            # MINIMUM / LOWEST
            # ==================================================

            if (
                "minimum of" in expression
                or "lowest of" in expression
            ):

                numbers = self._numbers(
                    expression
                )

                if numbers:

                    result = min(numbers)

                    result = self._format_result(
                        result
                    )

                    return (
                        f"The minimum is {result}."
                    )

            # ==================================================
            # PRODUCT
            # ==================================================

            if "product of" in expression:

                numbers = self._numbers(
                    expression
                )

                if len(numbers) >= 2:

                    result = numbers[0]

                    for number in numbers[1:]:
                        result *= number

                    result = self._format_result(
                        result
                    )

                    return (
                        f"The product is {result}."
                    )

            # ==================================================
            # QUOTIENT
            # ==================================================

            if "quotient of" in expression:

                numbers = self._numbers(
                    expression
                )

                if len(numbers) >= 2:

                    if numbers[1] == 0:

                        return (
                            "I cannot divide by zero."
                        )

                    result = (
                        numbers[0]
                        / numbers[1]
                    )

                    result = self._format_result(
                        result
                    )

                    return (
                        f"The quotient is {result}."
                    )

            # ==================================================
            # DIFFERENCE
            # ==================================================

            if (
                "difference between" in expression
                or "difference of" in expression
            ):

                numbers = self._numbers(
                    expression
                )

                if len(numbers) >= 2:

                    result = abs(
                        numbers[0]
                        - numbers[1]
                    )

                    result = self._format_result(
                        result
                    )

                    return (
                        f"The difference is {result}."
                    )

            # ==================================================
            # STANDARD EXPRESSION
            # ==================================================

            expression = expression.replace(
                "^",
                "**"
            )

            result = self._evaluate(
                expression
            )

            result = self._format_result(
                result
            )

            return (
                f"The answer is {result}."
            )

        except ZeroDivisionError:

            return (
                "I cannot divide by zero."
            )

        except Exception:

            return (
                "I could not calculate that."
            )

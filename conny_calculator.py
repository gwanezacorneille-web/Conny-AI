def calculate(expression):

    try:
        # Allow only numbers and basic operators
        allowed = "0123456789+-*/(). "

        for char in expression:

            if char not in allowed:
                return "I can only calculate numbers and basic operations."

        result = eval(expression)

        return f"{expression} = {result}"

    except:

        return "Sorry, I could not calculate that."

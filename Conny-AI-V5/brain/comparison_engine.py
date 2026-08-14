class ComparisonEngine:


    def compare(self, first, second):

        if first is None or second is None:

            return "I could not compare those concepts."


        first_name = first["name"].upper()
        second_name = second["name"].upper()

        first_data = first["data"]
        second_data = second["data"]


        reply = ""

        reply += f"{first_name} vs {second_name}\n\n"


        reply += f"{first_name}:\n"

        reply += first_data.get(
            "definition",
            first_data.get("answer", "")
        )

        reply += "\n\n"


        reply += f"{second_name}:\n"

        reply += second_data.get(
            "definition",
            second_data.get("answer", "")
        )

        reply += "\n\n"


        reply += "Main functions:\n\n"


        reply += f"{first_name}:\n"

        for item in first_data.get("functions", []):

            reply += f"- {item}\n"


        reply += "\n"


        reply += f"{second_name}:\n"

        for item in second_data.get("functions", []):

            reply += f"- {item}\n"


        return reply

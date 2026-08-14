class ExplanationEngine:


    def generate(self, intent, concept):

        if concept is None:
            return None

        name = concept["name"]
        data = concept["data"]


        if intent == "definition":

            return data.get(
                "definition",
                data.get("answer", "I don't know.")
            )


        if intent == "functions":

            functions = data.get("functions")

            if functions:

                return (
                    "Functions:\n- "
                    + "\n- ".join(functions)
                )


        if intent == "examples":

            examples = data.get("examples")

            if examples:

                return (
                    "Examples:\n- "
                    + "\n- ".join(examples)
                )


        if intent == "explanation":

            text = (
                f"{name.upper()} explained simply:\n\n"
            )

            text += data.get(
                "definition",
                data.get("answer", "")
            )


            functions = data.get("functions")

            if functions:

                text += "\n\nIt is used to:\n"

                for item in functions:

                    text += f"- {item}\n"

            return text


        if intent == "comparison":

            return (
                "Comparison mode is not implemented yet."
            )


        if intent == "reason":

            return (
                "Reasoning mode is coming soon."
            )


        return data.get(
            "definition",
            data.get("answer", "I don't know.")
        )

import re


class Reasoning:

    def analyze(self, text):

        text = str(text).strip().lower()

        # ==============================================
        # SIMPLE SUBTRACTION / "HOW MANY LEFT"
        # ==============================================

        if (
            "how many" in text
            and "have left" in text
        ):

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
        # SIMPLE ADDITION
        # ==============================================

        if (
            "how many" in text
            and (
                "altogether" in text
                or "in total" in text
                or "total" in text
            )
        ):

            numbers = [
                int(value)
                for value in re.findall(
                    r"\d+",
                    text
                )
            ]

            if len(numbers) >= 2:

                result = numbers[0] + numbers[1]

                return (
                    f"You have {result} in total."
                )

        # ==============================================
        # COMPARISON
        # ==============================================

        if (
            "which is greater" in text
            or "which is bigger" in text
            or "which is larger" in text
        ):

            numbers = [
                int(value)
                for value in re.findall(
                    r"\d+",
                    text
                )
            ]

            if len(numbers) >= 2:

                if numbers[0] > numbers[1]:

                    return (
                        f"{numbers[0]} is greater than "
                        f"{numbers[1]}."
                    )

                if numbers[1] > numbers[0]:

                    return (
                        f"{numbers[1]} is greater than "
                        f"{numbers[0]}."
                    )

                return "The two numbers are equal."

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
        # PHYSICS: WHY DOES ICE FLOAT?
        # ==============================================

        if (
            "why does ice float" in text
            or "why ice floats" in text
            or "why does ice float on water" in text
        ):

            return (
                "Ice floats because it is less dense than "
                "liquid water. When water freezes, its "
                "molecules form an open crystal structure "
                "that takes up more space. This makes ice "
                "less dense than liquid water, so the ice "
                "floats."
            )

        # ==============================================
        # PHYSICS: METAL CONDUCTIVITY
        # ==============================================

        if (
            "why does metal conduct" in text
            or "why do metals conduct" in text
            or "why is metal conductive" in text
        ):

            return (
                "Metals conduct electricity well because "
                "they contain electrons that can move "
                "relatively freely through the material. "
                "When an electric field is applied, these "
                "electrons move and produce electric current."
            )

        # ==============================================
        # PHYSICS: BALLOON
        # ==============================================

        if (
            "why does a balloon rise" in text
            or "why does a balloon float" in text
            or "why do balloons rise" in text
        ):

            return (
                "A balloon rises when the air or gas inside "
                "it makes the balloon's average density lower "
                "than the surrounding air. The upward buoyant "
                "force from the surrounding air can then "
                "exceed the balloon's weight."
            )

        # ==============================================
        # PROCESS: REFRIGERATOR
        # ==============================================

        if (
            "how does a refrigerator work" in text
            or "how does a fridge work" in text
            or "how does refrigerator work" in text
            or "how does fridge work" in text
        ):

            return (
                "A refrigerator removes heat from inside the "
                "cabinet and releases that heat into the "
                "surrounding room.\n\n"
                "The basic refrigeration cycle is:\n"
                "1. Compressor — compresses the refrigerant "
                "and raises its pressure and temperature.\n"
                "2. Condenser — releases heat to the room "
                "and turns the refrigerant into a liquid.\n"
                "3. Expansion device — reduces the refrigerant "
                "pressure and temperature.\n"
                "4. Evaporator — the cold refrigerant absorbs "
                "heat from inside the refrigerator.\n"
                "5. The refrigerant returns to the compressor "
                "and the cycle repeats."
            )

        # ==============================================
        # PROCESS: TRANSISTOR
        # ==============================================

        if (
            "how does a transistor work" in text
            or "how do transistors work" in text
        ):

            return (
                "A transistor controls the flow of electrical "
                "current using a small electrical signal. "
                "Depending on how it is connected, a "
                "transistor can operate as an electronic "
                "switch or as an amplifier."
            )

        # ==============================================
        # PROCESS: TRANSFORMER
        # ==============================================

        if (
            "how does a transformer work" in text
            or "how do transformers work" in text
        ):

            return (
                "A transformer transfers electrical energy "
                "between coils using electromagnetic "
                "induction. An alternating current in the "
                "primary coil creates a changing magnetic "
                "field, which induces a voltage in the "
                "secondary coil.\n\n"
                "A transformer can increase or decrease "
                "AC voltage depending on the turns ratio "
                "between the two coils."
            )

        # ==============================================
        # PROCESS: ELECTRIC MOTOR
        # ==============================================

        if (
            "how does a motor work" in text
            or "how does an electric motor work" in text
            or "how do electric motors work" in text
        ):

            return (
                "An electric motor converts electrical energy "
                "into mechanical motion. Current flowing "
                "through conductors in a magnetic field "
                "creates a force. The arrangement of the "
                "magnetic field and current produces torque, "
                "which turns the motor shaft."
            )

        # ==============================================
        # PROCESS: GENERATOR
        # ==============================================

        if (
            "how does a generator work" in text
            or "how do generators work" in text
        ):

            return (
                "A generator converts mechanical energy into "
                "electrical energy using electromagnetic "
                "induction. When a conductor moves through "
                "a magnetic field, a voltage is induced in "
                "the conductor."
            )

        # ==============================================
        # PHYSICS: SKY IS BLUE
        # ==============================================

        if (
            "why does the sky look blue" in text
            or "why is the sky blue" in text
            or "why does the sky appear blue" in text
            or "why sky is blue" in text
        ):

            return (
                "The sky looks blue because Earth's atmosphere "
                "scatters sunlight. Blue light has a shorter "
                "wavelength and is scattered more strongly than "
                "most other visible colors, so blue light reaches "
                "our eyes from many directions."
            )

        # ==============================================
        # OCEAN: WHY IS THE OCEAN SALTY?
        # ==============================================

        if (
            "why is the ocean salty" in text
            or "why are oceans salty" in text
            or "why is seawater salty" in text
            or "why is sea water salty" in text
        ):

            return (
                "The ocean is salty because minerals and dissolved "
                "salts are carried into the oceans by rivers, "
                "weathering of rocks, and underwater volcanic "
                "activity. Water evaporates but most dissolved "
                "salts remain behind, so they accumulate in the "
                "ocean over very long periods."
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

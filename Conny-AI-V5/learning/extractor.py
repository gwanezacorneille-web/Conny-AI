from learning.models import KnowledgeEntry
import re


class KnowledgeExtractor:
    """
    Converts lessons into structured knowledge.
    """


    def extract(self, lesson, subject=None):

        lines = [
            line.strip()
            for line in lesson.split("\n")
            if line.strip()
        ]


        if not lines:

            return None


        # Determine topic

        topic = subject

        if not topic:

            topic = lines[0].split()[0]


        entry = KnowledgeEntry(
            topic=topic
        )


        for line in lines:

            lower = line.lower()


            # First sentence becomes definition

            if not entry.definition:

                entry.definition = line


            # Store every sentence as a fact

            entry.add_fact(line)


            # Extract keywords

            words = re.findall(
                r"[A-Za-z]{4,}",
                line
            )


            for word in words:

                entry.add_keyword(word)



            # Detect relationships


            if "created by" in lower:

                value = line.split(
                    "created by",
                    1
                )[1].strip()

                entry.add_relationship(
                    "creator",
                    value
                )


            if "released in" in lower:

                value = line.split(
                    "released in",
                    1
                )[1].strip()

                entry.add_relationship(
                    "release",
                    value
                )


            if "used for" in lower:

                value = line.split(
                    "used for",
                    1
                )[1].strip()

                entry.add_relationship(
                    "uses",
                    value
                )


        return entry

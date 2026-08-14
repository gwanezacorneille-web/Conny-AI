import re


class LessonParser:
    """
    Cleans and prepares a lesson before extraction.
    """

    def clean(self, lesson):

        if not lesson:
            return ""

        # Normalize line endings
        lesson = lesson.replace("\r\n", "\n")

        # Remove tabs
        lesson = lesson.replace("\t", " ")

        # Remove repeated spaces
        lesson = re.sub(r" +", " ", lesson)

        # Remove empty lines
        lines = []

        for line in lesson.split("\n"):

            line = line.strip()

            if line:

                lines.append(line)

        return "\n".join(lines)

    def paragraphs(self, lesson):

        lesson = self.clean(lesson)

        return lesson.split("\n")

    def sentences(self, lesson):

        lesson = self.clean(lesson)

        lesson = lesson.replace("\n", " ")

        sentences = re.split(r'(?<=[.!?])\s+', lesson)

        return [

            s.strip()

            for s in sentences

            if s.strip()

        ]

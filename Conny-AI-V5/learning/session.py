from datetime import datetime


class LearningSession:
    """
    Manages a teaching session.

    Example:

    User:
        study python

    Conny:
        Paste your lesson.

    User:
        ...

    User:
        END
    """

    def __init__(self):

        self.reset()

    def reset(self):

        self.active = False

        self.subject = None

        self.started = None

        self.lesson = []

    def start(self, subject):

        self.reset()

        self.active = True

        self.subject = subject

        self.started = datetime.now()

    def stop(self):

        self.active = False

    def add_line(self, line):

        self.lesson.append(line)

    def get_text(self):

        return "\n".join(self.lesson)

    def line_count(self):

        return len(self.lesson)

    def word_count(self):

        return len(self.get_text().split())

    def character_count(self):

        return len(self.get_text())

    def summary(self):

        duration = datetime.now() - self.started

        return {

            "subject": self.subject,

            "lines": self.line_count(),

            "words": self.word_count(),

            "characters": self.character_count(),

            "duration": str(duration)

        }

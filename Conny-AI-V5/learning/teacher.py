from learning.session import LearningSession


class Teacher:

    def __init__(self):

        self.session = LearningSession()

    def start(self, subject):

        self.session.start(subject)

        return f"""
==============================
CONNY AI TEACH MODE
==============================

Subject:
{subject.title()}

Paste your lesson.

When finished type

END

I will analyze everything before saving.
"""

    def receive(self, message):

        if not self.session.active:

            return None

        if message.strip().upper() == "END":

            lesson = self.session.get_text()

            summary = self.session.summary()

            self.session.stop()

            return {

                "finished": True,

                "lesson": lesson,

                "summary": summary

            }

        self.session.add_line(message)

        return {

            "finished": False
        }

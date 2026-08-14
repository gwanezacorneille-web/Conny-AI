from learning.teacher import Teacher
from learning.parser import LessonParser
from learning.extractor import KnowledgeExtractor


class LearningEngine:


    def __init__(self):

        self.teacher = Teacher()

        self.parser = LessonParser()

        self.extractor = KnowledgeExtractor()



    def start_learning(self, subject):

        return self.teacher.start(subject)



    def process_input(self, message):

        result = self.teacher.receive(message)


        if not result:

            return None



        if result["finished"]:


            lesson = result["lesson"]


            cleaned = self.parser.clean(
                lesson
            )


            knowledge = self.extractor.extract(
                cleaned,
                result["summary"]["subject"]
            )


            return {

                "type": "lesson_complete",

                "knowledge": knowledge,

                "summary": result["summary"]

            }


        return {

            "type": "learning",

            "message": "Lesson received..."

        }

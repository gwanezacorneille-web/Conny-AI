from brain.language.spell_checker import SpellChecker



class LanguageEngine:


    def __init__(self):

        self.spell_checker = SpellChecker()



    def understand(self, message):


        corrected = self.spell_checker.correct_sentence(
            message
        )


        return {

            "original": message,

            "corrected": corrected,

            "length": len(corrected),

            "words": corrected.split()

        }

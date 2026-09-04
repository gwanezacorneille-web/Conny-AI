from brain.language.spell_checker import SpellChecker


class LanguageEngine:

    def __init__(self):
        self.spell_checker = SpellChecker()

    # ---------------------------------------------------------
    # INDEFINITE ARTICLE RULE: A / AN
    # ---------------------------------------------------------

    _VOWEL_SOUNDS = (
        "a", "e", "i", "o", "u"
    )

    _AN_EXCEPTIONS = {
        "hour",
        "honest",
        "honor",
        "honour",
        "heir",
        "herb",
    }

    _A_EXCEPTIONS = {
        "university",
        "universal",
        "unique",
        "uniform",
        "union",
        "united",
        "use",
        "user",
        "usual",
        "useful",
        "European",
        "european",
        "one",
        "once",
    }

    def indefinite_article(self, word):
        """
        Return the correct indefinite article: 'a' or 'an'.

        The rule is based primarily on the SOUND of the
        following word, not simply its first written letter.
        """

        if not isinstance(word, str):
            raise TypeError("word must be a string")

        word = word.strip()

        if not word:
            return "a"

        # Remove common leading punctuation.
        word = word.lstrip("\"'([{")

        if not word:
            return "a"

        # Explicit pronunciation-based exceptions.
        if word.lower() in {
            item.lower() for item in self._AN_EXCEPTIONS
        }:
            return "an"

        if word.lower() in {
            item.lower() for item in self._A_EXCEPTIONS
        }:
            return "a"

        first = word[0].lower()

        # Ordinary vowel-initial words.
        if first in self._VOWEL_SOUNDS:
            return "an"

        return "a"

    def article_phrase(self, word):
        """
        Return '<a/an> <word>'.
        """
        if not isinstance(word, str):
            raise TypeError("word must be a string")

        word = word.strip()

        if not word:
            return ""

        return f"{self.indefinite_article(word)} {word}"

    def check_article(self, article, word):
        """
        Check whether an indefinite article is correct.
        """

        if not isinstance(article, str):
            return False

        expected = self.indefinite_article(word)

        return article.strip().lower() == expected

    # ---------------------------------------------------------
    # LANGUAGE UNDERSTANDING
    # ---------------------------------------------------------

    def understand(self, message):

        corrected = self.spell_checker.correct_sentence(
            message
        )

        return {
            "original": message,
            "corrected": corrected,
            "length": len(corrected),
            "words": corrected.split(),
        }

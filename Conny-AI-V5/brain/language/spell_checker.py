import difflib

from knowledge.knowledge_engine import KnowledgeEngine


class SpellChecker:

    def __init__(self):

        knowledge = KnowledgeEngine()

        self.dictionary = set(
            word.lower()
            for word in knowledge.get_all_keywords()
        )

    # ==================================================
    # CORRECT WORD
    # ==================================================

    def correct_word(self, word):

        # Preserve punctuation
        stripped = word.strip(".,!?;:()[]{}\"'")

        if not stripped:
            return word

        lower = stripped.lower()

        # ----------------------------------------------
        # Already known word
        # ----------------------------------------------

        if lower in self.dictionary:
            return word

        # ----------------------------------------------
        # Very short words are too risky to correct
        # ----------------------------------------------

        if len(lower) <= 3:
            return word

        # ----------------------------------------------
        # Only make corrections when similarity is high
        # ----------------------------------------------

        matches = difflib.get_close_matches(
            lower,
            self.dictionary,
            n=1,
            cutoff=0.90
        )

        if not matches:
            return word

        match = matches[0]

        # ----------------------------------------------
        # Preserve original capitalization/punctuation
        # ----------------------------------------------

        prefix = word[:len(word) - len(word.lstrip())]
        suffix = word[len(word.rstrip()):]

        punctuation = ""

        if word[-1:] in ".,!?;:)]}\"'":
            punctuation = word[-1]

        return prefix + match + punctuation

    # ==================================================
    # CORRECT SENTENCE
    # ==================================================

    def correct_sentence(self, sentence):

        words = sentence.split()

        corrected = []

        for word in words:

            corrected.append(
                self.correct_word(word)
            )

        return " ".join(corrected)

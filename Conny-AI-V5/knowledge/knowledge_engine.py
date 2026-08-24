import re

from knowledge.domains.networking import get_knowledge as networking
from knowledge.domains.computers import get_knowledge as computers
from knowledge.domains.programming import get_knowledge as programming
from knowledge.domains.electronics import get_knowledge as electronics
from knowledge.domains.operating_systems import get_knowledge as operating_systems


class KnowledgeEngine:

    def __init__(self):

        self.knowledge = {}

        self.load()

    # ==================================================
    # LOAD KNOWLEDGE
    # ==================================================

    def load(self):

        self.knowledge.update(networking())
        self.knowledge.update(computers())
        self.knowledge.update(programming())
        self.knowledge.update(electronics())
        self.knowledge.update(operating_systems())
        
        # ==================================================
        # CONNY CREATOR PERSONAL KNOWLEDGE
        # ==================================================
        # Custom knowledge intentionally kept in the
        # KnowledgeEngine so it works with the existing
        # offline knowledge pipeline.
        
        self.knowledge["carine bebe"] = {
            "keywords": [
                "carine bebe",
                "carine",
                "bebe"
            ],
            "answer": (
                "CARINE BEBE is the current girlfriend of my creator, "
                "and perhaps his future wife. She means so much to him, "
                "and my creator loves her more than words can express. ❤️"
            )
        }


    # ==================================================
    # KEYWORD MATCHING
    # ==================================================

    def _keyword_matches(self, text, keyword):

        text = text.lower()
        keyword = keyword.lower().strip()

        if not keyword:
            return False

        # Match complete words/phrases.
        pattern = r"\b" + re.escape(keyword) + r"\b"

        return re.search(pattern, text) is not None

    # ==================================================
    # SCORE CONCEPT
    # ==================================================

    def score(self, text, data):

        score = 0

        keywords = data.get("keywords", [])

        for keyword in keywords:

            keyword = keyword.lower().strip()

            # Exact phrase / complete-word match
            if self._keyword_matches(text, keyword):

                # Exact keyword is strong evidence
                score += 5

                continue

            # Partial word matching for multi-word
            # keywords, but still using complete words.
            words = keyword.split()

            for word in words:

                if self._keyword_matches(text, word):

                    score += 1

        return score

    # ==================================================
    # FIND CONCEPT
    # ==================================================

    def find_concept(self, text):

        best_score = 0
        best_name = None
        best_data = None

        text = text.lower().strip()

        for concept, data in self.knowledge.items():

            score = self.score(text, data)

            # --------------------------------------------------
            # Direct-question boost
            # --------------------------------------------------
            # Give a strong preference to the concept that the
            # user is actually asking about.
            #
            # Handles:
            #   what is variable?
            #   what is a variable?
            #   what is the variable?
            #   explain variable
            #   explain what a variable is
            #   explain what the variable is
            #   define variable
            # --------------------------------------------------

            if self._keyword_matches(text, concept):

                concept_pattern = re.escape(concept)

                direct_patterns = [

                    rf"\bwhat\s+is\s+(?:a|an|the)?\s*{concept_pattern}\b",

                    rf"\bwhat\s+are\s+(?:the)?\s*{concept_pattern}\b",

                    rf"\bexplain\s+(?:a|an|the)?\s*{concept_pattern}\b",

                    rf"\bexplain\s+what\s+(?:a|an|the)?\s*{concept_pattern}\s+is\b",

                    rf"\bdefine\s+(?:a|an|the)?\s*{concept_pattern}\b",

                    rf"\bdefinition\s+of\s+(?:a|an|the)?\s*{concept_pattern}\b",
                ]

                if any(
                    re.search(pattern, text)
                    for pattern in direct_patterns
                ):

                    score += 20

            # --------------------------------------------------
            # Best concept
            # --------------------------------------------------

            if score > best_score:

                best_score = score
                best_name = concept
                best_data = data

            elif score == best_score and score > 0:

                concept_match = self._keyword_matches(
                    text,
                    concept
                )

                current_match = self._keyword_matches(
                    text,
                    best_name
                )

                if concept_match and not current_match:

                    best_name = concept
                    best_data = data

        if best_score == 0:

            return None

        return {
            "name": best_name,
            "data": best_data,
            "score": best_score
        }
    # ==================================================
    # SEARCH
    # ==================================================

    def search(self, text):

        return self.find_concept(text)

    # ==================================================
    # ALL KEYWORDS
    # ==================================================

    def get_all_keywords(self):

        keywords = []

        for data in self.knowledge.values():

            keywords.extend(
                data.get("keywords", [])
            )

        return sorted(
            list(set(keywords))
        )

    # ==================================================
    # FIND BY NAME
    # ==================================================

    def find_by_name(self, name):

        name = name.lower().strip()

        for concept, data in self.knowledge.items():

            if concept.lower() == name:

                return {
                    "name": concept,
                    "data": data
                }

            for keyword in data.get("keywords", []):

                if keyword.lower() == name:

                    return {
                        "name": concept,
                        "data": data
                    }

        return None

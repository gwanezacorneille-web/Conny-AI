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

            # Prefer the concept being directly asked about.
            if self._keyword_matches(text, concept):

                normalized = text.replace(
                    f"what a {concept} is",
                    f"what {concept} is"
                )

                normalized = normalized.replace(
                    f"what an {concept} is",
                    f"what {concept} is"
                )

                normalized = normalized.replace(
                    f"what the {concept} is",
                    f"what {concept} is"
                )

                direct_patterns = [
                    f"what is {concept}",
                    f"what are {concept}",
                    f"explain {concept}",
                    f"explain what {concept} is",
                    f"define {concept}",
                    f"definition of {concept}",
                ]

                if any(pattern in normalized for pattern in direct_patterns):
                    score += 20
            if score > best_score:
                best_score = score
                best_name = concept
                best_data = data

            elif score == best_score and score > 0:

                # Prefer a concept whose actual name
                # appears in the user's question.
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

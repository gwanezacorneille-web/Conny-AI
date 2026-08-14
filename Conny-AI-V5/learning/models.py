from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class KnowledgeEntry:
    """
    Represents one learned concept.
    """

    topic: str

    category: str = "General"

    definition: str = ""

    facts: list[str] = field(default_factory=list)

    keywords: list[str] = field(default_factory=list)

    relationships: dict = field(default_factory=dict)

    examples: list[str] = field(default_factory=list)

    source: str = "User Teaching"

    confidence: float = 1.0

    verified: bool = False

    created: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    updated: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def add_fact(self, fact):

        if fact not in self.facts:

            self.facts.append(fact)

    def add_keyword(self, keyword):

        keyword = keyword.lower()

        if keyword not in self.keywords:

            self.keywords.append(keyword)

    def add_example(self, example):

        if example not in self.examples:

            self.examples.append(example)

    def add_relationship(self, relation, value):

        self.relationships[relation] = value

    def update_timestamp(self):

        self.updated = datetime.now().isoformat()

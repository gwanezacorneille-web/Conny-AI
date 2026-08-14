from learning.extractor import KnowledgeExtractor


lesson = """
Python is a high level programming language.

It was created by Guido van Rossum.

It was released in 1991.

Python is used for artificial intelligence.
"""


extractor = KnowledgeExtractor()


knowledge = extractor.extract(
    lesson,
    "Python"
)


print("================")
print("TOPIC:")
print(knowledge.topic)

print()

print("DEFINITION:")
print(knowledge.definition)

print()

print("FACTS:")
for fact in knowledge.facts:
    print("-", fact)

print()

print("KEYWORDS:")
print(knowledge.keywords)

print()

print("RELATIONSHIPS:")
print(knowledge.relationships)

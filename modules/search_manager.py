from modules.providers.wikipedia_provider import search as wiki_search
from modules.providers.duckduckgo_provider import search as duck_search
from modules.question_analyzer import analyze_question
from modules.answer_formatter import format_answer


def search_knowledge(query):

    analysis = analyze_question(query)

    question_type = analysis.get(
        "type",
        "general"
    )

    subject = analysis.get(
        "subject",
        query
    )

    providers = [

        wiki_search,

        duck_search

    ]

    for provider in providers:

        try:

            answer = provider(subject)

            if answer:

                formatted = format_answer(
                    question_type,
                    answer
                )

                if formatted:
                    return formatted

                return answer

        except Exception as error:

            print(
                "Search error:",
                error
            )

    return None

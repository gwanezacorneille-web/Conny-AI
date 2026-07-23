from conny_online import search_online
from modules.wikipedia_search import search_wikipedia



def search_knowledge(question):


    # Try Wikipedia first

    answer = search_wikipedia(question)

    if answer:

        return answer



    # Try DuckDuckGo

    answer = search_online(question)


    if answer.startswith("I couldn't"):

        return None


    return answer

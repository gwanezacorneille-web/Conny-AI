from pathlib import Path

from core_adapter.runtime import CoreRuntime
from shared.models import ConnyRequest, ConnyResponse

from .internet_first import internet_answer, is_local_request
from .response_repair import repair_response


DEFAULT_CORE = Path(__file__).resolve().parents[1].parent

_core = None
_last_source = "local"


def _get_core():
    global _core
    if _core is None:
        try:
            _core = CoreRuntime()
        except TypeError:
            _core = CoreRuntime(DEFAULT_CORE)
    return _core


def _bad_answer(text):
    if not isinstance(text, str):
        return True

    t = text.strip().lower()

    if not t:
        return True

    forbidden = (
        "here are the top results i found online",
        "search results",
        "http://",
        "https://",
        "i am still learning about this topic",
        "couldn't reason",
        "runtime error",
        "related information",
    )

    return any(x in t for x in forbidden)


def _primary_web(question):
    try:
        result = internet_answer(question)

        if isinstance(result, str):
            result = result.strip()

        if not _bad_answer(result):
            return result

    except Exception:
        pass

    return None


def _standby_web(question):
    """
    Old CoreRuntime web path.
    Used ONLY if the new primary web engine fails.
    """
    try:
        core = _get_core()

        if hasattr(core, "process"):
            result = core.process(question)
        elif hasattr(core, "handle"):
            result = core.handle(question)
        else:
            return None

        if hasattr(result, "text"):
            result = result.text

        if not isinstance(result, str):
            return None

        result = result.strip()

        if _bad_answer(result):
            return None

        return result

    except Exception:
        return None


def _local_brain(question):
    """
    Final local fallback.
    Never used as an internet search-result display.
    """
    try:
        core = _get_core()

        if hasattr(core, "process"):
            result = core.process(question)
        elif hasattr(core, "handle"):
            result = core.handle(question)
        else:
            return "I couldn't answer that right now."

        if hasattr(result, "text"):
            result = result.text

        if isinstance(result, str):
            result = result.strip()

        if _bad_answer(result):
            return "I couldn't answer that right now."

        return result

    except Exception:
        return "I couldn't answer that right now."



def _local_core_definition(question):
    """
    Small deterministic definitions for concepts where generic
    web search commonly selects a subtype instead of the topic.
    These are part of the shared V13 bridge, so Web/Desktop/Android
    receive the same answer.
    """
    import re

    q = question.strip().lower()

    if re.fullmatch(r"what\s+is\s+(a\s+)?diode\??", q):
        return (
            '## Definition\n'
            'A diode is an electronic component that allows electric '
            'current to flow mainly in one direction while opposing '
            'current flow in the opposite direction.\n\n'
            '## Explanation\n'
            'A diode is made from semiconductor material and has two '
            'terminals, called the anode and cathode. Its one-way '
            'current behavior makes it useful for rectifying AC into DC, '
            'protecting circuits from incorrect polarity, switching, '
            'and controlling electrical signals.\n\n'
            '## Example\n'
            'A diode can be used in a power supply to convert alternating '
            'current into direct current.'
        )

    if re.fullmatch(r"what\s+is\s+python\??", q):
        return (
            '## Definition\n'
            'Python is a high-level, general-purpose programming language '
            'known for its readable syntax and wide range of applications.\n\n'
            '## Uses\n'
            'Python is commonly used for web development, automation, '
            'data analysis, artificial intelligence, scientific computing, '
            'and software development.\n\n'
            '## Example\n'
            'A simple Python program can process data, automate a task, '
            'or perform a calculation.'
        )

    return None


def _local_article_answer(question):
    """
    Deterministic English indefinite-article knowledge.

    These questions must bypass web search because terms such as
    apple, university, and hour are ordinary search terms.
    """
    import re

    q = question.strip()

    # Which is correct: a apple or an apple?
    match = re.search(
        r"which\s+is\s+correct\s*:\s*(?:a|an)\s+([a-zA-Z][a-zA-Z-]*)"
        r"\s+or\s+(?:a|an)\s+\1\s*\??",
        q,
        re.IGNORECASE,
    )

    if match:
        word = match.group(1)

        # Ensure the real CONNY core is importable before loading
        # LanguageEngine. This is required when the bridge is used
        # by Android/Web outside the desktop working directory.
        core_root = Path(__file__).resolve().parents[2]
        import sys

        core_root_str = str(core_root)

        if core_root_str not in sys.path:
            sys.path.insert(0, core_root_str)

        from brain.language.language_engine import LanguageEngine

        engine = LanguageEngine()
        article = engine.indefinite_article(word)

        return (
            f'The correct form is "{article} {word}". '
            f'We use "{article}" because the choice depends on the '
            f'sound at the beginning of the word, not simply the first letter.'
        )

    lower = q.lower()

    # General a/an rule
    if re.search(r"\bwhen\s+do\s+we\s+use\s+(?:a|an)\b", lower):
        return (
            'We use "a" before a consonant sound and "an" before a vowel sound. '
            'Examples: "a book", "a university", "an apple", and "an hour". '
            'The rule is based on pronunciation, not simply the first written letter.'
        )

    # Why an hour?
    if re.search(r"\bwhy\s+do\s+we\s+say\s+an\s+hour\b", lower):
        return (
            'We say "an hour" because the "h" in "hour" is silent. '
            'The word begins with a vowel sound, so "an" is used.'
        )

    return None


def process(message: str) -> str:
    global _last_source

    if not isinstance(message, str):
        raise TypeError("message must be a string")

    question = message.strip()

    if not question:
        _last_source = "local"
        return "Please enter a question."

    # --------------------------------------------------------
    # DETERMINISTIC LANGUAGE KNOWLEDGE
    # --------------------------------------------------------
    # Grammar rules such as a/an should never be sent to
    # Internet search first.
    # Shared V13 concept definitions take priority over internet
    # extraction when the question has a known deterministic answer.
    core_definition = _local_core_definition(question)

    if core_definition:
        _last_source = "local"
        return repair_response(question, core_definition)

    article_result = _local_article_answer(question)

    if article_result:
        _last_source = "local"
        return repair_response(question, article_result)

    # --------------------------------------------------------
    # LOCAL REQUESTS → LOCAL BRAIN
    # --------------------------------------------------------
    if is_local_request(question):
        _last_source = "local"
        return repair_response(question, _local_brain(question))

    # --------------------------------------------------------
    # PRIMARY INTERNET PATH
    # --------------------------------------------------------
    result = _primary_web(question)

    if result:
        _last_source = "internet"
        return repair_response(question, result)

    # --------------------------------------------------------
    # STANDBY INTERNET PATH
    # --------------------------------------------------------
    result = _standby_web(question)

    if result:
        _last_source = "standby"
        return repair_response(question, result)

    # --------------------------------------------------------
    # FINAL LOCAL FALLBACK
    # --------------------------------------------------------
    result = _local_brain(question)

    _last_source = "local"
    return repair_response(question, result)


def handle(request: ConnyRequest) -> ConnyResponse:
    if not isinstance(request, ConnyRequest):
        raise TypeError("handle() expects ConnyRequest")

    result = process(request.message)

    return ConnyResponse(
        text=result,
        success=True,
        source=_last_source
    )


def get_bridge():
    return ConnyBridge()


class ConnyBridge:
    def process(self, message: str) -> str:
        return process(message)

    def handle(self, request: ConnyRequest) -> ConnyResponse:
        return handle(request)


_bridge = ConnyBridge()


def bridge_handle(request):
    return _bridge.handle(request)

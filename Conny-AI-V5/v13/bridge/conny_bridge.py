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


def process(message: str) -> str:
    global _last_source

    if not isinstance(message, str):
        raise TypeError("message must be a string")

    question = message.strip()

    if not question:
        _last_source = "local"
        return "Please enter a question."

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

"""
CONNY AI V13 — Main Answer Extraction Engine

Purpose:
    Turn web search/page material into the useful answer only.

Reject:
    - navigation
    - menus
    - advertisements
    - cookie notices
    - headers/footers
    - search-result boilerplate
    - repeated links
    - unrelated page sections
    - excessive metadata

Prefer:
    - direct definitions
    - direct answers
    - explanatory sentences
    - relevant examples
    - key facts

The engine does NOT reproduce entire web pages.
"""

from __future__ import annotations

import re
from html import unescape


NOISE_PATTERNS = (
    r"\badvertisement\b",
    r"\bads?\b",
    r"\bcookie(s)?\b",
    r"\bprivacy policy\b",
    r"\bterms of (service|use)\b",
    r"\bsubscribe\b",
    r"\bsign up\b",
    r"\blog in\b",
    r"\blog out\b",
    r"\bmenu\b",
    r"\bnavigation\b",
    r"\bhome\b",
    r"\bcontents\b",
    r"\btable of contents\b",
    r"\brelated articles?\b",
    r"\bshare\b",
    r"\bfollow us\b",
    r"\bnewsletter\b",
    r"\bskip to\b",
    r"\bclick here\b",
    r"\baccept cookies\b",
    r"\breferences?\b",
    r"\bcitations?\b",
    r"\bsee also\b",
)

WEAK_PATTERNS = (
    r"search results?",
    r"results? for",
    r"people also ask",
    r"people also search",
    r"top stories",
    r"sponsored",
)


def clean_html(text: str) -> str:
    text = unescape(str(text or ""))
    text = re.sub(
        r"<(script|style|noscript|svg|iframe)[^>]*>.*?</\1>",
        " ",
        text,
        flags=re.I | re.S,
    )
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _looks_like_noise(sentence: str) -> bool:
    s = sentence.lower().strip()

    if len(s) < 25:
        return True

    if len(s) > 900:
        return True

    for pattern in NOISE_PATTERNS:
        if re.search(pattern, s, re.I):
            return True

    for pattern in WEAK_PATTERNS:
        if re.search(pattern, s, re.I):
            return True

    # URL-only or link-heavy content.
    if re.fullmatch(r"https?://\S+", s):
        return True

    if s.count("http") >= 2:
        return True

    return False


def split_sentences(text: str) -> list[str]:
    text = clean_html(text)

    # Normalize common separators.
    text = re.sub(r"\s*[•|]\s*", ". ", text)
    text = re.sub(r"\s+", " ", text)

    sentences = re.split(
        r"(?<=[.!?])\s+(?=[A-Z0-9])",
        text,
    )

    return [
        x.strip(" -–—\t")
        for x in sentences
        if x.strip()
    ]


def _question_terms(question: str) -> set[str]:
    words = re.findall(
        r"[a-zA-Z0-9+#.-]+",
        str(question or "").lower(),
    )

    stop = {
        "what", "is", "are", "was", "were", "the",
        "a", "an", "of", "to", "for", "in", "on",
        "and", "or", "how", "why", "who", "where",
        "when", "does", "do", "can", "could", "would",
        "should", "tell", "me", "about", "please",
        "it", "this", "that",
    }

    return {
        w for w in words
        if len(w) >= 3 and w not in stop
    }


def score_sentence(sentence: str, question: str) -> int:
    low = sentence.lower()
    terms = _question_terms(question)

    words = set(
        re.findall(r"[a-zA-Z0-9+#.-]+", low)
    )

    score = len(terms.intersection(words)) * 3

    # Strong indicators of a direct explanation.
    if re.search(
        r"\bis (a|an|the)\b|\bare (a|an|the)\b",
        low,
    ):
        score += 8

    if any(
        marker in low
        for marker in (
            "means",
            "refers to",
            "defined as",
            "is known as",
            "is used to",
            "is used for",
            "allows",
            "consists of",
            "works by",
            "because",
            "for example",
            "such as",
        )
    ):
        score += 5

    # Prefer reasonably concise explanatory sentences.
    length = len(sentence)

    if 50 <= length <= 350:
        score += 4
    elif length > 600:
        score -= 3

    return score


def extract_main_answer(
    question: str,
    materials: list[str],
    maximum_sentences: int = 5,
) -> str:
    """
    Extract only the strongest answer-bearing sentences.
    """

    candidates = []

    for material in materials:
        if not material:
            continue

        for sentence in split_sentences(material):
            if _looks_like_noise(sentence):
                continue

            score = score_sentence(
                sentence,
                question,
            )

            candidates.append(
                (score, sentence)
            )

    if not candidates:
        return ""

    candidates.sort(
        key=lambda item: (
            item[0],
            -abs(len(item[1]) - 180),
        ),
        reverse=True,
    )

    selected = []
    seen = set()

    for score, sentence in candidates:
        normalized = re.sub(
            r"\W+",
            " ",
            sentence.lower(),
        ).strip()

        if normalized in seen:
            continue

        seen.add(normalized)
        selected.append(sentence)

        if len(selected) >= maximum_sentences:
            break

    if not selected:
        return ""

    # Reorder selected material according to strongest relevance.
    result = " ".join(selected)

    # Remove accidental repeated whitespace.
    result = re.sub(r"\s+", " ", result).strip()

    # Keep the answer focused.
    if len(result) > 1800:
        result = result[:1797].rsplit(" ", 1)[0] + "..."

    return result


def answer_is_raw_web_dump(answer: str) -> bool:
    """
    Detect whether an answer looks like copied search/page material.
    """

    text = str(answer or "").strip()
    low = text.lower()

    if not text:
        return True

    if len(text) > 2500:
        return True

    noise_hits = sum(
        bool(re.search(pattern, low, re.I))
        for pattern in NOISE_PATTERNS
    )

    if noise_hits >= 2:
        return True

    if low.count("http") >= 2:
        return True

    if "search results" in low:
        return True

    return False


def format_conny_answer(
    question: str,
    answer: str,
) -> str:
    """
    Final presentation cleanup.
    """

    text = clean_html(answer)

    # Strip common search-engine prefixes.
    text = re.sub(
        r"^(search results?:?|results?:?)\s*",
        "",
        text,
        flags=re.I,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    if not text:
        return ""

    return text

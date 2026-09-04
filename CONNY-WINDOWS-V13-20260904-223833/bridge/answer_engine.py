import re
from typing import List, Dict, Optional


# ----------------------------------------------------------------------
# TEXT CLEANING
# ----------------------------------------------------------------------

NOISE_PATTERNS = [
    r"^a\s+a\s+",
    r"\ba\s+a\s*$",
    r"^home\s*$",
    r"^menu\s*$",
    r"^search\s*$",
    r"^login\s*$",
    r"^sign in\s*$",
    r"^sign up\s*$",
    r"^subscribe\s*$",
    r"^advertisement\s*$",
    r"^cookie",
    r"^privacy policy\s*$",
    r"^terms of",
    r"^skip to",
    r"^navigation\s*$",
    r"^contents\s*$",
    r"^table of contents\s*$",
]

SOURCE_TITLE_PATTERNS = [
    "wikipedia",
    "geeksforgeeks",
    "britannica",
    "tutorialspoint",
    "byju",
    "studytonight",
    "javatpoint",
    "techopedia",
    "coursera",
    "indeed",
    "simplilearn",
    "educba",
]


def _clean(text: str) -> str:
    if not text:
        return ""

    text = str(text)

    # Remove URLs.
    text = re.sub(r"https?://\S+", " ", text)

    # Remove common HTML leftovers.
    text = re.sub(r"<[^>]+>", " ", text)

    # Decode a few common entities.
    text = text.replace("&nbsp;", " ")
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")

    # Remove repeated navigation artifacts.
    text = re.sub(r"\bA\s+A\b", " ", text, flags=re.I)

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip(" -–—:;,. \n\t")


def _normalize_key(text: str) -> str:
    text = _clean(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _looks_like_noise(text: str) -> bool:
    value = _clean(text)

    if not value:
        return True

    low = value.lower()

    if len(value) < 25:
        return True

    for pattern in NOISE_PATTERNS:
        if re.search(pattern, low):
            return True

    # Source-title/navigation chains.
    source_hits = sum(1 for name in SOURCE_TITLE_PATTERNS if name in low)

    if source_hits >= 2:
        return True

    # Strong navigation indicators.
    navigation_words = [
        "click here",
        "read more",
        "learn more",
        "related articles",
        "all rights reserved",
        "follow us",
        "share this",
        "sign in",
        "subscribe now",
    ]

    if any(x in low for x in navigation_words):
        return True

    # Sentences that are mostly title fragments.
    if low.count(" - ") >= 2:
        return True

    # Repeated "A A" remnants.
    if low.count("a a") >= 2:
        return True

    return False


def _sentence_parts(text: str) -> List[str]:
    text = _clean(text)

    if not text:
        return []

    # Split on sentence boundaries.
    parts = re.split(r"(?<=[.!?])\s+", text)

    # Some scraped pages have long fragments separated by pipes.
    expanded = []

    for part in parts:
        part = _clean(part)

        if not part:
            continue

        # Split obvious navigation chains.
        chunks = re.split(r"\s+\|\s+", part)

        for chunk in chunks:
            chunk = _clean(chunk)

            if chunk:
                expanded.append(chunk)

    return expanded


def _sentences(text: str) -> List[str]:
    result = []
    seen = set()

    for part in _sentence_parts(text):
        if _looks_like_noise(part):
            continue

        key = _normalize_key(part)

        if not key or key in seen:
            continue

        seen.add(key)
        result.append(part)

    return result


# ----------------------------------------------------------------------
# SOURCE PROCESSING
# ----------------------------------------------------------------------

def _source_sentences(
    question: str,
    sources: List[Dict],
    context: Optional[str] = None,
) -> List[str]:

    candidates = []

    if context:
        candidates.extend(_sentences(str(context)))

    for source in sources or []:

        # IMPORTANT:
        # Titles are metadata, NOT answer content.
        #
        # Only snippets and page text are considered factual material.
        snippet = source.get("snippet", "")
        text = source.get("text", "")

        if snippet:
            candidates.extend(_sentences(str(snippet)))

        if text:
            candidates.extend(_sentences(str(text)))

    return _rank_sentences(question, candidates)


def _question_words(question: str) -> List[str]:
    stop = {
        "what", "is", "are", "a", "an", "the", "of", "to", "for",
        "and", "or", "in", "on", "with", "how", "why", "does", "do",
        "can", "used", "use", "define", "definition", "meaning",
        "explain", "please", "tell", "me", "about", "between",
        "difference", "differences",
    }

    words = re.findall(r"[a-zA-Z0-9]+", question.lower())

    return [
        word
        for word in words
        if len(word) >= 3 and word not in stop
    ]


def _rank_sentences(question: str, sentences: List[str]) -> List[str]:

    words = _question_words(question)

    scored = []

    for index, sentence in enumerate(sentences):

        low = sentence.lower()
        score = 0

        # Relevance to question.
        for word in words:
            if re.search(r"\b" + re.escape(word) + r"\b", low):
                score += 4

        # Definitions are highly valuable for "what is".
        if re.search(
            r"\b(is|are|refers to|means|defined as|known as|"
            r"consists of|used to)\b",
            low,
        ):
            score += 7

        # Prefer reasonable factual sentence length.
        if 45 <= len(sentence) <= 350:
            score += 3

        if len(sentence) > 700:
            score -= 4

        # Penalize obvious source-page noise.
        if any(name in low for name in SOURCE_TITLE_PATTERNS):
            score -= 8

        if "a a" in low:
            score -= 10

        # Slight preference for earlier source material.
        score += max(0, 2 - index / 50)

        scored.append((score, index, sentence))

    scored.sort(key=lambda item: (-item[0], item[1]))

    return [sentence for _, _, sentence in scored]


# ----------------------------------------------------------------------
# GENERAL HELPERS
# ----------------------------------------------------------------------

def _unique(items: List[str], limit: int = 6) -> List[str]:

    result = []
    seen = set()

    for item in items:
        item = _clean(item)

        if _looks_like_noise(item):
            continue

        key = _normalize_key(item)

        if not key or key in seen:
            continue

        seen.add(key)
        result.append(item)

        if len(result) >= limit:
            break

    return result


def _bullets(items: List[str]) -> str:
    return "\n".join(f"• {x}" for x in items if x)


def _is_comparison(question: str) -> bool:

    q = question.lower()

    markers = [
        "compare",
        "comparison",
        "difference between",
        "differences between",
        "versus",
        " vs ",
        "better than",
    ]

    return any(marker in q for marker in markers)


def _is_definition(question: str) -> bool:

    q = question.lower().strip()

    markers = [
        "what is ",
        "what are ",
        "define ",
        "definition of ",
        "meaning of ",
        "explain ",
    ]

    return any(marker in q for marker in markers)


def _is_current(question: str) -> bool:

    q = question.lower()

    markers = [
        "today",
        "latest",
        "current",
        "recent",
        "now",
        "news",
        "this week",
        "this month",
        "what happened",
    ]

    return any(marker in q for marker in markers)


def _extract_by_keywords(
    sentences: List[str],
    keywords: List[str],
    limit: int = 4,
) -> List[str]:

    matches = []

    for sentence in sentences:

        low = sentence.lower()

        if any(k in low for k in keywords):
            matches.append(sentence)

    return _unique(matches, limit)


def _best_definition(sentences: List[str]) -> Optional[str]:

    if not sentences:
        return None

    patterns = [
        r"\bis a\b",
        r"\bis an\b",
        r"\bare\b",
        r"\brefers to\b",
        r"\bmeans\b",
        r"\bdefined as\b",
        r"\bknown as\b",
        r"\bis the\b",
    ]

    candidates = []

    for sentence in sentences:

        low = sentence.lower()

        score = 0

        for pattern in patterns:
            if re.search(pattern, low):
                score += 5

        # Prefer concise definition sentences.
        if len(sentence) <= 300:
            score += 2

        # Prefer sentences directly containing question topic words.
        if len(sentence) >= 45:
            score += 1

        candidates.append((score, sentence))

    candidates.sort(key=lambda item: (-item[0], len(item[1])))

    best_score, best_sentence = candidates[0]

    if best_score > 0:
        return best_sentence

    return sentences[0]


def _topic_from_question(question: str) -> str:

    q = question.strip()

    q = re.sub(
        r"^(what is|what are|define|definition of|meaning of|explain)\s+",
        "",
        q,
        flags=re.I,
    )

    q = q.rstrip("?.! ")

    return q.strip()


# ----------------------------------------------------------------------
# MAIN ANSWER ENGINE
# ----------------------------------------------------------------------

def answer_from_sources(
    question: str,
    sources: List[Dict],
    context: Optional[str] = None,
) -> Optional[str]:

    sentences = _source_sentences(
        question,
        sources,
        context=context,
    )

    if not sentences:
        return None

    comparison = _is_comparison(question)
    current = _is_current(question)
    definition = _is_definition(question)

    # ------------------------------------------------------------------
    # CURRENT INFORMATION
    # ------------------------------------------------------------------

    if current:

        key = _extract_by_keywords(
            sentences,
            [
                "today",
                "announced",
                "reported",
                "latest",
                "recent",
                "according",
                "update",
                "said",
                "confirmed",
                "yesterday",
            ],
            6,
        )

        if not key:
            key = _unique(sentences, 6)

        if not key:
            return None

        sections = [
            "## What happened",
            _bullets(key[:4]),
        ]

        if len(key) > 4:
            sections += [
                "",
                "## Key details",
                _bullets(key[4:6]),
            ]

        sections += [
            "",
            "## Summary",
            key[0],
        ]

        return "\n".join(sections)

    # ------------------------------------------------------------------
    # COMPARISON
    # ------------------------------------------------------------------

    if comparison:

        differences = _extract_by_keywords(
            sentences,
            [
                "difference",
                "whereas",
                "while",
                "however",
                "unlike",
                "both",
                "advantage",
                "disadvantage",
                "faster",
                "slower",
                "larger",
                "smaller",
                "different",
            ],
            6,
        )

        uses = _extract_by_keywords(
            sentences,
            [
                "used",
                "use",
                "application",
                "purpose",
                "designed",
                "works",
                "used for",
            ],
            4,
        )

        definition = _best_definition(sentences)

        sections = [
            "## Definition",
            definition or sentences[0],
            "",
            "## Key Differences",
            _bullets(
                differences[:5]
                if differences
                else _unique(sentences[1:5], 4)
            ),
        ]

        if uses:
            sections += [
                "",
                "## Uses",
                _bullets(uses[:4]),
            ]

        sections += [
            "",
            "## Summary",
            sentences[-1],
        ]

        return "\n".join(sections)

    # ------------------------------------------------------------------
    # DEFINITION / EXPLANATION
    # ------------------------------------------------------------------

    if definition:

        best_definition = _best_definition(sentences)

        explanation = _extract_by_keywords(
            sentences,
            [
                "means",
                "refers to",
                "is a",
                "is an",
                "defined",
                "consists",
                "involves",
                "works by",
                "operates",
                "converts",
            ],
            4,
        )

        # Don't repeat the definition inside Explanation.
        if best_definition:
            explanation = [
                x for x in explanation
                if _normalize_key(x) != _normalize_key(best_definition)
            ]

        examples = _extract_by_keywords(
            sentences,
            [
                "example",
                "examples",
                "such as",
                "including",
                "for instance",
                "types include",
            ],
            4,
        )

        uses = _extract_by_keywords(
            sentences,
            [
                "used",
                "use",
                "purpose",
                "application",
                "works",
                "designed",
                "used for",
            ],
            4,
        )

        advantages = _extract_by_keywords(
            sentences,
            [
                "advantage",
                "benefit",
                "efficient",
                "useful",
                "convenient",
                "helpful",
            ],
            4,
        )

        disadvantages = _extract_by_keywords(
            sentences,
            [
                "disadvantage",
                "drawback",
                "limitation",
                "limited",
                "difficult",
                "expensive",
            ],
            4,
        )

        sections = [
            "## Definition",
            best_definition or sentences[0],
        ]

        if explanation:
            sections += [
                "",
                "## Explanation",
                _bullets(explanation[:3]),
            ]

        if examples:
            sections += [
                "",
                "## Examples",
                _bullets(examples[:4]),
            ]

        if uses:
            sections += [
                "",
                "## Uses",
                _bullets(uses[:4]),
            ]

        if advantages:
            sections += [
                "",
                "## Advantages",
                _bullets(advantages[:4]),
            ]

        if disadvantages:
            sections += [
                "",
                "## Disadvantages",
                _bullets(disadvantages[:4]),
            ]

        # Use the most relevant final sentence instead of blindly
        # taking the last scraped sentence.
        summary = sentences[0]

        if best_definition:
            summary = best_definition

        sections += [
            "",
            "## Summary",
            summary,
        ]

        return "\n".join(sections)

    # ------------------------------------------------------------------
    # GENERAL QUESTION
    # ------------------------------------------------------------------

    key = _unique(sentences, 6)

    if not key:
        return None

    sections = [
        "## Explanation",
        _bullets(key[:4]),
    ]

    if len(key) > 4:
        sections += [
            "",
            "## Key points",
            _bullets(key[4:6]),
        ]

    sections += [
        "",
        "## Summary",
        key[0],
    ]

    return "\n".join(sections)


def extract_answer(
    question: str,
    sources: List[Dict],
    context=None,
):
    return answer_from_sources(
        question,
        sources,
        context,
    )

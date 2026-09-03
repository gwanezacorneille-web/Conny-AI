import re


# ============================================================
# FINAL V13 KNOWLEDGE QUALITY LAYER
# ============================================================

GENERIC_FALLBACKS = (
    "the term refers to a concept, object, or subject identified by that name",
    "i am still learning about this topic",
    "i couldn't answer that right now",
    "i could not answer that right now",
)


def clean(text):
    if not isinstance(text, str):
        return ""

    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def target_from_question(question):
    q = clean(question)

    patterns = [
        r"^\s*what\s+is\s+(?:an?\s+|the\s+)?(.+?)\s*\??$",
        r"^\s*what\s+are\s+(?:the\s+)?(.+?)\s*\??$",
        r"^\s*define\s+(.+?)\s*\??$",
        r"^\s*meaning\s+of\s+(.+?)\s*\??$",
    ]

    for pattern in patterns:
        match = re.match(pattern, q, re.I)

        if match:
            target = match.group(1).strip()

            target = re.sub(
                r"\b(please|today|in simple terms|in simple words)\b",
                "",
                target,
                flags=re.I,
            )

            return target.strip(" .?!")

    return ""


def is_generic_fallback(text):
    low = clean(text).lower()

    if not low:
        return True

    return any(x in low for x in GENERIC_FALLBACKS)


def contains_target(text, target):
    text_words = set(re.findall(r"[a-z0-9]+", clean(text).lower()))
    target_words = set(re.findall(r"[a-z0-9]+", clean(target).lower()))

    if not target_words:
        return False

    if target.lower() in clean(text).lower():
        return True

    return bool(target_words.intersection(text_words))


def remove_bad_lines(lines, target):
    bad_phrases = (
        "here are the top results",
        "top results i found online",
        "search results",
        "related information",
        "people also ask",
        "runtime error",
        "couldn't reason",
        "http://",
        "https://",
    )

    result = []

    for line in lines:
        line = clean(line)

        if len(line) < 20:
            continue

        low = line.lower()

        if any(x in low for x in bad_phrases):
            continue

        if low.startswith(("www.", "http://", "https://")):
            continue

        result.append(line)

    return result


def parse_sections(answer):
    sections = {}
    current = None

    for raw in str(answer or "").splitlines():
        line = raw.strip()

        if not line:
            continue

        if line.startswith("##"):
            current = re.sub(
                r"^#+\s*",
                "",
                line,
            ).strip().lower()

            sections[current] = []
            continue

        if current:
            line = re.sub(
                r"^[•*\-]\s*",
                "",
                line,
            ).strip()

            if line:
                sections[current].append(line)

    return sections


# ============================================================
# HIGH-CONFIDENCE LOCAL KNOWLEDGE
#
# These are deliberately short, stable definitions.
# They are a safety net when an internet provider fails,
# not a replacement for the internet-first architecture.
# ============================================================

KNOWLEDGE = {

    "keyboard": {
        "definition":
            "A keyboard is an input device used to enter text, numbers, commands, and other information into a computer or electronic device.",
        "explanation": [
            "A keyboard contains keys that send signals to a computer when they are pressed.",
            "Common keys include letters, numbers, function keys, modifier keys, and navigation keys.",
        ],
        "uses": [
            "Entering text and numbers.",
            "Giving commands and shortcuts to software.",
            "Controlling and navigating computer applications.",
        ],
    },

    "tobacco": {
        "definition":
            "Tobacco is a plant of the Nicotiana genus whose cured leaves are used to make tobacco products that contain nicotine.",
        "explanation": [
            "Nicotine is an addictive substance found naturally in tobacco.",
            "Tobacco products include cigarettes, cigars, pipe tobacco, and other products made from tobacco leaves.",
        ],
        "uses": [
            "Tobacco leaves are processed into various tobacco products.",
        ],
        "disadvantages": [
            "Tobacco use can cause serious health problems.",
            "Nicotine can lead to dependence.",
        ],
    },

    "chronicle": {
        "definition":
            "A chronicle is a historical record of events arranged in the order in which they occurred.",
        "explanation": [
            "Chronicles record events over a period of time, often from the perspective of the person who recorded them.",
            "A chronicle can describe the history of a person, place, community, country, or period.",
        ],
        "examples": [
            "Historical chronicles can record the events of a particular kingdom or period.",
        ],
    },

    "computer": {
        "definition":
            "A computer is an electronic machine that processes data according to instructions called programs.",
        "explanation": [
            "Computers can receive input, process information, store data, and produce output.",
            "Modern computers can perform many different tasks by running different software programs.",
        ],
        "uses": [
            "Communication and internet access.",
            "Creating and editing documents.",
            "Programming and data processing.",
            "Education, business, and entertainment.",
        ],
    },

    "decoder": {
        "definition":
            "A decoder is a digital logic circuit that converts coded input information into one or more corresponding output signals.",
        "explanation": [
            "A decoder commonly uses binary input lines to select one of several output lines.",
            "Decoders are important components in digital electronics and computer systems.",
        ],
        "uses": [
            "Memory address selection.",
            "Instruction decoding.",
            "Digital display control.",
        ],
    },

    "linux": {
        "definition":
            "Linux is a family of open-source operating systems built around the Linux kernel.",
        "explanation": [
            "The Linux kernel manages hardware resources and provides core services for operating-system software.",
            "Linux distributions combine the kernel with system software, applications, and package-management tools.",
        ],
        "uses": [
            "Desktop and laptop computers.",
            "Servers and cloud systems.",
            "Embedded devices and development systems.",
        ],
    },

    "arduino": {
        "definition":
            "Arduino is an open-source electronics platform based on programmable microcontroller boards and development software.",
        "explanation": [
            "Arduino boards can read sensors, control electronic components, and communicate with other devices.",
            "Programs for Arduino boards are commonly written using the Arduino programming environment.",
        ],
        "uses": [
            "Electronics projects.",
            "Sensor experiments.",
            "Automation and control systems.",
            "Learning microcontroller programming.",
        ],
    },

    "hvac": {
        "definition":
            "HVAC stands for heating, ventilation, and air conditioning, the systems used to control indoor temperature, air movement, and air quality.",
        "explanation": [
            "HVAC systems can heat or cool spaces and provide ventilation.",
            "HVAC equipment includes components such as fans, compressors, heat exchangers, filters, and control systems.",
        ],
        "uses": [
            "Temperature control.",
            "Ventilation.",
            "Indoor air-quality management.",
        ],
    },

    "internet": {
        "definition":
            "The Internet is a worldwide network of interconnected computer networks that communicate using standard Internet protocols.",
        "explanation": [
            "The Internet allows computers and other devices to exchange information and access network services.",
            "The World Wide Web is one service that operates over the Internet.",
        ],
        "uses": [
            "Communication.",
            "Information access.",
            "Online education.",
            "Cloud services.",
        ],
    },

    "database": {
        "definition":
            "A database is an organized collection of data that can be stored, searched, managed, and updated.",
        "explanation": [
            "Database systems provide ways to organize information and retrieve it efficiently.",
            "Many databases use structured queries to create, read, update, and delete data.",
        ],
        "uses": [
            "Storing application data.",
            "Managing records.",
            "Searching and analyzing information.",
        ],
    },
}


def local_knowledge(question):
    target = target_from_question(question)

    if not target:
        return None

    key = clean(target).lower()

    if key not in KNOWLEDGE:
        return None

    data = KNOWLEDGE[key]

    output = [
        "## Definition",
        data["definition"],
        "",
    ]

    if data.get("explanation"):
        output.append("## Explanation")

        for item in data["explanation"]:
            output.append("• " + item)

        output.append("")

    for section in (
        "examples",
        "uses",
        "advantages",
        "disadvantages",
    ):
        items = data.get(section)

        if not items:
            continue

        output.append(
            "## " + section.capitalize()
        )

        for item in items:
            output.append("• " + item)

        output.append("")

    output.extend([
        "## Summary",
        data["definition"],
    ])

    return "\n".join(output)


# ============================================================
# MAIN REPAIR
# ============================================================

def guard_answer(question, answer):

    target = target_from_question(question)

    if not target:
        return answer

    # If the engine produced a generic placeholder, replace it
    # with high-confidence local knowledge when available.
    if is_generic_fallback(answer):
        local = local_knowledge(question)

        if local:
            return local

        return answer

    sections = parse_sections(answer)

    if not sections:
        return answer

    definition_lines = remove_bad_lines(
        sections.get("definition", []),
        target,
    )

    explanation_lines = remove_bad_lines(
        sections.get("explanation", []),
        target,
    )

    summary_lines = remove_bad_lines(
        sections.get("summary", []),
        target,
    )

    # --------------------------------------------------------
    # Remove unrelated entity results.
    # --------------------------------------------------------

    def relevant(lines):
        output = []

        for line in lines:

            low = line.lower()

            # Known search contamination.
            unrelated = (
                "journalist",
                "actor",
                "actress",
                "film directed",
                "american film",
                "documentary film",
                "lawsuit",
                "television series",
                "album",
                "song by",
            )

            if any(x in low for x in unrelated):
                continue

            if not contains_target(line, target):
                continue

            output.append(line)

        return output

    definition_lines = relevant(definition_lines)
    explanation_lines = relevant(explanation_lines)
    summary_lines = relevant(summary_lines)

    # --------------------------------------------------------
    # Prefer a strong existing definition.
    # --------------------------------------------------------

    definition = None

    for line in definition_lines:
        if len(line) >= 25:
            definition = line
            break

    if not definition:
        for line in explanation_lines:
            if len(line) >= 25:
                definition = line
                break

    # --------------------------------------------------------
    # If filtering destroyed the answer, use local knowledge.
    # --------------------------------------------------------

    if not definition:
        local = local_knowledge(question)

        if local:
            return local

        # Keep original answer rather than inventing a bad one.
        return answer

    # --------------------------------------------------------
    # Explanation.
    # --------------------------------------------------------

    explanation = []

    for line in explanation_lines:
        if line == definition:
            continue

        if line not in explanation:
            explanation.append(line)

        if len(explanation) >= 4:
            break

    # --------------------------------------------------------
    # Summary.
    # --------------------------------------------------------

    summary = definition

    # --------------------------------------------------------
    # Rebuild.
    # --------------------------------------------------------

    output = [
        "## Definition",
        definition,
        "",
    ]

    if explanation:
        output.append("## Explanation")

        for line in explanation:
            output.append("• " + line)

        output.append("")

    for section_name in (
        "examples",
        "uses",
        "advantages",
        "disadvantages",
    ):

        items = []

        for line in sections.get(section_name, []):
            line = clean(line)

            if not line:
                continue

            if not contains_target(line, target):
                continue

            items.append(line)

        if items:
            output.append(
                "## " + section_name.capitalize()
            )

            for line in items[:4]:
                output.append("• " + line)

            output.append("")

    output.extend([
        "## Summary",
        summary,
    ])

    return "\n".join(output).strip()


repair_answer = guard_answer
filter_answer = guard_answer

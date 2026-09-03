"""
CONNY AI V13 response repair layer.

Purpose:
- repair clearly unrelated legacy answers
- provide reliable core electrical explanations
- support natural follow-up questions
- avoid automatic voice playback
"""

_LAST_TOPIC = None
_LAST_ANSWER = None


def _topic_from_text(text):
    q = str(text or "").lower().strip()

    topics = (
        ("python", ("python",)),
        ("arduino", ("arduino",)),
        ("hvac", ("hvac", "heating ventilation air conditioning")),
        ("diode", ("diode",)),
        ("electricity", ("electricity",)),
        ("electric_current", ("electric current", "electrical current", "current")),
        ("voltage", ("voltage", "potential difference")),
        ("electric_charge", ("electric charge", "electrical charge")),
        ("circuit", ("electric circuit", "electrical circuit", "circuit")),
        ("fan", ("fan", "motor")),
        ("computer", ("computer",)),
    )

    for topic, words in topics:
        if any(w in q for w in words):
            return topic

    return None


def _followup_kind(text):
    q = str(text or "").lower().strip()

    if any(x in q for x in (
        "what is it used for",
        "what's it used for",
        "what is this used for",
        "what is that used for",
        "what do you use it for",
        "what do we use it for",
        "its use",
        "its uses",
        "use of it",
        "uses of it",
    )):
        return "use"

    if q in {
        "example",
        "an example",
        "give an example",
        "give me an example",
        "simple example",
        "for example",
    }:
        return "example"

    if (
        q == "difference"
        or "what is the difference" in q
        or "difference between" in q
        or "different between" in q
    ):
        return "difference"

    return None


def _topic_answer(topic, kind):
    if topic == "python":
        if kind == "use":
            return (
                "Python is used to build software, automate tasks, "
                "analyze data, develop websites, and create AI systems."
            )
        if kind == "example":
            return (
                'A simple Python example is: print("Hello, world!")'
            )

    if topic == "arduino":
        if kind == "use":
            return (
                "Arduino is used to control electronic projects. "
                "It can read sensors, control LEDs, motors and relays, "
                "and automate physical systems."
            )
        if kind == "example":
            return (
                "For example, an Arduino can read a temperature sensor "
                "and switch a fan on when the temperature becomes high."
            )

    if topic == "hvac":
        if kind == "use":
            return (
                "HVAC systems are used to control heating, cooling, "
                "ventilation, humidity and indoor air quality in buildings "
                "and vehicles."
            )
        if kind == "example":
            return (
                "For example, an air-conditioning system can remove heat "
                "from a room and circulate cooler air through the space."
            )

    if topic == "diode":
        if kind == "use":
            return (
                "A diode is commonly used to allow current to flow mainly "
                "in one direction, protect circuits from reverse polarity, "
                "rectify AC into DC, and control signals."
            )
        if kind == "example":
            return (
                "For example, a diode can be placed in a circuit to help "
                "prevent current from flowing backward into a component."
            )

    if topic == "electricity":
        if kind == "use":
            return (
                "Electrical energy is used to power devices such as bulbs, "
                "fans, motors, computers and other electrical equipment."
            )
        if kind == "example":
            return (
                "For example, a battery can provide electrical energy to "
                "a small bulb, causing current to flow and the bulb to light."
            )

    if topic == "electric_current":
        if kind == "use":
            return (
                "Electric current is the flow of electric charge through "
                "a conductor. It is what transfers electrical energy through "
                "a working circuit."
            )
        if kind == "example":
            return (
                "For example, when a battery, wires and bulb form a closed "
                "circuit, electric current flows through the bulb."
            )

    if topic == "voltage":
        if kind == "use":
            return (
                "Voltage provides the electrical potential difference that "
                "can drive current through a circuit."
            )
        if kind == "example":
            return (
                "For example, a 9 V battery provides a 9-volt potential "
                "difference between its terminals."
            )

    if topic == "fan":
        if kind == "use":
            return (
                "An electric fan uses electrical energy to power its motor. "
                "The motor converts that electrical energy into mechanical "
                "motion that rotates the blades and moves air."
            )
        if kind == "example":
            return (
                "For example, when a fan is connected to its rated power "
                "source, current flows through its motor and the motor "
                "rotates the blades to move air."
            )

    if topic == "computer":
        if kind == "use":
            return (
                "A computer is used to process information and run software. "
                "It can be used for communication, programming, learning, "
                "data processing and many other tasks."
            )
        if kind == "example":
            return (
                "For example, a computer can run a program that reads data, "
                "processes it and displays the result on the screen."
            )

    if topic == "electric_charge":
        if kind == "use":
            return (
                "Electric charge is the property responsible for electrical "
                "interactions. Its movement in a conductor produces electric "
                "current."
            )
        if kind == "example":
            return (
                "For example, electrons carry negative electric charge, and "
                "their movement through a conductor contributes to electric current."
            )

    if topic == "circuit":
        if kind == "use":
            return (
                "An electric circuit provides a complete path for electric "
                "current to flow between electrical components."
            )
        if kind == "example":
            return (
                "A simple example is a battery connected by wires to a bulb. "
                "When the circuit is closed, current can flow and the bulb lights."
            )

    return None


def _difference_answer(topic):
    if topic in {"voltage", "electric_current"}:
        return (
            "Voltage and electric current are different but related. "
            "Voltage is the electrical potential difference that provides "
            "the push for charge to move, and it is measured in volts (V). "
            "Current is the flow of electric charge, and it is measured in "
            "amperes (A). In a simple analogy, voltage is like the pressure "
            "pushing water through a pipe, while current is like the amount "
            "of water flowing through it."
        )

    if topic == "electricity":
        return (
            "Electricity is the broader idea involving electric charge and "
            "electrical energy. Voltage describes potential difference, "
            "while current describes the flow of electric charge."
        )

    if topic == "diode":
        return (
            "A diode differs from a normal wire because it is designed to "
            "allow current mainly in one direction. A wire normally provides "
            "a low-resistance path in either direction."
        )

    if topic == "fan":
        return (
            "A fan and its power source have different roles. The power "
            "source provides electrical energy, while the fan motor converts "
            "that electrical energy into mechanical motion to rotate the blades."
        )

    return None


def _direct_electrical(q):
    if (
        "why does a fan need electricity" in q
        or "why does a fan need electric" in q
        or "why does a fan use electricity" in q
        or "why does a fan need power" in q
        or ("fan" in q and ("electricity" in q or "power" in q))
    ):
        return (
            "An electric fan needs electrical energy to run its motor. "
            "The motor converts electrical energy into mechanical motion, "
            "which rotates the blades and moves air. Without the required "
            "electrical power, the motor cannot produce that rotation."
        )

    if (
        "what is electric current" in q
        or "what is electrical current" in q
        or q == "current"
        or "flow of electrons" in q
        or "flow of electric charge" in q
    ):
        return (
            "Electric current is the flow of electric charge through a "
            "conductor. It is measured in amperes (A). For example, when "
            "a battery is connected to a bulb in a closed circuit, current "
            "flows through the circuit."
        )

    if "voltage" in q or "potential difference" in q:
        return (
            "Voltage is the electrical potential difference between two "
            "points. It provides the push that can cause electric charge "
            "to move through a circuit. Voltage is measured in volts (V)."
        )

    if "electric charge" in q or "electrical charge" in q:
        return (
            "Electric charge is a physical property of matter that can be "
            "positive or negative. Electrons carry negative electric charge, "
            "and moving charge can produce electric current."
        )

    if "electric circuit" in q or "electrical circuit" in q:
        return (
            "An electric circuit is a complete path through which electric "
            "current can flow. A simple circuit can contain a battery, wires "
            "and a bulb. When the circuit is closed, current can flow."
        )

    if (
        q == "electricity"
        or q == "what is electricity"
        or q == "what is electricity?"
        or "explain electricity" in q
        or "explain what electricity" in q
        or "tell me about electricity" in q
    ):
        return (
            "Electricity involves electric charge and electrical energy. "
            "In a simple circuit, a battery provides electrical energy that "
            "can cause charge to move through wires and a device such as "
            "a bulb. That movement of charge is electric current."
        )

    return None


def repair_response(user_text, response):
    global _LAST_TOPIC, _LAST_ANSWER

    query = str(user_text or "").strip()
    answer = str(response or "").strip()
    q = query.lower()

    topic = _topic_from_text(query)

    # Follow-up questions use the previous topic.
    kind = _followup_kind(query)
    if kind:
        use_topic = topic or _LAST_TOPIC

        if kind == "difference":
            fixed = _difference_answer(use_topic)
            if fixed:
                _LAST_ANSWER = fixed
                return fixed

        fixed = _topic_answer(use_topic, kind)
        if fixed:
            _LAST_ANSWER = fixed
            return fixed

    # Direct reliable electrical explanations.
    fixed = _direct_electrical(q)
    if fixed:
        _LAST_TOPIC = _topic_from_text(query) or _LAST_TOPIC
        _LAST_ANSWER = fixed
        return fixed

    # Detect obviously unrelated legacy answers.
    low = answer.lower()
    bad = (
        "cold war" in low
        or "contingency plan" in low
        or "search result" in low
        or "couldn't reason" in low
        or "runtime error" in low
        or "http://" in low
        or "https://" in low
    )

    if q in {"python", "what is python", "what's python"} and bad:
        answer = (
            "Python is a high-level programming language used to build "
            "software, automate tasks, analyze data, and create AI systems. "
            'For example: print("Hello, world!")'
        )

    elif "diode" in q and bad:
        answer = (
            "A diode is an electronic component that mainly allows electric "
            "current to flow in one direction. It can be used for rectification "
            "and circuit protection."
        )

    new_topic = _topic_from_text(query)
    if new_topic:
        _LAST_TOPIC = new_topic

    _LAST_ANSWER = answer
    return answer

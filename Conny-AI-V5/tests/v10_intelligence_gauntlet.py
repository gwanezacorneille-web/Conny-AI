import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from brain.brain import Brain
import traceback
import re
import sys


# ============================================================
# CONNY AI V10 — INTELLIGENCE GAUNTLET
# Diagnostic / Regression Test
# ============================================================

PASS = 0
FAIL = 0
ERROR = 0


def normalize(text):
    if text is None:
        return ""

    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def contains_any(text, phrases):
    text = normalize(text)
    return any(normalize(p) in text for p in phrases)


def run_test(
    brain,
    name,
    user_text,
    expected_answer=None,
    expected_intent=None,
    expected_decision=None,
    answer_contains=None,
    answer_not_contains=None,
):
    global PASS, FAIL, ERROR

    print("\n" + "-" * 78)
    print(f"TEST: {name}")
    print(f"USER: {user_text}")

    try:
        answer = brain.process(user_text)

        answer_n = normalize(answer)
        intent = getattr(brain, "last_intent", None)
        decision = getattr(brain, "last_decision", None)

        failures = []

        # ----------------------------------------------------
        # ANSWER EXACT MATCH
        # ----------------------------------------------------
        if expected_answer is not None:
            if answer_n != normalize(expected_answer):
                failures.append(
                    f"ANSWER MISMATCH\n"
                    f"Expected: {expected_answer}\n"
                    f"Got:      {answer}"
                )

        # ----------------------------------------------------
        # ANSWER MUST CONTAIN
        # ----------------------------------------------------
        if answer_contains:
            missing = [
                phrase
                for phrase in answer_contains
                if normalize(phrase) not in answer_n
            ]

            if missing:
                failures.append(
                    "MISSING ANSWER CONTENT: "
                    + ", ".join(repr(x) for x in missing)
                )

        # ----------------------------------------------------
        # ANSWER MUST NOT CONTAIN
        # ----------------------------------------------------
        if answer_not_contains:
            found = [
                phrase
                for phrase in answer_not_contains
                if normalize(phrase) in answer_n
            ]

            if found:
                failures.append(
                    "UNEXPECTED ANSWER CONTENT: "
                    + ", ".join(repr(x) for x in found)
                )

        # ----------------------------------------------------
        # INTENT
        # ----------------------------------------------------
        if expected_intent is not None:
            if intent != expected_intent:
                failures.append(
                    f"INTENT MISMATCH\n"
                    f"Expected: {expected_intent}\n"
                    f"Got:      {intent}"
                )

        # ----------------------------------------------------
        # DECISION
        # ----------------------------------------------------
        if expected_decision is not None:
            if decision != expected_decision:
                failures.append(
                    f"DECISION MISMATCH\n"
                    f"Expected: {expected_decision}\n"
                    f"Got:      {decision}"
                )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------
        if failures:
            FAIL += 1

            print("❌ FAIL")
            print(f"ANSWER:   {answer}")
            print(f"INTENT:   {intent}")
            print(f"DECISION: {decision}")

            for failure in failures:
                print("\n" + failure)

        else:
            PASS += 1

            print("✅ PASS")
            print(f"ANSWER:   {answer}")
            print(f"INTENT:   {intent}")
            print(f"DECISION: {decision}")

    except Exception as exc:
        ERROR += 1

        print("💥 ERROR")
        print("Exception:", repr(exc))
        traceback.print_exc()


def section(title):
    print("\n\n")
    print("=" * 78)
    print(title)
    print("=" * 78)


def main():

    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                 CONNY AI V10 — INTELLIGENCE GAUNTLET                        ║
║                                                                              ║
║                 THE V10 MAFIA BOSS TEST                                    ║
║                                                                              ║
║        This test diagnoses CONNY. It does NOT modify CONNY's code.          ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    brain = Brain()

    # ========================================================
    # 1. COMPARISON
    # ========================================================

    section("1 — COMPARISON")

    comparison_tests = [
        (
            "Equal numbers",
            "are 10 and 10 equal",
            ["equal"],
        ),
        (
            "Unequal numbers",
            "are 10 and 5 equal",
            ["not equal"],
        ),
        (
            "Equal numbers — alternate wording",
            "is 7 equal to 7",
            ["equal"],
        ),
        (
            "Unequal numbers — alternate wording",
            "is 7 equal to 8",
            ["not equal"],
        ),
        (
            "Greater",
            "which is greater 10 or 5",
            ["10", "greater"],
        ),
        (
            "Smaller",
            "which is smaller 3 or 8",
            ["3", "smaller"],
        ),
        (
            "Greatest",
            "which is greatest 10 25 7",
            ["25"],
        ),
        (
            "Smallest",
            "which is smallest 10 25 7",
            ["7"],
        ),
        (
            "Compare equal values",
            "compare 5 and 5",
            ["equal"],
        ),
        (
            "Compare decimals",
            "which is greater 5.5 or 5.2",
            ["5.5"],
        ),
        (
            "Compare negative values",
            "which is greater -2 or -5",
            ["-2"],
        ),
        (
            "Large values",
            "which is greater 1000000 or 999999",
            ["1000000"],
        ),
    ]

    for name, text, expected in comparison_tests:
        run_test(
            brain,
            name,
            text,
            answer_contains=expected,
            expected_decision="comparison",
        )

    # ========================================================
    # 2. IDENTITY / BASIC CONVERSATION
    # ========================================================

    section("2 — CONVERSATION / IDENTITY")

    conversation_tests = [
        ("Greeting", "hello"),
        ("Greeting", "hi"),
        ("Greeting", "hey"),
        ("Identity", "who are you"),
        ("Capability", "what can you do"),
        ("Thanks", "thank you"),
        ("Goodbye", "bye"),
    ]

    for name, text in conversation_tests:
        run_test(
            brain,
            name,
            text,
        )

    # ========================================================
    # 3. DEFINITIONS
    # ========================================================

    section("3 — DEFINITIONS")

    definition_tests = [
        ("Python definition", "what is python"),
        ("RAM definition", "what is RAM"),
        ("ROM definition", "what is ROM"),
        ("Arduino definition", "what is Arduino"),
        ("AI definition", "what is artificial intelligence"),
    ]

    for name, text in definition_tests:
        run_test(
            brain,
            name,
            text,
        )

    # ========================================================
    # 4. EXPLANATIONS
    # ========================================================

    section("4 — EXPLANATIONS")

    explanation_tests = [
        ("Explain RAM", "explain RAM"),
        ("Explain Arduino", "explain Arduino"),
        ("Explain computer", "explain how a computer works"),
        ("Explain networking", "explain networking"),
    ]

    for name, text in explanation_tests:
        run_test(
            brain,
            name,
            text,
        )

    # ========================================================
    # 5. REASONING
    # ========================================================

    section("5 — REASONING")

    reasoning_tests = [
        ("Basic reasoning", "if all birds have wings and a sparrow is a bird, does it have wings"),
        ("Simple logic", "if 10 is greater than 5, is 10 greater than 3"),
        ("Arithmetic reasoning", "what is 5 plus 5"),
        ("Arithmetic", "what is 10 minus 3"),
        ("Arithmetic", "what is 4 times 5"),
    ]

    for name, text in reasoning_tests:
        run_test(
            brain,
            name,
            text,
        )

    # ========================================================
    # 6. CODING
    # ========================================================

    section("6 — CODING")

    coding_tests = [
        ("Python code", "write python code to add two numbers"),
        ("JavaScript code", "write javascript code to print hello"),
        ("C code", "write C code to print hello"),
        ("C++ code", "write C++ code to print hello"),
        ("HTML code", "write HTML code for a webpage"),
        ("CSS code", "write CSS for a button"),
    ]

    for name, text in coding_tests:
        run_test(
            brain,
            name,
            text,
        )

    # ========================================================
    # 7. MEMORY
    # ========================================================

    section("7 — MEMORY")

    memory_tests = [
        (
            "Remember fact",
            "remember my favorite language is Python",
        ),
        (
            "Remember another fact",
            "remember that my project is called CONNY AI",
        ),
        (
            "Recall favorite language",
            "what is my favorite language",
        ),
        (
            "Recall project",
            "what is my project called",
        ),
    ]

    for name, text in memory_tests:
        run_test(
            brain,
            name,
            text,
        )

    # ========================================================
    # 8. ROUTING
    # ========================================================

    section("8 — ROUTING")

    routing_tests = [
        ("Comparison routing", "which is greater 50 or 20"),
        ("Definition routing", "what is RAM"),
        ("Explanation routing", "explain RAM"),
        ("Coding routing", "write python code to calculate 2 plus 2"),
        ("Conversation routing", "hello Conny"),
    ]

    for name, text in routing_tests:
        run_test(
            brain,
            name,
            text,
        )

    # ========================================================
    # 9. NATURAL LANGUAGE VARIATIONS
    # ========================================================

    section("9 — NATURAL LANGUAGE VARIATIONS")

    variation_tests = [
        "Which one is bigger, 20 or 10?",
        "which number is larger 20 or 10",
        "IS 10 EQUAL TO 10?",
        "are 50 and 50 the same",
        "tell me which is smaller: 4 or 9",
        "compare 100 and 50",
        "what's greater, 99 or 100?",
    ]

    for text in variation_tests:
        run_test(
            brain,
            "Natural language variation",
            text,
            expected_decision="comparison",
        )

    # ========================================================
    # 10. EDGE CASES
    # ========================================================

    section("10 — EDGE CASES")

    edge_tests = [
        "",
        " ",
        "asdfghjkl",
        "hello!!!!",
        "what",
        "why",
        "123",
        "???",
        "compare",
        "equal",
    ]

    for text in edge_tests:
        run_test(
            brain,
            "Edge case",
            text,
        )

    # ========================================================
    # FINAL REPORT
    # ========================================================

    total = PASS + FAIL + ERROR

    print("\n\n")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                         FINAL GAUNTLET REPORT                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")

    print()
    print(f"TOTAL TESTS : {total}")
    print(f"PASSED      : {PASS}")
    print(f"FAILED      : {FAIL}")
    print(f"ERRORS      : {ERROR}")

    if total:
        score = (PASS / total) * 100
    else:
        score = 0

    print(f"SCORE       : {score:.2f}%")

    print()

    if ERROR:
        print("💥 V10 STATUS: CRITICAL — runtime errors detected")
    elif FAIL:
        print("⚠️  V10 STATUS: INTELLIGENCE ISSUES FOUND")
        print("    Do NOT move to V11 yet.")
    else:
        print("🏆 V10 STATUS: ALL TESTS PASSED")
        print("🚀 V11 MAY PROCEED")

    print()


if __name__ == "__main__":
    main()

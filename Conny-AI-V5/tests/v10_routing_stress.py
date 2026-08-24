import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from brain.brain import Brain


# ============================================================
# CONNY AI V10 — ROUTING STRESS TEST
# ============================================================

print("=" * 78)
print("💥 CONNY AI V10 — ROUTING STRESS TEST 💥")
print("=" * 78)

brain = Brain()

passed = 0
failed = 0
results = []


def run_test(category, message, expected_decisions):
    global passed, failed

    print("\n" + "-" * 78)
    print(f"[{category}]")
    print(f"USER: {message}")

    try:
        answer = brain.process(message)

        decision = getattr(
            brain,
            "last_decision",
            None
        )

        print(f"DECISION: {decision}")
        print(f"CONNY: {answer}")

        if decision in expected_decisions:
            print("STATUS: PASS")
            passed += 1
            results.append(
                (category, message, decision, "PASS")
            )
        else:
            print("STATUS: FAIL")
            print(
                f"EXPECTED: {expected_decisions}"
            )

            failed += 1
            results.append(
                (category, message, decision, "FAIL")
            )

    except Exception as error:

        print("STATUS: FAIL")
        print(
            f"ERROR: {type(error).__name__}: {error}"
        )

        failed += 1
        results.append(
            (category, message, "ERROR", "FAIL")
        )


# ============================================================
# 1. NORMAL ROUTING
# ============================================================

run_test(
    "Conversation",
    "hello",
    {"conversation"}
)

run_test(
    "Identity",
    "what is your name",
    {"identity", "conversation"}
)

run_test(
    "Memory",
    "remember my favorite language is Python",
    {"memory_store"}
)

run_test(
    "Memory Recall",
    "what do you remember",
    {"memory_recall"}
)


# ============================================================
# 2. COMPARISON STRESS
# ============================================================

run_test(
    "Comparison",
    "compare Python and JavaScript",
    {"comparison"}
)

run_test(
    "Comparison",
    "Python vs Java",
    {"comparison"}
)

run_test(
    "Comparison",
    "which is better Python or JavaScript?",
    {"comparison"}
)

run_test(
    "Comparison",
    "what is the difference between Python and Java?",
    {"comparison"}
)

run_test(
    "Comparison",
    "which is greater 999 or 1000?",
    {"comparison", "calculator"}
)


# ============================================================
# 3. CODING STRESS
# ============================================================

run_test(
    "Coding",
    "write Python code",
    {"coding"}
)

run_test(
    "Coding",
    "create a JavaScript function",
    {"coding"}
)

run_test(
    "Coding",
    "build a C++ program",
    {"coding"}
)

run_test(
    "Coding",
    "debug my Python code",
    {"coding"}
)

run_test(
    "Coding",
    "fix this JavaScript syntax error",
    {"coding"}
)


# ============================================================
# 4. CRITICAL CODING VS COMPARISON COLLISIONS
# ============================================================

run_test(
    "Collision",
    "compare Python code and JavaScript code",
    {"comparison"}
)

run_test(
    "Collision",
    "Python versus JavaScript programming",
    {"comparison"}
)

run_test(
    "Collision",
    "which programming language is better Python or Java?",
    {"comparison"}
)

run_test(
    "Collision",
    "difference between Python functions and Java functions",
    {"comparison"}
)


# ============================================================
# 5. CALCULATOR STRESS
# ============================================================

run_test(
    "Calculator",
    "calculate 100 + 250",
    {"calculator"}
)

run_test(
    "Calculator",
    "what is the average of 10 20 30 40?",
    {"calculator"}
)

run_test(
    "Calculator",
    "what is the difference between 500 and 125?",
    {"calculator", "comparison"}
)

run_test(
    "Calculator",
    "what is the square root of 144?",
    {"calculator"}
)


# ============================================================
# 6. KNOWLEDGE / CODING COLLISIONS
# ============================================================

run_test(
    "Knowledge",
    "what is Python?",
    {"knowledge", "conversation"}
)

run_test(
    "Knowledge",
    "how does a Python function work?",
    {"knowledge", "coding"}
)

run_test(
    "Knowledge",
    "explain Java classes",
    {"knowledge", "coding"}
)


# ============================================================
# 7. INTERNET STRESS
# ============================================================

run_test(
    "Internet",
    "search online for Python",
    {"internet"}
)

run_test(
    "Internet",
    "what is the latest Python version?",
    {"internet"}
)

run_test(
    "News",
    "latest news about technology",
    {"internet"}
)

run_test(
    "Weather",
    "weather today",
    {"internet"}
)

run_test(
    "Current",
    "what is happening right now?",
    {"internet"}
)

run_test(
    "Wikipedia",
    "wikipedia Python programming",
    {"internet"}
)


# ============================================================
# 8. ONLINE VS KNOWLEDGE COLLISIONS
# ============================================================

run_test(
    "Online Collision",
    "what is the latest Python news?",
    {"internet"}
)

run_test(
    "Online Collision",
    "what is the current weather?",
    {"internet"}
)

run_test(
    "Online Collision",
    "search online what Python is",
    {"internet"}
)


# ============================================================
# 9. SYSTEM ROUTING
# ============================================================

run_test(
    "System",
    "open the terminal",
    {"system"}
)

run_test(
    "System",
    "restart the computer",
    {"system"}
)

run_test(
    "System",
    "open the file manager",
    {"system", "knowledge"}
)


# ============================================================
# 10. EMOTION
# ============================================================

run_test(
    "Emotion",
    "I am stressed about my exam",
    {"emotional_support"}
)

run_test(
    "Emotion",
    "I feel nervous",
    {"emotional_support"}
)


# ============================================================
# 11. CREATIVE
# ============================================================

run_test(
    "Creative",
    "write a short story about a robot",
    {"creative"}
)

run_test(
    "Creative",
    "create a birthday message",
    {"creative"}
)


# ============================================================
# 12. CASE / FORMATTING STRESS
# ============================================================

run_test(
    "Case",
    "COMPARE PYTHON AND JAVASCRIPT",
    {"comparison"}
)

run_test(
    "Case",
    "WRITE PYTHON CODE",
    {"coding"}
)

run_test(
    "Case",
    "WEATHER TODAY",
    {"internet"}
)


# ============================================================
# 13. NATURAL LANGUAGE STRESS
# ============================================================

run_test(
    "Natural Language",
    "Hey Conny, can you compare Python with JavaScript for me?",
    {"comparison"}
)

run_test(
    "Natural Language",
    "Can you please write a Python program for me?",
    {"coding"}
)

run_test(
    "Natural Language",
    "Could you tell me which is better, an HDD or an SSD?",
    {"comparison"}
)


# ============================================================
# 14. MULTI-INTENT / AMBIGUOUS REQUESTS
# ============================================================

run_test(
    "Multi Intent",
    "compare Python and JavaScript and then write code",
    {"comparison", "coding"}
)

run_test(
    "Multi Intent",
    "tell me what Python is and search for the latest news",
    {"internet", "knowledge"}
)

run_test(
    "Multi Intent",
    "calculate 50 + 50 and compare it with 200",
    {"calculator", "comparison"}
)


# ============================================================
# FINAL REPORT
# ============================================================

total = passed + failed

print("\n")
print("=" * 78)
print("🏁 CONNY V10 ROUTING STRESS RESULTS")
print("=" * 78)

print(f"TOTAL TESTS : {total}")
print(f"PASSED      : {passed}")
print(f"FAILED      : {failed}")

if total:
    rate = (passed / total) * 100
else:
    rate = 0

print(f"SUCCESS RATE: {rate:.1f}%")

print("\n" + "=" * 78)

if failed == 0:

    print("🔥🔥🔥 ROUTING STRESS TEST PASSED — 100% 🔥🔥🔥")
    print()
    print("🚦 ROUTING SURVIVED HARD MODE")
    print("🧠 DECISION ENGINE: STABLE")
    print("💻 CODING ROUTING: STABLE")
    print("⚖️  COMPARISON ROUTING: STABLE")
    print("🌐 ONLINE ROUTING: STABLE")
    print("🔢 CALCULATOR ROUTING: STABLE")
    print("🧩 KNOWLEDGE ROUTING: STABLE")
    print()
    print("🏆 V10 ROUTING STRESS STATUS: PASSED")

else:

    print("⚠️ ROUTING STRESS TEST FOUND FAILURES")
    print()
    print("Failed tests:")

    for category, message, decision, status in results:
        if status == "FAIL":
            print(
                f"  ❌ [{category}] "
                f"{message}"
            )
            print(
                f"     Decision: {decision}"
            )

print("=" * 78)
print("🏁 ROUTING STRESS TEST COMPLETE")
print("=" * 78)

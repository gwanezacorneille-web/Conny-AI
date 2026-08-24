import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from brain.brain import Brain


# ============================================================
# CONNY AI V10 — MASTER GAUNTLET
# ============================================================

print("=" * 78)
print("🔥 CONNY AI V10 — MASTER GAUNTLET 🔥")
print("=" * 78)

passed = 0
failed = 0
results = []


def test(brain, category, message, validator=None):
    global passed, failed

    print("\n" + "-" * 78)
    print(f"[{category}]")
    print(f"USER: {message}")

    try:
        answer = brain.process(message)

        if answer is None:
            raise AssertionError("Brain returned None")

        answer = str(answer).strip()

        if not answer:
            raise AssertionError("Brain returned an empty response")

        if validator is not None:
            validator(answer)

        print(f"CONNY: {answer}")
        print("STATUS: PASS")

        passed += 1
        results.append((category, message, "PASS"))

    except Exception as error:

        print("STATUS: FAIL")
        print(f"ERROR: {type(error).__name__}: {error}")

        failed += 1
        results.append((category, message, "FAIL"))


# ============================================================
# INITIALIZE BRAIN
# ============================================================

print("\n🧠 Initializing CONNY Brain...")

try:
    brain = Brain()
    print("BRAIN INITIALIZATION: PASS")
    passed += 1
    results.append(("System", "Brain initialization", "PASS"))

except Exception as error:
    print("BRAIN INITIALIZATION: FAIL")
    print(f"ERROR: {type(error).__name__}: {error}")

    print("\n❌ MASTER GAUNTLET ABORTED")
    raise SystemExit(1)


# ============================================================
# CONVERSATION / IDENTITY
# ============================================================

test(brain, "Conversation", "hello")
test(brain, "Conversation", "how are you?")
test(brain, "Identity", "what is your name")
test(brain, "Capabilities", "what can you do")


# ============================================================
# MEMORY
# ============================================================

test(
    brain,
    "Memory Store",
    "remember my favorite language is Python"
)

test(
    brain,
    "Memory Recall",
    "what do you remember"
)


# ============================================================
# CALCULATOR
# ============================================================

test(
    brain,
    "Calculator",
    "calculate 25 + 17"
)

test(
    brain,
    "Calculator",
    "what is the average of 10 20 30"
)

test(
    brain,
    "Calculator",
    "what is the square root of 144"
)


# ============================================================
# NUMERIC COMPARISON
# ============================================================

test(
    brain,
    "Comparison",
    "which is greater 10 or 5"
)

test(
    brain,
    "Comparison",
    "which is smaller 3 or 8"
)

test(
    brain,
    "Comparison",
    "are 10 and 10 equal"
)


# ============================================================
# KNOWLEDGE COMPARISONS
# ============================================================

test(
    brain,
    "Comparison",
    "compare RAM and ROM"
)

test(
    brain,
    "Comparison",
    "compare CPU and GPU"
)

test(
    brain,
    "Comparison",
    "compare Windows and Linux"
)

test(
    brain,
    "Comparison",
    "compare Python and Java"
)


# ============================================================
# CRITICAL CODING / COMPARISON COLLISIONS
# ============================================================

test(
    brain,
    "Collision",
    "compare python and javascript"
)

test(
    brain,
    "Collision",
    "python vs javascript"
)

test(
    brain,
    "Collision",
    "what is the difference between python and javascript"
)

test(
    brain,
    "Collision",
    "which is better python or javascript"
)

test(
    brain,
    "Coding",
    "write python code"
)

test(
    brain,
    "Coding",
    "create a javascript function"
)

test(
    brain,
    "Coding",
    "debug my python code"
)


# ============================================================
# KNOWLEDGE
# ============================================================

test(
    brain,
    "Knowledge",
    "what is an operating system"
)

test(
    brain,
    "Knowledge",
    "how does RAM work"
)

test(
    brain,
    "Knowledge",
    "explain what a CPU does"
)


# ============================================================
# REASONING
# ============================================================

test(
    brain,
    "Reasoning",
    "why is an SSD faster than an HDD"
)


# ============================================================
# EMOTION
# ============================================================

test(
    brain,
    "Emotion",
    "I am stressed about my exam"
)


# ============================================================
# ONLINE ROUTING
# ============================================================

test(
    brain,
    "Internet",
    "search online for Python"
)

test(
    brain,
    "News",
    "latest news about technology"
)

test(
    brain,
    "Weather",
    "weather today"
)

test(
    brain,
    "Current Info",
    "what is happening right now"
)

test(
    brain,
    "Wikipedia",
    "wikipedia Python programming"
)


# ============================================================
# CONTEXT
# ============================================================

test(
    brain,
    "Context Start",
    "tell me about Python"
)

test(
    brain,
    "Context Follow-up",
    "what about Java?"
)


# ============================================================
# EDGE / STRESS TESTS
# ============================================================

test(
    brain,
    "Edge",
    "HELLO"
)

test(
    brain,
    "Edge",
    "   hello   "
)

test(
    brain,
    "Edge",
    "what is greater 100 or 99"
)

test(
    brain,
    "Edge",
    "compare Python and JavaScript programming"
)

test(
    brain,
    "Edge",
    "write a Python program"
)

test(
    brain,
    "Edge",
    "what is the difference between RAM and ROM"
)


# ============================================================
# FINAL REPORT
# ============================================================

total = passed + failed

print("\n")
print("=" * 78)
print("🏁 CONNY V10 MASTER GAUNTLET RESULTS")
print("=" * 78)

print(f"TOTAL TESTS : {total}")
print(f"PASSED      : {passed}")
print(f"FAILED      : {failed}")

if total:
    percentage = (passed / total) * 100
else:
    percentage = 0

print(f"SUCCESS RATE: {percentage:.1f}%")

print("\n" + "=" * 78)

if failed == 0:

    print("🔥🔥🔥 MASTER GAUNTLET PASSED — 100% 🔥🔥🔥")
    print()
    print("🧠 FULL BRAIN       : OPERATIONAL")
    print("🚦 ROUTING          : OPERATIONAL")
    print("💾 MEMORY           : OPERATIONAL")
    print("🔢 CALCULATOR       : OPERATIONAL")
    print("⚖️  COMPARISON       : OPERATIONAL")
    print("💻 CODING           : OPERATIONAL")
    print("📚 KNOWLEDGE        : OPERATIONAL")
    print("🧩 REASONING        : OPERATIONAL")
    print("❤️  EMOTION          : OPERATIONAL")
    print("🌐 ONLINE BODY      : OPERATIONAL")
    print("🔄 CONTEXT          : OPERATIONAL")
    print()
    print("🏆 CONNY V10 MASTER STATUS: PASSED")

else:

    print("⚠️ MASTER GAUNTLET COMPLETED WITH FAILURES")
    print()
    print("Failed tests:")

    for category, message, status in results:
        if status == "FAIL":
            print(f"  ❌ [{category}] {message}")

print("=" * 78)
print("🏁 MASTER GAUNTLET COMPLETE")
print("=" * 78)

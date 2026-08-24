import sys
import re
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
PYTHON = PROJECT_ROOT / "conny_env" / "bin" / "python"

print("=" * 78)
print("🏆 CONNY AI V10 — FINAL FIXTURE 🏆")
print("=" * 78)
print()
print("🧠 MASTER GAUNTLET")
print("🚦 ROUTING STRESS")
print("🐛 ROUTING REGRESSIONS")
print("🔄 FULL Brain.process() PIPELINE")
print()

suite_results = []


def run_suite(name, filename):
    print("\n" + "=" * 78)
    print(f"▶ RUNNING {name}")
    print("=" * 78)

    try:
        result = subprocess.run(
            [str(PYTHON), str(PROJECT_ROOT / "tests" / filename)],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
        )

        output = result.stdout + result.stderr

        # Show the actual suite output.
        print(output)

        total_match = re.search(r"TOTAL TESTS\s*:\s*(\d+)", output)
        passed_match = re.search(r"PASSED\s*:\s*(\d+)", output)
        failed_match = re.search(r"FAILED\s*:\s*(\d+)", output)

        if not total_match or not passed_match or not failed_match:
            print(f"❌ {name}: could not parse final test summary")
            suite_results.append((name, 0, 0, 1))
            return

        total = int(total_match.group(1))
        passed = int(passed_match.group(1))
        failed = int(failed_match.group(1))

        suite_results.append((name, total, passed, failed))

        if failed == 0 and result.returncode == 0:
            print(f"✅ {name}: PASSED")
        else:
            print(f"❌ {name}: FAILED")

    except Exception as error:
        print(f"❌ {name}: {type(error).__name__}: {error}")
        suite_results.append((name, 0, 0, 1))


# ============================================================
# EXISTING V10 TEST SUITES
# ============================================================

run_suite(
    "V10 MASTER GAUNTLET",
    "v10_master_gauntlet.py"
)

run_suite(
    "V10 ROUTING STRESS",
    "v10_routing_stress.py"
)


# ============================================================
# FOUR CRITICAL ROUTING REGRESSIONS
# ============================================================

print("\n" + "=" * 78)
print("🐛 V10 ROUTING REGRESSION TESTS")
print("=" * 78)

from brain.brain import Brain

brain = Brain()

regressions = [
    (
        "Coding-vs-Comparison #1",
        "compare Python code and JavaScript code",
        {"comparison"},
    ),
    (
        "Coding-vs-Comparison #2",
        "Python versus JavaScript programming",
        {"comparison"},
    ),
    (
        "Coding-vs-Comparison #3",
        "which programming language is better Python or Java?",
        {"comparison"},
    ),
    (
        "Coding-vs-Comparison #4",
        "difference between Python functions and Java functions",
        {"comparison"},
    ),
]

reg_passed = 0
reg_failed = 0

for name, message, expected in regressions:

    print("\n" + "-" * 78)
    print(f"[REGRESSION] {name}")
    print(f"USER: {message}")

    try:
        answer = brain.process(message)
        decision = getattr(brain, "last_decision", None)

        print(f"DECISION: {decision}")
        print(f"CONNY: {answer}")

        if decision in expected and answer is not None and str(answer).strip():
            print("STATUS: PASS")
            reg_passed += 1
        else:
            print("STATUS: FAIL")
            print(f"EXPECTED DECISION: {expected}")
            reg_failed += 1

    except Exception as error:
        print("STATUS: FAIL")
        print(f"ERROR: {type(error).__name__}: {error}")
        reg_failed += 1


suite_results.append(
    ("V10 ROUTING REGRESSIONS", 4, reg_passed, reg_failed)
)


# ============================================================
# FINAL AGGREGATION
# ============================================================

total_tests = sum(item[1] for item in suite_results)
total_passed = sum(item[2] for item in suite_results)
total_failed = sum(item[3] for item in suite_results)

print("\n")
print("=" * 78)
print("🏁 CONNY V10 FINAL FIXTURE RESULTS")
print("=" * 78)

print()

for name, total, passed, failed in suite_results:
    print(f"{name}")
    print(f"  TOTAL  : {total}")
    print(f"  PASSED : {passed}")
    print(f"  FAILED : {failed}")
    print()

print("=" * 78)

print(f"TOTAL TESTS : {total_tests}")
print(f"PASSED      : {total_passed}")
print(f"FAILED      : {total_failed}")

if total_tests:
    percentage = (total_passed / total_tests) * 100
else:
    percentage = 0

print(f"SUCCESS RATE: {percentage:.1f}%")

print("=" * 78)

if total_failed == 0 and total_tests == total_passed:

    print()
    print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
    print()
    print("🏆 CONNY V10 FINAL FIXTURE: PASSED")
    print()
    print("🧠 FULL BRAIN       : OPERATIONAL")
    print("🚦 ROUTING          : OPERATIONAL")
    print("💾 MEMORY           : OPERATIONAL")
    print("🔢 CALCULATOR       : OPERATIONAL")
    print("⚖️  COMPARISON      : OPERATIONAL")
    print("💻 CODING           : OPERATIONAL")
    print("📚 KNOWLEDGE        : OPERATIONAL")
    print("🧩 REASONING        : OPERATIONAL")
    print("❤️  EMOTION         : OPERATIONAL")
    print("🌐 ONLINE BODY      : OPERATIONAL")
    print("🔄 CONTEXT          : OPERATIONAL")
    print("🐛 REGRESSIONS      : FIXED")
    print()
    print("🚀 V10 FINAL STATUS: PASSED")
    print()
    print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")

    sys.exit(0)

else:

    print()
    print("⚠️ CONNY V10 FINAL FIXTURE: FAILED")
    print()
    print("V10 is NOT signed off.")
    print("Fix the failing cases and rerun this fixture.")
    print()

    sys.exit(1)

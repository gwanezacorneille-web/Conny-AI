"""CONNY AI V13 — stable adapter for the verified legacy Brain."""

from pathlib import Path
import os
import sys

CORE_ROOT = Path(
    os.environ.get(
        "CONNY_CORE_PATH",
        str(
            Path.home()
            / "Conny-AI"
            / "Conny-AI-V5-V13-BACKUP-20260827-231231"
        ),
    )
).expanduser().resolve()


class CoreAdapter:

    def __init__(self, core_path=None):
        self.core_root = (
            Path(core_path).expanduser().resolve()
            if core_path
            else CORE_ROOT
        )

        self.brain = None
        self.available = False
        self.error = None

        self._load()

    def _load(self):
        try:
            if not self.core_root.is_dir():
                raise FileNotFoundError(
                    f"Core directory not found: {self.core_root}"
                )

            brain_file = self.core_root / "brain" / "brain.py"

            if not brain_file.is_file():
                raise FileNotFoundError(
                    f"Brain not found: {brain_file}"
                )

            root = str(self.core_root)

            if root not in sys.path:
                sys.path.insert(0, root)

            os.environ["CONNY_CORE_PATH"] = root

            old_cwd = Path.cwd()

            try:
                os.chdir(self.core_root)

                from brain.brain import Brain

                self.brain = Brain()
                self.available = True
                self.error = None

            finally:
                os.chdir(old_cwd)

        except Exception as exc:
            self.available = False
            self.error = f"{type(exc).__name__}: {exc}"

    def status(self):
        return {
            "v13": True,
            "core_available": self.available,
            "core_root": str(self.core_root),
            "error": self.error,
        }

    def ask(self, message):

        if not isinstance(message, str):
            raise TypeError("message must be a string")

        message = message.strip()

        if not message:
            return {
                "ok": False,
                "response": "Please enter a message.",
            }

        if not self.available:
            return {
                "ok": False,
                "response": "CONNY AI core is unavailable.",
                "error": self.error,
            }

        old_cwd = Path.cwd()

        try:
            os.chdir(self.core_root)

            if hasattr(self.brain, "process"):
                result = self.brain.process(message)

            elif hasattr(self.brain, "respond"):
                result = self.brain.respond(message)

            elif hasattr(self.brain, "run"):
                result = self.brain.run(message)

            else:
                return {
                    "ok": False,
                    "response": "Core interface not recognized.",
                }

            return {
                "ok": True,
                "response": str(result),
            }

        except Exception as exc:

            return {
                "ok": False,
                "response": "CONNY AI encountered an internal error.",
                "error": f"{type(exc).__name__}: {exc}",
            }

        finally:
            os.chdir(old_cwd)


__all__ = [
    "CoreAdapter",
    "CORE_ROOT",
]

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path


class CoreRuntime:
    def __init__(self, core_path=None):
        if core_path is None:
            core_path = os.environ.get("CONNY_CORE_PATH")

        if core_path is None:
            core_path = Path(__file__).resolve().parents[2]

        self.core_path = Path(core_path).expanduser().resolve()
        self.loaded_module = None
        self.brain = None

    def _prepare_environment(self):
        if not self.core_path.is_dir():
            raise FileNotFoundError(
                f"CONNY core directory not found: {self.core_path}"
            )

        brain_file = self.core_path / "brain" / "brain.py"

        if not brain_file.is_file():
            raise FileNotFoundError(
                f"CONNY Brain not found: {brain_file}"
            )

        root = str(self.core_path)

        # Keep the real CONNY core root available for the entire
        # lifetime of the V13 process.  LanguageEngine and other
        # core modules may be imported after the first request.
        if root in sys.path:
            sys.path.remove(root)

        sys.path.insert(0, root)

        os.environ["CONNY_CORE_PATH"] = root

    def load(self):
        self._prepare_environment()

        old_cwd = Path.cwd()

        try:
            os.chdir(self.core_path)

            packages = (
                "conny",
                "brain",
                "memory",
                "database",
                "plugins",
                "internet",
                "knowledge",
                "router",
                "core",
            )

            for name in list(sys.modules):
                if any(
                    name == package or name.startswith(package + ".")
                    for package in packages
                ):
                    sys.modules.pop(name, None)

            brain_module = importlib.import_module("brain.brain")

            Brain = getattr(brain_module, "Brain", None)

            if Brain is None:
                raise ImportError(
                    "brain.brain does not expose Brain"
                )

            self.brain = Brain()
            self.loaded_module = brain_module

            return self.brain

        finally:
            os.chdir(old_cwd)

    def process(self, message):
        if self.brain is None:
            self.load()

        old_cwd = Path.cwd()

        try:
            os.chdir(self.core_path)

            if hasattr(self.brain, "process"):
                return self.brain.process(message)

            if hasattr(self.brain, "respond"):
                return self.brain.respond(message)

            if hasattr(self.brain, "run"):
                return self.brain.run(message)

            raise AttributeError(
                "Brain has no process/respond/run interface"
            )

        finally:
            os.chdir(old_cwd)

    def handle(self, request):
        message = getattr(request, "message", None)

        if not isinstance(message, str):
            raise TypeError(
                "V13 request must contain a string message"
            )

        return self.process(message)


ConnyCoreRuntime = CoreRuntime

__all__ = [
    "CoreRuntime",
    "ConnyCoreRuntime",
]

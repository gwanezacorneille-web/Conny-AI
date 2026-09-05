from pathlib import Path


V14_ROOT = Path(__file__).resolve().parents[1]


def version():
    return (V14_ROOT / "VERSION").read_text().strip()


def required_directories():
    return [
        "account",
        "memory",
        "security",
        "cloud",
        "settings",
        "v14_platform",
        "app",
        "regression",
        "release",
    ]


def validate_structure():
    return [
        directory
        for directory in required_directories()
        if not (V14_ROOT / directory).is_dir()
    ]

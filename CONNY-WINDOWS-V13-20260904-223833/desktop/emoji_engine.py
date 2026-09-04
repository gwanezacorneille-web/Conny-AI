"""
CONNY AI V13 — Stage 9.9.2
Emoji Recognition Layer
"""

import re


EMOJI_MEANINGS = {
    "😀": "happiness",
    "😃": "happiness and cheerfulness",
    "😄": "joy",
    "😁": "big smile and excitement",
    "😆": "laughter",
    "😅": "nervous laughter or relief",
    "😂": "strong laughter",
    "🤣": "extreme laughter",
    "😊": "warm happiness",
    "😇": "kindness or innocence",
    "🙂": "calm friendliness",
    "🙃": "playfulness or irony",
    "😉": "joking or playfulness",
    "😍": "admiration or affection",
    "🥰": "affection and warmth",
    "😎": "confidence or coolness",
    "🤔": "thinking or uncertainty",
    "🤨": "doubt or questioning",
    "😐": "neutral mood",
    "🙄": "annoyance or disbelief",
    "😢": "sadness",
    "😭": "strong sadness",
    "😡": "anger",
    "😠": "frustration",
    "😱": "fear or shock",
    "😳": "embarrassment or surprise",
    "🥺": "pleading or emotional appeal",
    "😴": "sleepiness",
    "🤗": "warmth or friendliness",
    "🤩": "amazement or excitement",
    "🥳": "celebration",
    "🤯": "shock or amazement",
    "👍": "approval or agreement",
    "👎": "disapproval or disagreement",
    "👏": "applause or congratulations",
    "🙌": "celebration or praise",
    "🙏": "thanks, gratitude, or request",
    "🤝": "agreement or cooperation",
    "✌️": "peace or victory",
    "👌": "approval",
    "💪": "strength or determination",
    "👋": "greeting or goodbye",
    "❤️": "love, care, or affection",
    "🧡": "warmth or care",
    "💛": "friendship or happiness",
    "💚": "care or positivity",
    "💙": "trust or calmness",
    "💜": "affection or support",
    "🖤": "sadness or affection",
    "🤍": "peace or care",
    "💯": "strong approval or perfection",
    "🔥": "excitement or something impressive",
    "⭐": "importance or excellence",
    "✨": "magic, excitement, or emphasis",
    "🎉": "celebration",
    "🎊": "celebration",
    "🎂": "birthday or celebration",
    "🎁": "gift or surprise",
    "❤️‍🔥": "strong affection or passion",
    "💔": "heartbreak or sadness",
    "⚡": "energy, speed, or power",
    "🌟": "special achievement or excellence",
    "🚀": "launch, progress, or ambition",
    "💡": "idea or inspiration",
    "🎯": "goal, focus, or accuracy",
    "🏆": "victory or achievement",
    "⚽": "football or soccer",
    "🏀": "basketball",
    "🎮": "gaming",
    "🎵": "music",
    "🎶": "music or singing",
    "📚": "books or studying",
    "💻": "computer or technology",
    "📱": "phone or mobile technology",
    "🌍": "Earth or the world",
    "☀️": "sun or brightness",
    "🌙": "night or moon",
    "☁️": "cloud or cloudy weather",
    "🌧️": "rain",
    "❄️": "cold, snow, or winter",
    "❤️": "love or care",
    "❓": "question",
    "❗": "important or urgent",
    "✅": "correct, complete, or success",
    "❌": "incorrect, failure, or rejection",
}


def extract_emojis(text: str):
    if not text:
        return []

    found = []

    for emoji in EMOJI_MEANINGS:
        if emoji in text and emoji not in found:
            found.append(emoji)

    return found


def recognize_emojis(text: str):
    emojis = extract_emojis(text)

    return {
        "emojis": emojis,
        "meanings": [EMOJI_MEANINGS[e] for e in emojis],
        "count": len(emojis),
    }


def emoji_context(text: str):
    result = recognize_emojis(text)

    if not result["emojis"]:
        return ""

    parts = []

    for emoji, meaning in zip(
        result["emojis"],
        result["meanings"]
    ):
        parts.append(f"{emoji}={meaning}")

    return "Emoji context: " + "; ".join(parts)


def contains_emoji(text: str):
    return bool(extract_emojis(text))


__all__ = [
    "EMOJI_MEANINGS",
    "extract_emojis",
    "recognize_emojis",
    "emoji_context",
    "contains_emoji",
]

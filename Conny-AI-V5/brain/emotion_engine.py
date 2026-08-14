class EmotionEngine:
    def __init__(self):
        self.emotions = {
            "happy": [
                "happy",
                "great",
                "awesome",
                "excited",
                "love",
                "wonderful",
                "amazing",
                "good"
            ],

            "sad": [
                "sad",
                "unhappy",
                "lonely",
                "cry",
                "bad"
            ],

            "angry": [
                "angry",
                "mad",
                "furious",
                "annoyed",
                "hate"
            ],

            "fear": [
                "afraid",
                "scared",
                "worried",
                "nervous",
                "fear"
            ],

            "confused": [
                "confused",
                "don't understand",
                "unclear",
                "lost"
            ]
        }


    def detect(self, message):
        message = message.lower()

        for emotion, words in self.emotions.items():
            for word in words:
                if word in message:
                    return {
                        "emotion": emotion,
                        "confidence": 0.8
                    }

        return {
            "emotion": "neutral",
            "confidence": 0.5
        }

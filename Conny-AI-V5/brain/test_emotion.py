from emotion_engine import EmotionEngine


emotion = EmotionEngine()


messages = [
    "I am very happy today",
    "I am angry with my PC",
    "I am worried about my exam",
    "I don't understand this",
    "Hello Conny"
]


for message in messages:
    print(message)
    print(emotion.detect(message))
    print("----------------")

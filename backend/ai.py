from transformers import pipeline

# Sentiment
sentiment_model = pipeline("sentiment-analysis")

# Emotion
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def analyze_text(text):
    sentiment_result = sentiment_model(text)[0]
    emotion_result = emotion_model(text)[0]

    return {
        "sentiment": sentiment_result["label"],
        "confidence": sentiment_result["score"],
        "emotion": emotion_result["label"]
    }
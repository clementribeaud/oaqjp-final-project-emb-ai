"""Client for the IBM Skills Network emotion prediction service."""

import requests

EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network"
    "/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_HEADER = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return the five emotion scores and the dominant emotion."""
    if not text_to_analyze or not text_to_analyze.strip():
        return dict.fromkeys((*EMOTIONS, "dominant_emotion"))

    response = requests.post(
        EMOTION_URL,
        headers=MODEL_HEADER,
        json={"raw_document": {"text": text_to_analyze}},
        timeout=15,
    )
    if response.status_code == 400:
        return dict.fromkeys((*EMOTIONS, "dominant_emotion"))

    response.raise_for_status()
    prediction = response.json()["emotionPredictions"][0]["emotion"]
    scores = {emotion: prediction[emotion] for emotion in EMOTIONS}
    return {**scores, "dominant_emotion": max(EMOTIONS, key=scores.__getitem__)}

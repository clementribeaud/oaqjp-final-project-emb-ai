"""Serve the IBM Emotion Detector exercise with Flask."""

from flask import Flask, render_template, request
from requests import RequestException

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.get("/")
def render_index():
    """Render the starter form."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion():
    """Analyze text supplied by the starter form."""
    try:
        result = emotion_detector(request.args.get("textToAnalyze", ""))
    except RequestException:
        return "Emotion analysis is temporarily unavailable. Please try again.", 503

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

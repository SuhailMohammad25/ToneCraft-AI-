from __future__ import annotations

import math
import re
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class SentimentResult:
    sentiment: str
    emotion: str
    intensity: int
    reason: str


EMOTION_KEYWORDS: dict[str, list[str]] = {
    "Anger": [
        "angry",
        "furious",
        "outraged",
        "unacceptable",
        "ridiculous",
        "terrible",
        "hate",
        "mad",
        "annoyed",
        "blame",
    ],
    "Frustration": [
        "frustrated",
        "frustrating",
        "again",
        "still",
        "nobody",
        "no one",
        "not solved",
        "doesn't work",
        "waste",
        "three times",
        "multiple times",
    ],
    "Confusion": [
        "confused",
        "unclear",
        "don't understand",
        "do not understand",
        "why",
        "how",
        "what happened",
        "explain",
        "lost",
    ],
    "Disappointment": [
        "disappointed",
        "let down",
        "expected",
        "not what",
        "poor",
        "bad experience",
        "unhappy",
        "upset",
    ],
    "Urgency": [
        "urgent",
        "today",
        "immediately",
        "asap",
        "right now",
        "deadline",
        "cannot wait",
        "need an answer",
    ],
    "Satisfaction": [
        "thanks",
        "thank you",
        "great",
        "excellent",
        "happy",
        "satisfied",
        "appreciate",
        "resolved",
        "helpful",
    ],
}

NEGATIVE_WORDS = {
    "angry",
    "furious",
    "frustrated",
    "frustrating",
    "disappointed",
    "upset",
    "unhappy",
    "bad",
    "terrible",
    "awful",
    "unacceptable",
    "issue",
    "problem",
    "refund",
    "broken",
    "failed",
    "nobody",
    "never",
    "not",
    "delay",
    "delayed",
    "wrong",
}

POSITIVE_WORDS = {
    "thanks",
    "thank",
    "great",
    "excellent",
    "happy",
    "satisfied",
    "appreciate",
    "resolved",
    "helpful",
    "love",
    "good",
}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


@lru_cache(maxsize=1)
def _get_transformers_pipeline():
    try:
        from transformers import pipeline

        return pipeline("sentiment-analysis")
    except Exception:
        return None


class SentimentService:
    def analyze(self, message: str) -> SentimentResult:
        transformer_result = self._try_transformers(message)
        fallback_result = self._rule_based(message)
        if transformer_result is None:
            return fallback_result

        sentiment, model_confidence = transformer_result
        if fallback_result.emotion != "Neutral" or fallback_result.intensity >= 45:
            return SentimentResult(
                sentiment=sentiment if fallback_result.sentiment == "Neutral" else fallback_result.sentiment,
                emotion=fallback_result.emotion,
                intensity=max(fallback_result.intensity, int(model_confidence * 100)),
                reason=fallback_result.reason,
            )
        return SentimentResult(
            sentiment=sentiment,
            emotion=fallback_result.emotion,
            intensity=max(fallback_result.intensity, int(model_confidence * 70)),
            reason=f"Transformer sentiment signal was {sentiment.lower()} with limited emotion keywords.",
        )

    def _try_transformers(self, message: str) -> tuple[str, float] | None:
        classifier = _get_transformers_pipeline()
        if classifier is None:
            return None
        try:
            raw = classifier(message[:1000])[0]
            label = str(raw.get("label", "")).lower()
            score = float(raw.get("score", 0.0))
        except Exception:
            return None

        if "neg" in label or "1 star" in label or "2 stars" in label:
            return "Negative", score
        if "pos" in label or "4 stars" in label or "5 stars" in label:
            return "Positive", score
        return "Neutral", score

    def _rule_based(self, message: str) -> SentimentResult:
        text = _normalize(message)
        words = re.findall(r"[a-z']+", text)
        positive_hits = sum(1 for word in words if word in POSITIVE_WORDS)
        negative_hits = sum(1 for word in words if word in NEGATIVE_WORDS)

        emotion_scores: dict[str, int] = {}
        matched_terms: dict[str, list[str]] = {}
        for emotion, keywords in EMOTION_KEYWORDS.items():
            hits = [keyword for keyword in keywords if keyword in text]
            if hits:
                emotion_scores[emotion] = len(hits)
                matched_terms[emotion] = hits

        if emotion_scores:
            emotion = max(emotion_scores, key=lambda key: (emotion_scores[key], key == "Frustration"))
            matches = matched_terms[emotion]
        else:
            emotion = "Neutral"
            matches = []

        sentiment_score = positive_hits - negative_hits
        if emotion in {"Anger", "Frustration", "Confusion", "Disappointment", "Urgency"}:
            sentiment_score -= 2
        elif emotion == "Satisfaction":
            sentiment_score += 2

        if sentiment_score <= -2:
            sentiment = "Negative"
        elif sentiment_score >= 2:
            sentiment = "Positive"
        else:
            sentiment = "Neutral"

        punctuation_boost = min(message.count("!"), 3) * 6
        urgency_boost = 12 if any(term in text for term in EMOTION_KEYWORDS["Urgency"]) else 0
        negative_boost = min(negative_hits, 8) * 5
        match_boost = min(sum(emotion_scores.values()), 8) * 8
        base = 20 if sentiment == "Neutral" else 38
        if sentiment == "Positive":
            base = 35
        intensity = min(100, base + punctuation_boost + urgency_boost + negative_boost + match_boost)
        if emotion == "Neutral":
            intensity = min(40, 15 + int(math.sqrt(len(words) or 1) * 3))

        if matches:
            reason = f"Detected {emotion.lower()} from language such as {', '.join(matches[:4])}."
        elif sentiment == "Positive":
            reason = "Detected positive sentiment from appreciative or satisfied wording."
        elif sentiment == "Negative":
            reason = "Detected negative sentiment from issue-focused wording and complaint language."
        else:
            reason = "No strong emotional keywords were found; the message reads mostly informational."

        return SentimentResult(sentiment=sentiment, emotion=emotion, intensity=intensity, reason=reason)

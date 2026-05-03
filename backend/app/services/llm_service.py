from __future__ import annotations

import json
from typing import Any

from app.config import get_settings
from app.prompts.response_prompt import SYSTEM_PROMPT, build_response_prompt
from app.schemas import AnalyzeRequest
from app.services.sentiment_service import SentimentResult


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate(self, request: AnalyzeRequest, sentiment: SentimentResult) -> dict[str, Any]:
        if self.settings.openai_api_key:
            llm_response = self._try_openai(request, sentiment)
            if llm_response:
                return llm_response
        return self._template_fallback(request, sentiment)

    def _try_openai(self, request: AnalyzeRequest, sentiment: SentimentResult) -> dict[str, Any] | None:
        try:
            from openai import OpenAI

            client_kwargs: dict[str, str] = {"api_key": self.settings.openai_api_key}
            if self.settings.openai_base_url:
                client_kwargs["base_url"] = self.settings.openai_base_url
            client = OpenAI(**client_kwargs)
            prompt = build_response_prompt(
                customer_message=request.customer_message,
                brand_tone=request.brand_tone,
                channel=request.channel,
                company_context=request.company_context,
                agent_notes=request.agent_notes,
                sentiment=sentiment.sentiment,
                emotion=sentiment.emotion,
                intensity=sentiment.intensity,
                emotion_reason=sentiment.reason,
            )
            response = client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.4,
            )
            content = response.choices[0].message.content or "{}"
            parsed = json.loads(content)
            if self._has_required_shape(parsed):
                return parsed
        except Exception:
            return None
        return None

    def _has_required_shape(self, payload: dict[str, Any]) -> bool:
        return all(
            key in payload
            for key in ["tone_adjustment", "main_reply", "alternatives", "agent_guidance"]
        )

    def _template_fallback(self, request: AnalyzeRequest, sentiment: SentimentResult) -> dict[str, Any]:
        greeting = self._greeting(request.channel)
        signoff = self._signoff(request.channel)
        emotion_phrase = self._emotion_phrase(sentiment.emotion)
        emotion_adjective = self._emotion_adjective(sentiment.emotion)
        context_sentence = (
            f" I will use the context we have about {request.company_context.strip()} while reviewing this."
            if request.company_context
            else ""
        )
        notes_sentence = (
            f" I also see the note that {request.agent_notes.strip()}."
            if request.agent_notes
            else ""
        )
        apology = self._apology_for(sentiment.emotion)
        tone_line = self._tone_line(request.brand_tone, sentiment.emotion)
        next_step = self._next_step(request.channel)

        main_reply = (
            f"{greeting}{apology} I understand how {emotion_adjective} this situation feels, "
            f"especially after the effort you have already put into getting it resolved.{context_sentence}"
            f"{notes_sentence} {next_step} I will keep the response focused on what we can verify and do next, "
            f"without asking you to repeat details you have already shared.{signoff}"
        )

        short_reply = (
            f"{greeting}{apology} I understand this has been {emotion_phrase} for you. "
            f"{next_step} I will focus on the next practical step and keep you updated.{signoff}"
        )

        detailed_reply = (
            f"{greeting}{apology} You have had to spend extra time on this, and I can see why that would feel "
            f"{emotion_phrase}. I am going to review the history of your message, check the current "
            f"status, and identify the next action available. If anything is missing, I will ask only for the "
            f"specific detail needed so we can move this forward efficiently.{context_sentence}{signoff}"
        )

        de_escalation = (
            f"{greeting}I hear how important this is, and I want to help reduce the back-and-forth from here. "
            f"{apology} I will look at the prior contact points, clarify the current status, and share the next "
            f"action we can take. I cannot promise an outcome before reviewing the details, but I can make sure "
            f"the issue is handled carefully and clearly.{signoff}"
        )

        return {
            "tone_adjustment": tone_line,
            "main_reply": main_reply,
            "alternatives": {
                "short": short_reply,
                "detailed": detailed_reply,
                "de_escalation": de_escalation,
            },
            "agent_guidance": {
                "do": [
                    "Acknowledge the repeated effort and the customer's current emotion.",
                    "State the next step clearly and keep the scope realistic.",
                    "Use ownership language such as 'I will review' or 'I will check'.",
                ],
                "dont": [
                    "Do not blame the customer, previous agents, or internal teams.",
                    "Do not guarantee a refund, timeline, or resolution before verification.",
                    "Do not ask the customer to repeat information already provided.",
                ],
            },
        }

    def _greeting(self, channel: str) -> str:
        if channel == "Email":
            return "Hi, "
        if channel in {"Chat", "WhatsApp"}:
            return "Thanks for reaching out. "
        return "Thanks for flagging this. "

    def _signoff(self, channel: str) -> str:
        return "\n\nKind regards,\nCustomer Support" if channel == "Email" else ""

    def _apology_for(self, emotion: str) -> str:
        if emotion in {"Anger", "Frustration", "Disappointment"}:
            return "I am sorry this has taken more effort than it should have."
        if emotion == "Confusion":
            return "I am sorry this has not been clear."
        if emotion == "Urgency":
            return "I understand this is time-sensitive."
        return "Thank you for sharing this with us."

    def _tone_line(self, brand_tone: str, emotion: str) -> str:
        recommendations = {
            "Professional": "Use calm, precise language with clear ownership and no defensiveness.",
            "Warm": "Lead with reassurance and human acknowledgement before moving into next steps.",
            "Apologetic": "Open with a sincere apology, validate the inconvenience, and explain the immediate next step.",
            "Friendly": "Keep the reply approachable, but avoid sounding casual about the customer's concern.",
            "Premium": "Use polished, attentive language that signals care and careful follow-through.",
            "Concise": "Keep the reply brief while still acknowledging the customer's emotion and next action.",
        }
        return recommendations.get(
            brand_tone,
            f"Match the {brand_tone.lower()} tone while directly acknowledging {emotion.lower()}.",
        )

    def _next_step(self, channel: str) -> str:
        if channel == "Email":
            return "I will review the case history and reply with the clearest available update and next step."
        if channel == "Chat":
            return "I am checking the details now and will share the next step in this conversation."
        if channel == "WhatsApp":
            return "I will check the details and send you a clear update here."
        return "We will review the details and respond with the next practical step."

    def _emotion_phrase(self, emotion: str) -> str:
        phrases = {
            "Anger": "so upsetting",
            "Frustration": "so frustrating",
            "Confusion": "so confusing",
            "Disappointment": "so disappointing",
            "Urgency": "so urgent",
            "Satisfaction": "reassuring",
            "Neutral": "difficult",
        }
        return phrases.get(emotion, "difficult")

    def _emotion_adjective(self, emotion: str) -> str:
        adjectives = {
            "Anger": "upsetting",
            "Frustration": "frustrating",
            "Confusion": "confusing",
            "Disappointment": "disappointing",
            "Urgency": "urgent",
            "Satisfaction": "reassuring",
            "Neutral": "difficult",
        }
        return adjectives.get(emotion, "difficult")

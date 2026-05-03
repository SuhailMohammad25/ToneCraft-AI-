from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


BrandTone = Literal["Professional", "Warm", "Apologetic", "Friendly", "Premium", "Concise"]
Channel = Literal["Email", "Chat", "WhatsApp", "Social Media"]
Sentiment = Literal["Positive", "Neutral", "Negative"]


class AnalyzeRequest(BaseModel):
    customer_message: str = Field(..., min_length=3, max_length=8000)
    brand_tone: BrandTone
    channel: Channel
    company_context: str | None = Field(default=None, max_length=3000)
    agent_notes: str | None = Field(default=None, max_length=3000)


class Alternatives(BaseModel):
    short: str
    detailed: str
    de_escalation: str


class AgentGuidance(BaseModel):
    do: list[str]
    dont: list[str]


class AnalyzeResponse(BaseModel):
    sentiment: Sentiment
    emotion: str
    intensity: int = Field(..., ge=0, le=100)
    emotion_reason: str
    tone_adjustment: str
    main_reply: str
    alternatives: Alternatives
    agent_guidance: AgentGuidance


class CaseCreate(AnalyzeRequest, AnalyzeResponse):
    pass


class CaseRead(CaseCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str
    service: str

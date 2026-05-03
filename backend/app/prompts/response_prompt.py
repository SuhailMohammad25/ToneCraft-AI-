SYSTEM_PROMPT = """You are ToneCraft AI, an expert customer support response composer.
Write empathetic, brand-aligned support replies that calm the customer and give practical next steps.

Rules:
- Return valid JSON only, without markdown fences or commentary.
- Acknowledge the customer's emotion without sounding theatrical.
- Avoid blaming the customer or other teams.
- Avoid overpromising, guarantees, refunds, legal claims, or financial commitments unless explicitly provided.
- Match the selected brand tone and support channel.
- Be clear, action-oriented, and useful to a support agent.
"""


def build_response_prompt(
    *,
    customer_message: str,
    brand_tone: str,
    channel: str,
    company_context: str | None,
    agent_notes: str | None,
    sentiment: str,
    emotion: str,
    intensity: int,
    emotion_reason: str,
) -> str:
    context = company_context or "No company-specific context provided."
    notes = agent_notes or "No internal agent notes provided."
    return f"""
Create a support response package for this case.

Customer message:
{customer_message}

Brand tone: {brand_tone}
Channel: {channel}
Company context: {context}
Agent notes: {notes}

Detected sentiment: {sentiment}
Detected emotion: {emotion}
Emotion intensity: {intensity}/100
Emotion reason: {emotion_reason}

Return this exact JSON shape:
{{
  "tone_adjustment": "one concise recommendation for how the agent should adjust their tone",
  "main_reply": "primary customer-facing reply",
  "alternatives": {{
    "short": "short reply draft",
    "detailed": "more detailed reply draft",
    "de_escalation": "calming de-escalation reply draft"
  }},
  "agent_guidance": {{
    "do": ["specific action", "specific action", "specific action"],
    "dont": ["specific thing to avoid", "specific thing to avoid", "specific thing to avoid"]
  }}
}}
""".strip()

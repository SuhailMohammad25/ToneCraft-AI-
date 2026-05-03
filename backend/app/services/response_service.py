from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.llm_service import LLMService
from app.services.sentiment_service import SentimentService


class ResponseService:
    def __init__(self) -> None:
        self.sentiment_service = SentimentService()
        self.llm_service = LLMService()

    def analyze_and_generate(self, request: AnalyzeRequest) -> AnalyzeResponse:
        sentiment = self.sentiment_service.analyze(request.customer_message)
        generated = self.llm_service.generate(request, sentiment)
        return AnalyzeResponse(
            sentiment=sentiment.sentiment,
            emotion=sentiment.emotion,
            intensity=sentiment.intensity,
            emotion_reason=sentiment.reason,
            tone_adjustment=generated["tone_adjustment"],
            main_reply=generated["main_reply"],
            alternatives=generated["alternatives"],
            agent_guidance=generated["agent_guidance"],
        )

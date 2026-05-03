from fastapi import APIRouter, HTTPException

from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.response_service import ResponseService


router = APIRouter(prefix="/api", tags=["analysis"])
response_service = ResponseService()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    try:
        return response_service.analyze_and_generate(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to analyze customer message.") from exc

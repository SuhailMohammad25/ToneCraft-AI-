import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Case
from app.schemas import CaseCreate, CaseRead


router = APIRouter(prefix="/api/cases", tags=["cases"])


def _to_schema(case: Case) -> CaseRead:
    return CaseRead(
        id=case.id,
        customer_message=case.customer_message,
        brand_tone=case.brand_tone,
        channel=case.channel,
        company_context=case.company_context,
        agent_notes=case.agent_notes,
        sentiment=case.sentiment,
        emotion=case.emotion,
        intensity=case.intensity,
        emotion_reason=case.emotion_reason,
        tone_adjustment=case.tone_adjustment,
        main_reply=case.main_reply,
        alternatives={
            "short": case.short_reply,
            "detailed": case.detailed_reply,
            "de_escalation": case.de_escalation_reply,
        },
        agent_guidance={
            "do": json.loads(case.guidance_do),
            "dont": json.loads(case.guidance_dont),
        },
        created_at=case.created_at,
    )


@router.post("", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)) -> CaseRead:
    case = Case(
        customer_message=payload.customer_message,
        brand_tone=payload.brand_tone,
        channel=payload.channel,
        company_context=payload.company_context,
        agent_notes=payload.agent_notes,
        sentiment=payload.sentiment,
        emotion=payload.emotion,
        intensity=payload.intensity,
        emotion_reason=payload.emotion_reason,
        tone_adjustment=payload.tone_adjustment,
        main_reply=payload.main_reply,
        short_reply=payload.alternatives.short,
        detailed_reply=payload.alternatives.detailed,
        de_escalation_reply=payload.alternatives.de_escalation,
        guidance_do=json.dumps(payload.agent_guidance.do),
        guidance_dont=json.dumps(payload.agent_guidance.dont),
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return _to_schema(case)


@router.get("", response_model=list[CaseRead])
def list_cases(db: Session = Depends(get_db)) -> list[CaseRead]:
    cases = db.query(Case).order_by(Case.created_at.desc()).all()
    return [_to_schema(case) for case in cases]


@router.get("/{case_id}", response_model=CaseRead)
def get_case(case_id: int, db: Session = Depends(get_db)) -> CaseRead:
    case = db.get(Case, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found.")
    return _to_schema(case)


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(case_id: int, db: Session = Depends(get_db)) -> None:
    case = db.get(Case, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found.")
    db.delete(case)
    db.commit()

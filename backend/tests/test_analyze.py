import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite://"
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


client = TestClient(app)


def setup_function() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_frustrated_refund_message() -> None:
    response = client.post(
        "/api/analyze",
        json={
            "customer_message": "I have contacted your team three times and nobody has solved my refund issue. This is extremely frustrating and I want an answer today.",
            "brand_tone": "Apologetic",
            "channel": "Email",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "Negative"
    assert data["emotion"] in {"Frustration", "Anger", "Urgency"}
    assert data["intensity"] >= 70
    assert "sorry" in data["main_reply"].lower() or "understand" in data["main_reply"].lower()
    assert set(data["alternatives"].keys()) == {"short", "detailed", "de_escalation"}


def test_case_crud() -> None:
    analyze_payload = {
        "customer_message": "I am confused about why my account was charged twice.",
        "brand_tone": "Warm",
        "channel": "Chat",
    }
    analysis = client.post("/api/analyze", json=analyze_payload).json()
    save_payload = {**analyze_payload, **analysis}

    created = client.post("/api/cases", json=save_payload)
    assert created.status_code == 201
    case_id = created.json()["id"]

    listed = client.get("/api/cases")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/api/cases/{case_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == case_id

    deleted = client.delete(f"/api/cases/{case_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/cases/{case_id}").status_code == 404

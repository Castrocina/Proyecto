import atexit
import os
import tempfile
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Configure database location before importing the application modules
_db_fd, _db_path = tempfile.mkstemp(prefix="complaints_test_", suffix=".db")
os.close(_db_fd)
os.environ.setdefault("DATABASE_URL", f"sqlite:///{_db_path}")


@atexit.register
def _cleanup_temp_db() -> None:
    if os.path.exists(_db_path):
        os.remove(_db_path)


from complaints_app.config import settings  # noqa: E402

settings.database_url = os.environ["DATABASE_URL"]

from complaints_app.database import Base, SessionLocal, engine  # noqa: E402
from complaints_app.main import app  # noqa: E402
from complaints_app import ml, models  # noqa: E402


@pytest.fixture(autouse=True)
def clean_database() -> Iterator[None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def stub_classifier(predicted_label: str, score: float = 0.87):
    class _StubPipeline:
        def __call__(self, _text: str, candidate_labels: list[str]):
            label = predicted_label if predicted_label in candidate_labels else candidate_labels[0]
            return {"labels": [label], "scores": [score]}

    return _StubPipeline()


def test_full_complaint_flow(client: TestClient, session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ml, "pipeline", lambda *args, **kwargs: stub_classifier("Mesa de Control de Inversiones", 0.91))
    ml._get_classifier.cache_clear()

    product = models.Product(name="Cuenta Digital")
    area = models.ServiceArea(
        name="Mesa de Control de Inversiones",
        email="mesa@example.com",
        channel="Inversiones",
    )
    session.add_all([product, area])
    session.commit()
    session.refresh(product)

    response = client.post(
        "/api/auth/register",
        json={"email": "cliente@example.com", "password": "superseguro"},
    )
    assert response.status_code == 201

    token_response = client.post(
        "/api/auth/token",
        data={"username": "cliente@example.com", "password": "superseguro"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert token_response.status_code == 200
    assert "access_token" in token_response.json()

    complaint_response = client.post(
        "/api/complaints/",
        json={
            "product_id": product.id,
            "description": "Mi inversión no aparece en el portal",
        },
    )
    assert complaint_response.status_code == 201

    body = complaint_response.json()
    assert body["product"]["name"] == "Cuenta Digital"
    assert body["predicted_label"] == "Mesa de Control de Inversiones"
    assert body["score"] == pytest.approx(0.91, rel=1e-3)

    list_response = client.get("/api/complaints/")
    assert list_response.status_code == 200
    complaints = list_response.json()
    assert len(complaints) == 1
    assert complaints[0]["id"] == body["id"]

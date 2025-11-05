from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    database_url: str = Field(
        default=f"sqlite:///{Path(__file__).resolve().parent / 'complaints.db'}",
        description="SQLAlchemy compatible database URL.",
    )
    secret_key: str = Field(
        default="change-me", description="Secret key used to sign JWT tokens."
    )
    access_token_expire_minutes: int = Field(default=60 * 12)
    algorithm: str = Field(default="HS256")
    hf_token: str = Field(
        default="",
        description="Hugging Face token for authenticated model downloads.",
        env="HUGGINGFACE_TOKEN",
    )
    hf_model_name: str = Field(
        default="Recognai/bert-base-spanish-wwm-cased-xnli",
        description="Model used for zero-shot classification.",
    )
    candidate_areas: List[str] = Field(
        default_factory=lambda: [
            "Seguridad Digital",
            "Créditos Hipotecarios",
            "Cartera Digitales",
            "Mesa de Control de Inversiones",
            "Facturación",
            "Operaciones Money e Pagos",
            "Operaciones y Tesorería",
            "Operaciones y Efectivo",
            "Medios de Pago y Tarjetas",
            "Compensación",
        ]
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

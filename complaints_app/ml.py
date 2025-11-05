from functools import lru_cache
from typing import Iterable, Tuple

from transformers import pipeline

from .config import settings


@lru_cache
def _get_classifier():
    classifier = pipeline(
        "zero-shot-classification",
        model=settings.hf_model_name,
        token=settings.hf_token or None,
    )
    return classifier


def predict_responsible_area(
    product_name: str,
    description: str,
    candidate_labels: Iterable[str],
) -> Tuple[str, float]:
    classifier = _get_classifier()
    text = f"Producto: {product_name}. Descripción: {description}"
    result = classifier(text, candidate_labels=list(candidate_labels))
    label = result["labels"][0]
    score = float(result["scores"][0])
    return label, score

from pydantic import BaseModel
from typing import List

class OCRResult(BaseModel):
    text: str
    confidence: float

class PageSummary(BaseModel):
    summary: str
    key_entities: List[str]
    emotions: List[str]

class ImagePrompt(BaseModel):
    prompt: str
    style: str
    mood: str

class EvaluationResult(BaseModel):
    faithfulness_score: int
    hallucination: bool

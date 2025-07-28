from typing import List
from pydantic import BaseModel, HttpUrl

class RunRequest(BaseModel):
    documents: str
    questions: List[str]

class AnswerItem(BaseModel):
    question: str
    answer: str
    sources: List[str]

class RunResponse(BaseModel):
    answers: List[AnswerItem]

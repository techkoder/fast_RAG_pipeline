from pydantic import BaseModel
from typing import List
print("🔹 schema is getting loadded")
class RunRequest(BaseModel):
    documents: str
    questions: List[str]

class RunResponse(BaseModel):
    answers: List[str]  


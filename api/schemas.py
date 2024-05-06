from pydantic import BaseModel
from typing import List

class SubmitQuestionAndDocumentsRequest(BaseModel):
    question: str
    documents: List[str]

class GetQuestionAndFactsResponse(BaseModel):
    question: str
    facts: List[str]
    status: str
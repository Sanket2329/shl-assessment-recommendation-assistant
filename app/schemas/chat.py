from typing import List, Optional

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class Recommendation(BaseModel):
    name: str
    url: str

    duration: Optional[str] = None
    remote: Optional[str] = None
    adaptive: Optional[str] = None

    retrieval_score: Optional[float] = None
    match_score: Optional[str] = None
    reason: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation] = []
    end_of_conversation: bool = False

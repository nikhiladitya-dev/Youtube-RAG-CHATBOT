from pydantic import BaseModel
from typing import List


class ProcessVideoRequest(BaseModel):
    url: str


class ProcessVideoResponse(BaseModel):
    status: str
    video_id: str
    chunks: int


class ChatRequest(BaseModel):
    question: str
    video_id: str


class SourceChunk(BaseModel):

    timestamp: str
    start_time: float
    end_time: float
    content: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]

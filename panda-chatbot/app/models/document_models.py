from pydantic import BaseModel
from typing import List
from datetime import datetime

class TranscriptSegment(BaseModel):
    #Represents one subtitle segment of a YouTube transcript
    text: str
    start: float
    duration: float

class TranscriptDocument(BaseModel):
    #Represents a complete transcript with metadata.
    
    video_id: str
    video_url: str
    language: str
    language_code: str
    is_generated: bool
    segment_count: int
    created_at: datetime
    segments: List[TranscriptSegment]

class OffsetMap(BaseModel):
    char_start: int
    char_end: int
    start_time: float
    end_time: float
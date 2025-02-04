import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class InterviewDTO:
    """DTO for interview details."""
    id: str
    title: str
    description: str
    duration: int


@dataclass
class InterviewAttemptDTO:
    """DTO for interview attempt details."""
    interview_id: str
    user_id: str
    start_datetime: datetime.datetime
    end_datetime: Optional[datetime.datetime]
    scheduled_end_datetime: Optional[datetime.datetime]

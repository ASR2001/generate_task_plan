import abc
from typing import List

from interview.interactors.storage_interface.dtos import InterviewAttemptDTO, InterviewDTO


class InterviewStorageInterface(abc.ABC):
    """Abstract interface for interview storage operations."""
    
    @abc.abstractmethod
    def get_interview_details(self, interview_ids: List[str]) -> \
            List[InterviewDTO]:
        """Retrieve interview details for a list of interview IDs."""
        pass
    
    @abc.abstractmethod
    def create_interview_attempt(
            self, interview_attempt_dto: InterviewAttemptDTO):
        """Create an interview attempt for a user."""
        pass

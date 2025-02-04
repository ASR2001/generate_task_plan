import datetime

from interview.exceptions.exceptions import InvalidInterviewIdException
from interview.interactors.storage_interface.dtos import InterviewAttemptDTO
from interview.interactors.storage_interface.storage_interface import \
    InterviewStorageInterface


class CreateInterviewAttemptInteractor:
    """Interactor for creating an interview attempt."""
    def __init__(self, storage_interface: InterviewStorageInterface):
        self.storage_interface = storage_interface
        
    def create_interview_attempt(self, interview_id: str, user_id: str):
        """Create a new interview attempt for the given user and interview."""
        self.validate_interview_details(interview_id)
        
        interview_attempt_dto = InterviewAttemptDTO(
            interview_id=interview_id,
            user_id=user_id,
            start_datetime=datetime.datetime.now(),
            end_datetime=None,
            scheduled_end_datetime=None,
        )
        
        self.storage_interface.create_interview_attempt(
            interview_attempt_dto)
    
    def validate_interview_details(self, interview_id: str):
        """Validate interview ID"""
        interview_dtos = \
            self.storage_interface.get_interview_details([interview_id])
            
        if not interview_dtos:
            raise InvalidInterviewIdException

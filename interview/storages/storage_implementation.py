from typing import List
from interview.interactors.storage_interface.dtos import InterviewDTO, \
    InterviewAttemptDTO
from interview.interactors.storage_interface.storage_interface import \
    InterviewStorageInterface
from interview.models.models import Interview, InterviewAttempt


class StorageImplementation(InterviewStorageInterface):
    """Implementation of the interview storage interface."""
    
    def get_interview_details(self, interview_ids: List[str]) -> \
            List[InterviewDTO]:
        interviews = Interview.objects.filter(id__in=interview_ids)
        
        interview_dtos = [
            InterviewDTO(
                id=str(interview.id),
                title=interview.title,
                description=interview.description,
                duration=int(interview.duration.total_seconds()),
            )
            for interview in interviews
        ]
        
        return interview_dtos

    def create_interview_attempt(
            self, interview_attempt_dto: InterviewAttemptDTO):
        interview_attempt = InterviewAttempt.objects.create(
            interview_id=interview_attempt_dto.interview_id,
            user_id=interview_attempt_dto.user_id,
            start_datetime=interview_attempt_dto.start_datetime,
            end_datetime=interview_attempt_dto.end_datetime,
        )
        
        return str(interview_attempt.id)

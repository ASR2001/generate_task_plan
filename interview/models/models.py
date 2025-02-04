import uuid
from django.db import models


class Interview(models.Model):
    """Model representing an interview."""
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField()


class InterviewConfig(models.Model):
    """Model representing an interview configuration."""
    interview = models.OneToOneField(
        Interview, on_delete=models.CASCADE, related_name="interview_config")
    is_default_access_allowed = models.BooleanField(default=False)
    should_end_interview_after_duration = models.BooleanField(default=True)
 
    
class InterviewAttempt(models.Model):
    """Model representing a user's attempt at an interview."""
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    interview = models.ForeignKey(
        Interview, on_delete=models.CASCADE, related_name="interview_attempts")
    user_id = models.CharField(max_length=36, db_index=True)
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    scheduled_end_datetime = models.DateTimeField(null=True, blank=True)
    

class UserInterviewAccess(models.Model):
    """Model representing whether a user has access to an interview."""
    interview = models.ForeignKey(
        Interview, on_delete=models.CASCADE, related_name="user_interviews")
    user_id = models.CharField(max_length=36, db_index=True)

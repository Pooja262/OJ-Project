from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Challenge

class Problem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    # Other problem-related fields

class UserProgress(models.Model):
    STATUS_CHOICES = [
        ('solved', 'Solved'),
        ('attempted', 'Attempted'),
        ('not_attempted', 'Not Attempted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_attempted')
    attempts = models.IntegerField(default=0)
    last_attempt_date = models.DateTimeField(default=timezone.now)

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracker_submissions')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)  # Now referring to the imported Challenge model
    code = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Accepted', 'Accepted'), ('Wrong Answer', 'Wrong Answer')], default='Accepted')

    def __str__(self):
        return f"Submission by {self.user} for {self.challenge.title}"
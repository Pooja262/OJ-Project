from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()  # Store the code submitted
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('correct', 'Correct'), ('incorrect', 'Incorrect')])

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.status}"

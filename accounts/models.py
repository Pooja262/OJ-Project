from django.db import models
from django.contrib.auth.models import User

class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50,choices=[('solved', 'Solved'), ('unsolved', 'Unsolved')], default='unsolved')
    created_at = models.DateTimeField(auto_now_add=True)

class Submission(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_submissions') 
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE) # Custom related_name
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    code = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Accepted', 'Accepted'), ('Wrong Answer', 'Wrong Answer')], default='Accepted')

    def __str__(self):
        return f"Submission by {self.user} for {self.challenge.title}"
    
class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.score}"

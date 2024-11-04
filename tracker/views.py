
# views.py
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProgress, Submission, Problem

@login_required
def user_dashboard(request):
    user = request.user

    # Get the user's progress data
    user_progress = UserProgress.objects.filter(user=user)

    # Total problems attempted and solved
    total_solved = user_progress.filter(status='solved').count()
    total_attempted = user_progress.filter(Q(status='solved') | Q(status='attempted')).count()
    total_problems = Problem.objects.count()

    # Fetch all submissions made by the user
    submissions = Submission.objects.filter(user=user).order_by('-submission_date')

    context = {
        'progress': user_progress,
        'total_solved': total_solved,
        'total_attempted': total_attempted,
        'total_problems': total_problems,
        'submissions': submissions,  # List of all submissions
    }
    return render(request, "user_dashboard.html", context)

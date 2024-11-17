
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Q
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from .models import Challenge, Submission,LeaderboardEntry

'''def dashboard_view(request):
    return render(request, 'dashboard.html')
'''


@login_required
def leaderboard_view(request):
    # Get the top 10 users by score, sorted in descending order
    leaderboard = LeaderboardEntry.objects.order_by('-score')[:10]
    return render(request, 'leaderboard.html', {'leaderboard': leaderboard})

@login_required
def my_challenges(request):
    user = request.user
    # Use the `submission` related name to filter challenges linked to the user
    challenges = Challenge.objects.filter(submission__user=user).distinct()
    return render(request, 'my_challenges.html', {'challenges': challenges})
def dashboard(request):
    total_submissions = Submission.objects.filter(user=request.user).count()
    problems_solved = Challenge.objects.filter(user=request.user, status='solved').count()
    rank = calculate_user_rank(request.user)  # Custom logic for calculating rank

    return render(request, 'dashboard.html', {
        'total_submissions': total_submissions,
        'problems_solved': problems_solved,
        'rank': rank,
    })
def calculate_user_rank(user):
    # Count the number of solved problems for each user
    user_solved_count = Challenge.objects.filter(user=user, status='solved').count()

    # Get all users sorted by the number of solved problems, descending
    users = User.objects.annotate(solved_count=Count('challenge', filter=Q(challenge__status='solved')))
    sorted_users = users.order_by('-solved_count')

    # Get the rank of the current user
    rank = 1
    for u in sorted_users:
        if u == user:
            break
        rank += 1

    return rank
def submissions_list(request):
    submissions = Submission.objects.filter(user=request.user)
    return render(request, 'submissions_list.html', {'submissions': submissions})

def register_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request,'User with this username already exists')
            return redirect("/register/")
        
        user = User.objects.create_user(username=username)

        user.set_password(password)

        user.save()
        
        messages.info(request,'User created successfully')
        return redirect('/login/')
    
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context,request))
    
    


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            messages.info(request, 'User with this username does not exist')
            return redirect('login')  # Use the name of the URL pattern

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, 'Invalid password')
            return redirect('login')  # Use the name of the URL pattern

        login(request, user)
        

        # Redirect to dashboard after login
        return redirect('dashboard')  # Use the name of the URL pattern

    # If the request is GET, render the login page
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'Logout successful')
    response = HttpResponseRedirect('/login/')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Prevent caching
    response['Pragma'] = 'no-cache'  # HTTP 1.0 compatibility
    response['Expires'] = '0' 
    return redirect('/login/')  # Use the name of the URL pattern


# Dashboard view

#@login_required  # This ensures only logged-in users can access the dashboard
@login_required(login_url='/login/')
def dashboard_view(request):
    template = loader.get_template('dashboard.html')
    context = {}
    return HttpResponse(template.render(context,request))
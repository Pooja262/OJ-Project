from django.urls import path, include
from accounts.views import register_user, login_user, logout_user,dashboard_view, my_challenges,submissions_list,leaderboard_view

urlpatterns = [
    path("register/", register_user, name="register-user"),
    path("login/", login_user, name="login-user"),
    path("logout/", logout_user, name="logout-user"),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_user, name='logout'),
    path('my_challenges/', my_challenges, name='my_challenges'),
    path('submissions/', submissions_list, name='submissions-list'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
]

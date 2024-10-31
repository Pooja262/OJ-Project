from django.urls import path
from . import views

urlpatterns = [
    path('challenges/', views.problem_list_view, name='problem_list'),
    path('add_problem/', views.problem_create_view, name='add_problem'),
    path('problems/<int:pk>/', views.problem_detail_view, name='problem_detail'),  # Detail page for a specific problem
    path('create/', views.problem_create_view, name='problem_create'),
    #path('problems/compile/<int:problem_id>/', views.compile_code, name='compile_code')
    path('problems/run_code/<int:pk>/', views.run_code, name='run_code'),
    path("submit/", views.submit, name="submit"),

]

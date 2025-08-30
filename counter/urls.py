
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Food management
    path('foods/', views.food_list, name='food_list'),
    path('foods/add/', views.add_food, name='add_food'),
    
    # Food logging
    path('log/', views.log_food, name='log_food'),
    path('quick-log/', views.quick_log, name='quick_log'),
    path('history/', views.entries_history, name='entries_history'),
    
    # Analytics
    path('weekly/', views.weekly_summary, name='weekly_summary'),
    
    # Settings
    path('goals/', views.goals_settings, name='goals_settings'),
    
    # API endpoints
    path('api/food-search/', views.food_search_api, name='food_search_api'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
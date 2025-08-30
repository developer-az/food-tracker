from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import json

from .models import Food, FoodEntry, NutritionalGoal
from .forms import FoodForm, FoodEntryForm, QuickFoodEntryForm, NutritionalGoalForm, CustomUserCreationForm


def home(request):
    """Home page with dashboard for logged-in users"""
    if request.user.is_authenticated:
        return dashboard(request)
    
    context = {
        'total_foods': Food.objects.count(),
        'recent_foods': Food.objects.order_by('-created_at')[:5]
    }
    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    """User dashboard showing daily summary and recent entries"""
    today = timezone.now().date()
    
    # Get today's entries
    today_entries = FoodEntry.objects.filter(
        user=request.user,
        consumed_at__date=today
    ).select_related('food')
    
    # Calculate today's totals
    today_totals = {
        'calories': sum(entry.calories_consumed() for entry in today_entries),
        'protein': sum(entry.protein_consumed() for entry in today_entries),
        'carbs': sum(entry.carbs_consumed() for entry in today_entries),
        'fat': sum(entry.fat_consumed() for entry in today_entries),
    }
    
    # Get user's goals
    goal, created = NutritionalGoal.objects.get_or_create(user=request.user)
    
    # Calculate progress percentages
    progress = {}
    if goal.daily_calories > 0:
        progress['calories'] = min(100, float(today_totals['calories'] / goal.daily_calories * 100))
    if goal.daily_protein > 0:
        progress['protein'] = min(100, float(today_totals['protein'] / goal.daily_protein * 100))
    if goal.daily_carbs > 0:
        progress['carbs'] = min(100, float(today_totals['carbs'] / goal.daily_carbs * 100))
    if goal.daily_fat > 0:
        progress['fat'] = min(100, float(today_totals['fat'] / goal.daily_fat * 100))
    
    # Group entries by meal type
    meals = {
        'breakfast': today_entries.filter(meal_type='breakfast'),
        'lunch': today_entries.filter(meal_type='lunch'),
        'dinner': today_entries.filter(meal_type='dinner'),
        'snack': today_entries.filter(meal_type='snack'),
    }
    
    # Get recent entries (last 5)
    recent_entries = FoodEntry.objects.filter(user=request.user).select_related('food')[:5]
    
    context = {
        'today_totals': today_totals,
        'goal': goal,
        'progress': progress,
        'meals': meals,
        'recent_entries': recent_entries,
        'today': today,
    }
    return render(request, 'dashboard.html', context)


@login_required
def add_food(request):
    """Add a new food item"""
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save()
            messages.success(request, f'Food "{food.name}" added successfully!')
            return redirect('food_list')
    else:
        form = FoodForm()
    
    return render(request, 'add_food.html', {'form': form})


def food_list(request):
    """List all foods with search functionality"""
    query = request.GET.get('search', '')
    foods = Food.objects.all()
    
    if query:
        foods = foods.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    foods = foods.order_by('name')
    
    context = {
        'foods': foods,
        'search_query': query,
    }
    return render(request, 'food_list.html', context)


@login_required
def log_food(request):
    """Log food consumption"""
    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, f'Logged {entry.quantity_g}g of {entry.food.name}!')
            return redirect('dashboard')
    else:
        form = FoodEntryForm()
    
    return render(request, 'log_food.html', {'form': form})


@login_required
def quick_log(request):
    """Quick food logging with search"""
    if request.method == 'POST':
        form = QuickFoodEntryForm(request.POST)
        if form.is_valid():
            food_name = form.cleaned_data['food_name']
            quantity_g = form.cleaned_data['quantity_g']
            meal_type = form.cleaned_data['meal_type']
            
            # Try to find existing food
            try:
                food = Food.objects.get(name__iexact=food_name)
            except Food.DoesNotExist:
                messages.error(request, f'Food "{food_name}" not found. Please add it first.')
                return render(request, 'quick_log.html', {'form': form})
            
            # Create entry
            FoodEntry.objects.create(
                user=request.user,
                food=food,
                quantity_g=quantity_g,
                meal_type=meal_type
            )
            
            messages.success(request, f'Logged {quantity_g}g of {food.name}!')
            return redirect('dashboard')
    else:
        form = QuickFoodEntryForm()
    
    return render(request, 'quick_log.html', {'form': form})


def food_search_api(request):
    """API endpoint for food search (used by quick log autocomplete)"""
    query = request.GET.get('q', '')
    if query:
        foods = Food.objects.filter(
            name__icontains=query
        ).values('name', 'calories_per_100g')[:10]
        return JsonResponse({'foods': list(foods)})
    return JsonResponse({'foods': []})


@login_required
def entries_history(request):
    """Show user's food entry history"""
    entries = FoodEntry.objects.filter(user=request.user).select_related('food').order_by('-consumed_at')
    
    # Pagination could be added here
    context = {
        'entries': entries[:50],  # Show last 50 entries
    }
    return render(request, 'entries_history.html', context)


@login_required
def goals_settings(request):
    """Set nutritional goals"""
    goal, created = NutritionalGoal.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = NutritionalGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goals updated successfully!')
            return redirect('dashboard')
    else:
        form = NutritionalGoalForm(instance=goal)
    
    return render(request, 'goals_settings.html', {'form': form, 'goal': goal})


@login_required
def weekly_summary(request):
    """Show weekly nutrition summary"""
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    # Get week's entries
    week_entries = FoodEntry.objects.filter(
        user=request.user,
        consumed_at__date__gte=week_start,
        consumed_at__date__lte=week_end
    ).select_related('food')
    
    # Group by day
    daily_data = {}
    for i in range(7):
        date = week_start + timedelta(days=i)
        day_entries = [e for e in week_entries if e.consumed_at.date() == date]
        
        daily_data[date.strftime('%A')] = {
            'date': date,
            'calories': sum(e.calories_consumed() for e in day_entries),
            'protein': sum(e.protein_consumed() for e in day_entries),
            'carbs': sum(e.carbs_consumed() for e in day_entries),
            'fat': sum(e.fat_consumed() for e in day_entries),
            'entries_count': len(day_entries),
        }
    
    # Weekly totals
    week_totals = {
        'calories': sum(data['calories'] for data in daily_data.values()),
        'protein': sum(data['protein'] for data in daily_data.values()),
        'carbs': sum(data['carbs'] for data in daily_data.values()),
        'fat': sum(data['fat'] for data in daily_data.values()),
    }
    
    # Get user's goals for comparison
    goal = NutritionalGoal.objects.filter(user=request.user).first()
    
    context = {
        'daily_data': daily_data,
        'week_totals': week_totals,
        'week_start': week_start,
        'week_end': week_end,
        'goal': goal,
    }
    return render(request, 'weekly_summary.html', context)


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create default nutritional goal
            NutritionalGoal.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
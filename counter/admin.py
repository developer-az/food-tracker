from django.contrib import admin
from .models import Food, FoodEntry, NutritionalGoal


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories_per_100g', 'protein_per_100g', 'carbs_per_100g', 'fat_per_100g', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(FoodEntry)
class FoodEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'quantity_g', 'meal_type', 'consumed_at', 'calories_consumed')
    list_filter = ('meal_type', 'consumed_at', 'food')
    search_fields = ('user__username', 'food__name')
    date_hierarchy = 'consumed_at'
    ordering = ('-consumed_at',)


@admin.register(NutritionalGoal)
class NutritionalGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'daily_calories', 'daily_protein', 'daily_carbs', 'daily_fat', 'updated_at')
    search_fields = ('user__username',)
    ordering = ('user__username',)

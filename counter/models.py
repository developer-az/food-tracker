from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class Food(models.Model):
    """Model representing a food item with nutritional information"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, help_text="Brief description of the food item")
    
    # Nutritional information per 100g
    calories_per_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    protein_per_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Protein in grams")
    carbs_per_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Carbohydrates in grams")
    fat_per_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Fat in grams")
    fiber_per_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Fiber in grams")
    
    # Common serving size
    serving_size_g = models.DecimalField(max_digits=6, decimal_places=1, default=100, help_text="Common serving size in grams")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def calories_per_serving(self):
        """Calculate calories for the common serving size"""
        return (self.calories_per_100g * self.serving_size_g / 100).quantize(Decimal('0.1'))
    
    def protein_per_serving(self):
        """Calculate protein for the common serving size"""
        return (self.protein_per_100g * self.serving_size_g / 100).quantize(Decimal('0.1'))


class FoodEntry(models.Model):
    """Model representing a user's food consumption entry"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_entries')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='entries')
    
    # Consumption details
    quantity_g = models.DecimalField(max_digits=6, decimal_places=1, help_text="Quantity consumed in grams")
    meal_type = models.CharField(max_length=20, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ], default='breakfast')
    
    # Timestamps
    consumed_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-consumed_at']
        verbose_name_plural = "Food entries"
    
    def __str__(self):
        return f"{self.user.username} - {self.food.name} ({self.quantity_g}g)"
    
    def calories_consumed(self):
        """Calculate calories consumed for this entry"""
        return (self.food.calories_per_100g * self.quantity_g / 100).quantize(Decimal('0.1'))
    
    def protein_consumed(self):
        """Calculate protein consumed for this entry"""
        return (self.food.protein_per_100g * self.quantity_g / 100).quantize(Decimal('0.1'))
    
    def carbs_consumed(self):
        """Calculate carbohydrates consumed for this entry"""
        return (self.food.carbs_per_100g * self.quantity_g / 100).quantize(Decimal('0.1'))
    
    def fat_consumed(self):
        """Calculate fat consumed for this entry"""
        return (self.food.fat_per_100g * self.quantity_g / 100).quantize(Decimal('0.1'))


class NutritionalGoal(models.Model):
    """Model representing a user's nutritional goals"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nutritional_goal')
    
    # Daily goals
    daily_calories = models.DecimalField(max_digits=6, decimal_places=0, default=2000, help_text="Daily calorie target")
    daily_protein = models.DecimalField(max_digits=6, decimal_places=1, default=150, help_text="Daily protein target in grams")
    daily_carbs = models.DecimalField(max_digits=6, decimal_places=1, default=250, help_text="Daily carbohydrates target in grams")
    daily_fat = models.DecimalField(max_digits=6, decimal_places=1, default=70, help_text="Daily fat target in grams")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Goals"

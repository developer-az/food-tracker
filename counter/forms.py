from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Food, FoodEntry, NutritionalGoal


class FoodForm(forms.ModelForm):
    """Form for adding/editing food items"""
    class Meta:
        model = Food
        fields = ['name', 'description', 'calories_per_100g', 'protein_per_100g', 
                 'carbs_per_100g', 'fat_per_100g', 'fiber_per_100g', 'serving_size_g']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Banana'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description...'}),
            'calories_per_100g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'protein_per_100g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'carbs_per_100g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'fat_per_100g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'fiber_per_100g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'serving_size_g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '1'}),
        }


class FoodEntryForm(forms.ModelForm):
    """Form for logging food consumption"""
    class Meta:
        model = FoodEntry
        fields = ['food', 'quantity_g', 'meal_type', 'consumed_at']
        widgets = {
            'food': forms.Select(attrs={'class': 'form-control'}),
            'quantity_g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0.1', 'placeholder': 'grams'}),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'consumed_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['food'].queryset = Food.objects.all().order_by('name')
        # Set default time to now
        if not self.initial.get('consumed_at'):
            from django.utils import timezone
            self.initial['consumed_at'] = timezone.now().strftime('%Y-%m-%dT%H:%M')


class QuickFoodEntryForm(forms.Form):
    """Simplified form for quick food logging"""
    food_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Start typing food name...',
            'autocomplete': 'off'
        })
    )
    quantity_g = forms.DecimalField(
        max_digits=6, 
        decimal_places=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'step': '0.1', 
            'min': '0.1', 
            'placeholder': 'Quantity in grams'
        })
    )
    meal_type = forms.ChoiceField(
        choices=FoodEntry._meta.get_field('meal_type').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class NutritionalGoalForm(forms.ModelForm):
    """Form for setting nutritional goals"""
    class Meta:
        model = NutritionalGoal
        fields = ['daily_calories', 'daily_protein', 'daily_carbs', 'daily_fat']
        widgets = {
            'daily_calories': forms.NumberInput(attrs={'class': 'form-control', 'min': '500', 'max': '5000'}),
            'daily_protein': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'daily_carbs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'daily_fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
        }


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
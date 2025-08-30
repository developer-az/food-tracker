from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from counter.models import Food, FoodEntry, NutritionalGoal
from decimal import Decimal


class FoodTrackerTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.food = Food.objects.create(
            name='Test Apple',
            description='Test apple for testing',
            calories_per_100g=Decimal('52'),
            protein_per_100g=Decimal('0.3'),
            carbs_per_100g=Decimal('13.8'),
            fat_per_100g=Decimal('0.2'),
            serving_size_g=Decimal('182')
        )

    def test_home_page_loads(self):
        """Test that home page loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Food Tracker')

    def test_food_list_loads(self):
        """Test that food list page loads and shows foods"""
        response = self.client.get(reverse('food_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Apple')

    def test_food_search_functionality(self):
        """Test food search works"""
        response = self.client.get(reverse('food_list'), {'search': 'apple'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Apple')

    def test_food_calorie_calculation(self):
        """Test food calorie calculation methods"""
        serving_calories = self.food.calories_per_serving()
        expected_calories = (Decimal('52') * Decimal('182') / 100).quantize(Decimal('0.1'))
        self.assertEqual(serving_calories, expected_calories)

    def test_food_entry_creation(self):
        """Test food entry logging"""
        self.client.login(username='testuser', password='testpass123')
        entry = FoodEntry.objects.create(
            user=self.user,
            food=self.food,
            quantity_g=Decimal('100'),
            meal_type='breakfast'
        )
        self.assertEqual(entry.calories_consumed(), Decimal('52.0'))
        self.assertEqual(entry.protein_consumed(), Decimal('0.3'))

    def test_nutritional_goal_creation(self):
        """Test nutritional goal model"""
        goal = NutritionalGoal.objects.create(
            user=self.user,
            daily_calories=Decimal('2000'),
            daily_protein=Decimal('150'),
            daily_carbs=Decimal('250'),
            daily_fat=Decimal('70')
        )
        self.assertEqual(goal.daily_calories, Decimal('2000'))
        self.assertEqual(str(goal), f"{self.user.username}'s Goals")

    def test_food_api_search(self):
        """Test food search API endpoint"""
        response = self.client.get(reverse('food_search_api'), {'q': 'apple'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('foods', data)
        self.assertEqual(len(data['foods']), 1)
        self.assertEqual(data['foods'][0]['name'], 'Test Apple')

    def test_sample_foods_loaded(self):
        """Test that sample foods can be loaded"""
        from django.core.management import call_command
        call_command('load_sample_foods')
        
        # Check that sample foods exist
        banana = Food.objects.filter(name='Banana').first()
        self.assertIsNotNone(banana)
        self.assertEqual(banana.calories_per_100g, Decimal('89'))

    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication"""
        response = self.client.get(reverse('dashboard'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_add_food_requires_login(self):
        """Test that add food requires authentication"""
        response = self.client.get(reverse('add_food'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
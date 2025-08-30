from django.core.management.base import BaseCommand
from counter.models import Food
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load sample foods into the database'

    def handle(self, *args, **options):
        sample_foods = [
            {
                'name': 'Banana',
                'description': 'Fresh banana, medium size',
                'calories_per_100g': Decimal('89'),
                'protein_per_100g': Decimal('1.1'),
                'carbs_per_100g': Decimal('22.8'),
                'fat_per_100g': Decimal('0.3'),
                'fiber_per_100g': Decimal('2.6'),
                'serving_size_g': Decimal('118'),
            },
            {
                'name': 'Chicken Breast',
                'description': 'Cooked, skinless chicken breast',
                'calories_per_100g': Decimal('231'),
                'protein_per_100g': Decimal('43.5'),
                'carbs_per_100g': Decimal('0'),
                'fat_per_100g': Decimal('5.0'),
                'fiber_per_100g': Decimal('0'),
                'serving_size_g': Decimal('100'),
            },
            {
                'name': 'Brown Rice',
                'description': 'Cooked brown rice',
                'calories_per_100g': Decimal('112'),
                'protein_per_100g': Decimal('2.6'),
                'carbs_per_100g': Decimal('23'),
                'fat_per_100g': Decimal('0.9'),
                'fiber_per_100g': Decimal('1.8'),
                'serving_size_g': Decimal('150'),
            },
            {
                'name': 'Apple',
                'description': 'Fresh apple with skin',
                'calories_per_100g': Decimal('52'),
                'protein_per_100g': Decimal('0.3'),
                'carbs_per_100g': Decimal('13.8'),
                'fat_per_100g': Decimal('0.2'),
                'fiber_per_100g': Decimal('2.4'),
                'serving_size_g': Decimal('182'),
            },
            {
                'name': 'Broccoli',
                'description': 'Raw broccoli florets',
                'calories_per_100g': Decimal('34'),
                'protein_per_100g': Decimal('2.8'),
                'carbs_per_100g': Decimal('7'),
                'fat_per_100g': Decimal('0.4'),
                'fiber_per_100g': Decimal('2.6'),
                'serving_size_g': Decimal('100'),
            },
            {
                'name': 'Salmon',
                'description': 'Atlantic salmon, cooked',
                'calories_per_100g': Decimal('231'),
                'protein_per_100g': Decimal('25.4'),
                'carbs_per_100g': Decimal('0'),
                'fat_per_100g': Decimal('13.4'),
                'fiber_per_100g': Decimal('0'),
                'serving_size_g': Decimal('100'),
            },
            {
                'name': 'Oats',
                'description': 'Rolled oats, dry',
                'calories_per_100g': Decimal('389'),
                'protein_per_100g': Decimal('16.9'),
                'carbs_per_100g': Decimal('66.3'),
                'fat_per_100g': Decimal('6.9'),
                'fiber_per_100g': Decimal('10.6'),
                'serving_size_g': Decimal('40'),
            },
            {
                'name': 'Greek Yogurt',
                'description': 'Plain, non-fat Greek yogurt',
                'calories_per_100g': Decimal('59'),
                'protein_per_100g': Decimal('10.3'),
                'carbs_per_100g': Decimal('3.6'),
                'fat_per_100g': Decimal('0.4'),
                'fiber_per_100g': Decimal('0'),
                'serving_size_g': Decimal('170'),
            },
            {
                'name': 'Avocado',
                'description': 'Raw avocado',
                'calories_per_100g': Decimal('160'),
                'protein_per_100g': Decimal('2'),
                'carbs_per_100g': Decimal('8.5'),
                'fat_per_100g': Decimal('14.7'),
                'fiber_per_100g': Decimal('6.7'),
                'serving_size_g': Decimal('150'),
            },
            {
                'name': 'Sweet Potato',
                'description': 'Baked sweet potato with skin',
                'calories_per_100g': Decimal('90'),
                'protein_per_100g': Decimal('2'),
                'carbs_per_100g': Decimal('20.7'),
                'fat_per_100g': Decimal('0.2'),
                'fiber_per_100g': Decimal('3.3'),
                'serving_size_g': Decimal('130'),
            },
            {
                'name': 'Almonds',
                'description': 'Raw almonds',
                'calories_per_100g': Decimal('579'),
                'protein_per_100g': Decimal('21.2'),
                'carbs_per_100g': Decimal('21.6'),
                'fat_per_100g': Decimal('49.9'),
                'fiber_per_100g': Decimal('12.5'),
                'serving_size_g': Decimal('28'),
            },
            {
                'name': 'Quinoa',
                'description': 'Cooked quinoa',
                'calories_per_100g': Decimal('120'),
                'protein_per_100g': Decimal('4.4'),
                'carbs_per_100g': Decimal('21.3'),
                'fat_per_100g': Decimal('1.9'),
                'fiber_per_100g': Decimal('2.8'),
                'serving_size_g': Decimal('150'),
            },
        ]

        created_count = 0
        for food_data in sample_foods:
            food, created = Food.objects.get_or_create(
                name=food_data['name'],
                defaults=food_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created: {food.name}')
            else:
                self.stdout.write(f'Already exists: {food.name}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {created_count} new foods into the database!')
        )
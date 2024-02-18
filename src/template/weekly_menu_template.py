import random


class MealPlanner:
    def __init__(self, meat_meals=0, fish_meals=0, free_day=None):
        self.days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.categories = ['vegetariano', 'vegano', 'carne', 'pesce']
        self.meat_meals = meat_meals
        self.fish_meals = fish_meals
        self.free_day = free_day  # Accepts a specific day as a string, e.g., 'Monday'
        self.meal_times = ['Lunch', 'Dinner']

    def generate_plan(self):
        plan = []
        meat_assigned = []
        fish_assigned = []

        # Assign free day if specified
        if self.free_day and self.free_day in self.days_of_week:
            for meal_time in self.meal_times:
                plan.append({'day': self.free_day, 'moment_of_day': meal_time, 'category': 'Free'})

        # Assign meat and fish meals
        for _ in range(self.meat_meals + self.fish_meals):
            category = 'carne' if len(meat_assigned) < self.meat_meals else 'pesce'
            day, meal_time = self._get_random_day_time(meat_assigned if category == 'carne' else fish_assigned)
            plan.append({'day': day, 'moment_of_day': meal_time, 'category': category})
            if category == 'carne':
                meat_assigned.append(day)
            else:
                fish_assigned.append(day)

        # Fill remaining meals with vegetarian or vegan
        for day in self.days_of_week:
            for meal_time in self.meal_times:
                if not any(meal['day'] == day and meal['moment_of_day'] == meal_time for meal in plan):
                    category = random.choice(['vegetariano', 'vegano'])
                    plan.append({'day': day, 'moment_of_day': meal_time, 'category': category})

        return plan

    def _get_random_day_time(self, assigned_days):
        available_days = set(self.days_of_week) - set(assigned_days) - {self.free_day}
        day = random.choice(list(available_days))
        meal_time = random.choice(self.meal_times)
        return day, meal_time


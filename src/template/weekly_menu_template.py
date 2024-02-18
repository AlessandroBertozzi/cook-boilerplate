import random


class WeeklyMenuTemplate:
    def __init__(self):
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.meal_times = ['Lunch', 'Dinner']
        self.categories = ['Vegetarian', 'Vegan']
        self.weekly_menu = {}

    def is_valid_distribution(self, selected_days):
        for i in range(len(selected_days)):
            if i > 0:
                prev_day_index = self.days.index(selected_days[i - 1])
                current_day_index = self.days.index(selected_days[i])
                if abs(prev_day_index - current_day_index) == 1:
                    return False
        return True

    def select_days(self, count, exclude_days=[]):
        valid = False
        selected_days = []
        while not valid:
            selected_days = random.sample([day for day in self.days if day not in exclude_days], count)
            valid = self.is_valid_distribution(selected_days)
        return selected_days

    def generate(self):
        meat_days = self.select_days(2)
        fish_days = self.select_days(3, exclude_days=meat_days)

        for day in self.days:
            self.weekly_menu[day] = {}
            for meal_time in self.meal_times:
                if day in meat_days:
                    self.weekly_menu[day][meal_time] = 'Meat'
                    meat_days.remove(day)  # Ensure meat is served only once that day
                elif day in fish_days:
                    self.weekly_menu[day][meal_time] = 'Fish'
                    fish_days.remove(day)  # Ensure fish is served only once that day
                else:
                    self.weekly_menu[day][meal_time] = random.choice(self.categories)

    def print_menu(self):
        for day, meals in self.weekly_menu.items():
            print(f"{day}:")
            for meal_time, category in meals.items():
                print(f"  {meal_time}: {category}")
            print()

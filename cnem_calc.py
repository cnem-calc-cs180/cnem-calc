import csv
import sys
import os

class CNEM_Calc:
    FIELD_INDEX = {
        "cost": -1,
        "protein": -1,
        "fats": -1,
        "carbohydrates": -1,
        "calories": -1
    } # should tell u in which column these fields can be found sa recipes db
    # please update when possible :)

    def init(self):
        self.prices = []
        self.recipes = []
        self.nutrition_constraints = {} # {nutrition(str) : [target (int), min tolerance (0-1, float), max tolerance (0-inf, float)]}
        self.max_constraint_funcs = [self.cost_bound, self.max_nutrition_limit]
        self.min_constraint_funcs = []
        self.constraint_tolerance = -1

        self.nutrients = ["protein", "fats", "carbohydrates", "calories"]
        self.n_meals = 3    # number of meals in a mealset
        self.n_mealsets = 5 # number of mealsets suggested

    def get_meal_value(self, meal, param):
        return meal[self.FIELD_INDEX[param]]

    def get_mealset_value(self, mealset, param):
        value = 0
        for meal in mealset:
            value += meal[self.FIELD_INDEX[param]]
        return value

    def within_max_constraints(self, current_meals, valid_mealsets):
        for constraint_func in self.max_constraint_funcs:
            if not constraint_func(current_meals, valid_mealsets):
                return False
        return True

    def cost_bound(self, current_meals, valid_mealsets):
        n_mealsets = self.n_mealsets
        if len(valid_mealsets) < n_mealsets:
            return True
        return self.get_mealset_value(current_meals, "cost") <= self.get_mealset_value(valid_mealsets[n_mealsets - 1])

    def max_nutrition_limit(self, current_meals, valid_mealsets):
        nutrition_constraints = self.nutrition_constraints
        for nutrient in self.nutrients:
            target = nutrition_constraints[nutrient][0]
            max_tolerance = nutrition_constraints[nutrient][2]
            limit = target * (1 + max_tolerance)
            if self.get_mealset_value(current_meals, nutrient) > limit:
                return False
        return True

    def within_min_constraints(self, current_meals, valid_mealsets):
        for constraint_func in self.min_constraint_funcs:
            if not constraint_func(current_meals, valid_mealsets):
                return False
        return True

    def min_nutrition_requirement(self, current_meals, valid_mealsets):
        nutrition_constraints = self.nutrition_constraints
        for nutrient in self.nutrients:
            target = nutrition_constraints[nutrient][0]
            min_tolerance = nutrition_constraints[nutrient][1]
            limit = target * (1 - min_tolerance)
            if self.get_mealset_value(current_meals, nutrient) < limit:
                return False
        return True

    def recursive_backtrack(self, current_meals = [], valid_mealsets = []):
        n_recipes = len(self.recipes)
        n_meals = self.n_meals
        n_mealsets = self.n_mealsets

        if not self.within_max_constraints(current_meals, valid_mealsets):
            return valid_mealsets

        if len(current_meals) >= n_meals:
            if not self.within_min_constraints(current_meals, valid_mealsets):
                return valid_mealsets
            valid_mealsets.append(current_meals)
            valid_mealsets.sort(key=self.mealset_cost)
            too_expensive = [] if len(valid_mealsets) <= n_mealsets else valid_mealsets[n_mealsets:]
            valid_mealsets = valid_mealsets if len(valid_mealsets) <= n_mealsets else valid_mealsets[:n_mealsets]
            return valid_mealsets
        
        previous_index = current_meals[-1] if len(current_meals) > 0 else 0
        for n in range(previous_index + 1, n_meals):
            next_meal_index = n
            valid_mealsets = self.backtrack(current_meals + [n], valid_mealsets)
        
        return valid_mealsets

if __name__ == "__main__":
    # DEFAULTS
    recipes_filename = "recipes.db"
    prices_filename = "prices.db"

    args = sys.argv

    # PARSE TERMINAL ARGS
    # # # # #

    meal_calc = CNEM_Calc()




# how do you expect to run this?
# > py cnem_calc.py
# >>> this should be able to run defaults
# >>> external parameters: price, recipes, constraints
# >>>>>> madali lang defaults ng recipes at constraints, pero price hmm
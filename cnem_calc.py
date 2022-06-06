import csv

class CNEM_Calc:

    def init(self):
        self.prices = []
        self.recipes = []
        self.max_constraint_funcs = []
        self.min_constraint_funcs = []
        self.constraint_tolerance = -1

        self.n_meals = 3    # number of meals in a mealset
        self.n_mealsets = 5 # number of mealsets suggested

    def within_max_constraints(self, current_state, valid_states):
        return True

    def within_min_constraints(self, current_state, valid_states):
        return True

    def mealset_cost(self, mealset):
        cost = 0
        for meal in mealset:
            cost += 0 # meal cost
        return cost

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

if __name__ == "__main__":
    pass
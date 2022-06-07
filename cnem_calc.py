import csv
import sys
import os

class CNEM_Calc:
    FIELD_INDEX = {
        "cost": -1,
        "protein": -1,
        "fat": -1,
        "carbohydrates": -1,
        "energy": -1
    } # should tell u in which column these fields can be found sa recipes db
    # please update when possible :)

    def __init__(self, recipes_h, recipes, prices, nutrition):
        self.prices = prices
        self.recipes = recipes
        self.nutrition_constraints = {constraint[0]:[float(v) for v in constraint[1:]] for constraint in nutrition} # {nutrition(str) : [target (int), min tolerance (0-1, float), max tolerance (0-inf, float)]}
        self.max_constraint_funcs = [self.cost_bound, self.max_nutrition_limit]
        self.max_constraint_funcs_no_bounds = [self.max_nutrition_limit]
        self.min_constraint_funcs = [self.min_nutrition_requirement]

        self.nutrients = ["protein", "fat", "carbohydrates", "energy"]
        self.parameters = self.nutrients + ["cost"]
        self.n_meals = 3    # number of meals in a mealset
        self.n_mealsets = 5 # number of mealsets suggested
        self.recursion_calls = 0

        #cost calculation
        for index, recipe in enumerate(self.recipes):
            cost = 0
            serving_scale = float(recipes[index][recipes_h.index('servings/head')]) / float(recipes[index][recipes_h.index('serving size')])
            for ingredient in self.prices:
                if not recipes[index][recipes_h.index(ingredient[0])]: continue
                cost += float(recipes[index][recipes_h.index(ingredient[0])]) * float(ingredient[1]) # if preprocessed, can remove float typecast
            for nutrient in self.nutrients:
                recipes[index][recipes_h.index(nutrient)] = str(float(recipes[index][recipes_h.index(nutrient)]) * serving_scale)
            cost *= serving_scale
            self.recipes[index] += [cost]
        recipes_h += ["cost"]

        #field index set
        for field in self.FIELD_INDEX.keys():
            self.FIELD_INDEX[field] = recipes_h.index(field)
            
        #self.FIELD_INDEX["meal"] = 1
        #add ingredients to field index
        #start = recipes_h.index("Rice (kg)")
        #for i in range(start,len(recipes_h)-1):
        #    self.FIELD_INDEX[recipes_h[i]] = i
        #    pass
            
    def get_meal_value(self, meal_index, param):
        output = self.recipes[meal_index][self.FIELD_INDEX[param]]
        try:
            output = float(output)
        except:
            output = 0
        return output

    def get_mealset_value(self, mealset, param):
        value = 0
        for meal in mealset:
            value += self.get_meal_value(meal, param)
        return value

    def get_mealset_cost(self, mealset):
        return self.get_mealset_value(mealset, "cost")

    def get_mealset_ingredients(self, mealset):
        total = []
        start = recipes_h.index("Rice (kg)")
        for i in range(start,len(recipes_h)-1):
            ingredient = recipes_h[i]
            amount = 0
            for m in mealset:
                amount += float(self.recipes[m][i])
            if amount > 0:
                total.append([ingredient,round(amount,3)])
        return total

    def within_max_constraints(self, current_meals, param_values, valid_mealsets):
        for constraint_func in self.max_constraint_funcs:
            if not constraint_func(current_meals, param_values, valid_mealsets):
                return False
        return True

    def within_max_constraints_no_bounds(self, current_meals, param_values, valid_mealsets):
        for constraint_func in self.max_constraint_funcs_no_bounds:
            if not constraint_func(current_meals, param_values, valid_mealsets):
                return False
        return True

    def cost_bound(self, current_meals, param_values, valid_mealsets):
        n_mealsets = self.n_mealsets
        if len(valid_mealsets) < n_mealsets:
            return True
        return param_values["cost"] <= self.get_mealset_value(valid_mealsets[n_mealsets - 1], "cost")

    def max_nutrition_limit(self, current_meals, param_values, valid_mealsets):
        nutrition_constraints = self.nutrition_constraints
        for nutrient in nutrition_constraints.keys():
            target = nutrition_constraints[nutrient][0]
            max_tolerance = nutrition_constraints[nutrient][2]
            if max_tolerance < 0: continue
            limit = target * (1 + max_tolerance)
            if param_values[nutrient] > limit:
                # print("Rip ", current_meals, " ", nutrient, " - ", param_values[nutrient])
                return False
        return True

    def within_min_constraints(self, current_meals, param_values, valid_mealsets):
        for constraint_func in self.min_constraint_funcs:
            if not constraint_func(current_meals, param_values, valid_mealsets):
                return False
        return True

    def min_nutrition_requirement(self, current_meals, param_values, valid_mealsets):
        nutrition_constraints = self.nutrition_constraints
        for nutrient in self.nutrition_constraints:
            target = nutrition_constraints[nutrient][0]
            min_tolerance = nutrition_constraints[nutrient][1]
            if min_tolerance < 0: continue
            limit = target * (1 - min_tolerance)
            if param_values[nutrient] < limit:
                #print("Min Rip ", current_meals, " ", nutrient, " - ", param_values[nutrient])
                return False
        return True

    def recursive_backtrack(self, current_meals = [], valid_mealsets = [], param_values = {}):
        self.recursion_calls += 1
        n_recipes = len(self.recipes)
        n_meals = self.n_meals
        n_mealsets = self.n_mealsets
        parameters = self.parameters
        param_values = {parameter : 0 for parameter in parameters} if param_values == {} else param_values

        if len(current_meals) >= n_meals:
            if not self.within_min_constraints(current_meals, param_values, valid_mealsets):
                return valid_mealsets
            valid_mealsets.append(current_meals)
            valid_mealsets.sort(key=self.get_mealset_cost)
            too_expensive = [] if len(valid_mealsets) <= n_mealsets else valid_mealsets[n_mealsets:]
            valid_mealsets = valid_mealsets if len(valid_mealsets) <= n_mealsets else valid_mealsets[:n_mealsets]
            return valid_mealsets
        
        previous_index = current_meals[-1] if len(current_meals) > 0 else -1
        for n in range(previous_index+1, n_recipes):
            # print(current_meals, "+", n)
            next_meal_index = n
            next_meals = current_meals + [next_meal_index]
            next_param_values = { \
                parameter : param_values[parameter] + self.get_meal_value(n, parameter) \
                for parameter in parameters}
            if not self.within_max_constraints(next_meals, next_param_values, valid_mealsets):
                # print("OOF")
                continue
            valid_mealsets = self.recursive_backtrack(next_meals, valid_mealsets, next_param_values)
        
        return valid_mealsets

    def recursive_backtrack_no_bounds(self, current_meals = [], valid_mealsets = [], param_values = {}):
        self.recursion_calls += 1
        # Branch and Bounds is removing expensive meals
        n_recipes = len(self.recipes)
        n_meals = self.n_meals
        n_mealsets = self.n_mealsets
        parameters = self.parameters
        param_values = {parameter : 0 for parameter in parameters} if param_values == {} else param_values

        if len(current_meals) >= n_meals:
            if not self.within_min_constraints(current_meals, param_values, valid_mealsets):
                return valid_mealsets
            valid_mealsets.append(current_meals)
            valid_mealsets.sort(key=self.get_mealset_cost)
            too_expensive = [] if len(valid_mealsets) <= n_mealsets else valid_mealsets[n_mealsets:]
            valid_mealsets = valid_mealsets if len(valid_mealsets) <= n_mealsets else valid_mealsets[:n_mealsets]
            return valid_mealsets
        
        previous_index = current_meals[-1] if len(current_meals) > 0 else -1
        for n in range(previous_index+1, n_recipes):
            # print(current_meals, "+", n)
            next_meal_index = n
            next_meals = current_meals + [next_meal_index]
            next_param_values = { \
                parameter : param_values[parameter] + self.get_meal_value(n, parameter) \
                for parameter in parameters}
            if not self.within_max_constraints_no_bounds(next_meals, next_param_values, valid_mealsets):
                # print("OOF")
                continue
            valid_mealsets = self.recursive_backtrack(next_meals, valid_mealsets, next_param_values)
        
        return valid_mealsets
#END OF CNEM_CALC
  
def print_suggestion(mc, s, mealset):
    print("--------------------------------------------------")
    print("Suggestion " + str(s) + " - P" + str(round(mc.get_mealset_cost(mealset),2)) + ":")
    for meal in mealset:
        print(" - " + mc.recipes[meal][1])
    print()

def print_suggestion_ingredients(mc, mealset):
    ingredients = mc.get_mealset_ingredients(mealset)
    print("Total Ingredients:")
    for i,a in ingredients:
        print(i + ": " + str(a))
    print()


if __name__ == "__main__":
    print()
    # DEFAULTS
    recipes_filename = "recipes.csv"
    prices_filename = "prices.csv"
    nutrition_filename = "nutrition.csv"
    args = sys.argv

    # PARSE TERMINAL ARGS
    # # # # #
    if "-M" in args:
        print("You have entered Manual Input Mode (-M)")
        print("Please enter the filepath for the following files")
        print("(Enter nothing to use default value)")
        print("--------------------------------------")

        # Recipes
        buf = input("Recipe database: ").strip()
        if buf != "":
            recipes_filename = buf
        buf = input("Ingredient pricelist: ").strip()
        if buf != "":
            prices_filename = buf
        buf = input("Constraint list: ").strip()
        if buf != "":
            nutrition_filename = buf
    else:
        if "-r" in args:
            recipes_filename = args[args.index("-r")+1].replace('"', '').replace("'", "")
        if "-p" in args:
            prices_filename = args[args.index("-p")+1].replace('"', '').replace("'", "")
        if "-c" in args:
            nutrition_filename = args[args.index("-c")+1].replace('"', '').replace("'", "")
    
    recipes = []
    recipes_h  = []
    prices = []
    nutrition = []

    with open(recipes_filename, 'r') as recipes_db:
        recipes = list(csv.reader(recipes_db))
        recipes_h = recipes.pop(0) # recipes header

    with open(prices_filename, 'r') as prices_db:
        prices = list(csv.reader(prices_db))

    with open(nutrition_filename, 'r') as nutrition_db:
        nutrition = list(csv.reader(nutrition_db))

    meal_calc = CNEM_Calc(recipes_h, recipes, prices, nutrition)
    
    if "--nm" in args:
        meal_calc.n_meals = int(args[args.index("--nm")+1].replace('"', '').replace("'", ""))
    if "--ns" in args:
        meal_calc.n_mealsets = int(args[args.index("--ns")+1].replace('"', '').replace("'", ""))

    output = meal_calc.recursive_backtrack()
    print(output)
    
    buf = ""
    
    print("==================================================")
    print("Top 5 Suggestions\n")
    for i in range(5):
        if i == len(output):
            break
        print_suggestion(meal_calc, i+1, output[i])

    while True:
        buf = input("Enter suggestion number: ")
        if buf in ["-1", "exit"]:
                break
        if buf.lower() == "top":
            print("==================================================")
            print("Top 5 Suggestions")
            for i in range(5):
                if i == len(output):
                    break
                print_suggestion(meal_calc, i+1, output[i])
        try:
            buf = int(buf)
            if buf > len(output):
                print("Try a smaller number")
                continue
        except:
            print("Please enter a valid number")
            continue
        
        print_suggestion(meal_calc, buf, output[buf-1])
        print_suggestion_ingredients(meal_calc, output[buf-1])

        print("To show Top 5 Suggestions again, type 'top'")
        print("To exit, type 'exit'")
    
    # pwedeng sa CNEM_Calc nang iimplement yung pag-open ng files

# how do you expect to run this?
# > py cnem_calc.py
# >>> this should be able to run defaults
# >>> external parameters: price, recipes, constraints
# >>>>>> madali lang defaults ng recipes at constraints, pero price hmm

# What do you want to tweak?
# > Recipe source (-r <filepath>)
# > Price source (-p <filepath>)
# > Constraints? (-c <filepath>)
# > Manual mode (-M)

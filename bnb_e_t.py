# Branch and Bounds Effectiveness Test
from cnem_calc import CNEM_Calc
import csv

if __name__ == "__main__":
    recipes_filename = "recipes.csv"
    prices_filename = "prices.csv"
    constraints_filename = "nutrition.csv"
    n_meals = 3
    n_mealsets = 5

    if True:
        recipes_filename = "test_data/recipes.csv"
        prices_filename = "test_data/p.csv"
        constraints_filename = "test_data/c.csv"


    recipes = []
    recipes_h  = []
    prices = []
    nutrition = []

    with open(recipes_filename, 'r') as recipes_db:
        recipes = list(csv.reader(recipes_db))
        recipes_h = recipes.pop(0) # recipes header

    with open(prices_filename, 'r') as prices_db:
        prices = list(csv.reader(prices_db))

    with open(constraints_filename, 'r') as nutrition_db:
        nutrition = list(csv.reader(nutrition_db))

    meal_calc = CNEM_Calc(recipes_h, recipes, prices, nutrition)
    meal_calc.n_mealsets = n_mealsets

    print("Test 1: w/ branch and bounds")
    print("Raw output: ", meal_calc.recursive_backtrack())
    print("Recursion calls: ", meal_calc.recursion_calls)
    print()

    recipes = []
    recipes_h  = []
    prices = []
    nutrition = []

    with open(recipes_filename, 'r') as recipes_db:
        recipes = list(csv.reader(recipes_db))
        recipes_h = recipes.pop(0) # recipes header

    with open(prices_filename, 'r') as prices_db:
        prices = list(csv.reader(prices_db))

    with open(constraints_filename, 'r') as nutrition_db:
        nutrition = list(csv.reader(nutrition_db))

    meal_calc_2 = CNEM_Calc(recipes_h, recipes, prices, nutrition)
    meal_calc_2.n_mealsets

    print("Test 2: w/o branch and bounds")
    print("Raw output: ", meal_calc_2.recursive_backtrack_no_bounds())
    print("Recursion calls: ", meal_calc_2.recursion_calls)
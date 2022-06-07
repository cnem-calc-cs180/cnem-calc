# cnem-calc
The Cost-to-Nutrition Efficiency Calculator (cnem-calc) is an AI-based program that suggests meals that are both cheap and nutritious using backtracking search. It uses ingredient prices from market price reports, ingredients and nutritional values of meals from online recipes and daily nutritional constraints to determine which meals to suggest. _It doesn't really analyze efficiency. It was a working title and the name stuck._


## Basic Operation
### Prerequisites
- Python 3

### How to Use
The program should come with demo datasets that have the filenames that are used by the program by default. These default filenames are:
- `recipes.csv` for the recipe database
- `prices.csv` for the ingredient prices
- `nutrition.csv` for the nutritional constraints 

To use the calculator, simply run the Python file, `cnem_calc.py`:

`py cnem_calc.py` or `python3 cnem_calc.py`

These use the default CSV files as described above as input. To override these, __Options__ may be added to the command. Currently only CSV format is supported.
- `-r <filepath>` - Uses `<filepath>` as the recipe database source
- `-p <filepath>` - Uses `<filepath>` as the ingredient price source
- `-c <filepath>` - Uses `<filepath>` as the nutritional constraints source
- `-M` - Allows the user the manually enter the filepaths through standard input during runtime. This __overrides__ the above options

Examples:

`py cnem_calc.py -r my_recipes.csv -c my_requirements.csv -p data/prices_today.csv`, `py cnem_calc.py -M`

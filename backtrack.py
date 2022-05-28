n_variables = 3 # number of meals in a meal set
n_values = 10 # number of recipes in our db
n_suggestions = 5 # number of meal sets we will suggest

def max_constraints(state, valid_states):
    # Check for constraints that impose a maximum for some values in the mealset
    # Currently only max constraints we have are:
    #   1. if the meals have total calories that exceed recommended
    #   2. if mealset is too expensive (relative to other mealsets found in valid_states)
    # return True if constraints are passed, else False
    # done outside of the base case so we can prune branches that already exceed the max constraints

    return True

def min_constraints(state, valid_states):
    # Check of constraints that impose a minimum of some values in the mealset
    # Currently only min constaints we have are:
    #   1. if meals have total nutritional value that meet daily recommended
    # return True if constraints are passed, else False
    # done within base case since we won't know if the meal set fails to meet the min requirements until it is complete

    return True

def backtrack(n_values, n_variables, n_suggestions, current_state = [], valid_states = []):
    # Recursive backtrack algorithm with depth n_variables
    # Variables are homogenous with domain n_values
    # Values are intended to be indices to database entries
    # Db or data must be accessed to interpret true meaning of the indices
    #
    # current_state - the meal set, array of indices of meals
    # valid_states - valid meal sets found so far, array of arrays
    #              - will hold the final list of meals we will suggest
    
    # max constraint checks #
    if not max_constraints(current_state, valid_states):
        return # if meals so far already exceed max constraints, skip this meal set (prune branch)

    if len(current_state) >= n_variables:
        # Base case
        # if there are already 3 meals found

        # min constraint checks #
        if not min_constraints(current_state, valid_states):
            return # if meals do not meet min constraint, do not add to valid meal sets

        # if 3 meals have already been found and it passes all constraints # 
        # add meal set to valid meal sets # valid_states.append(current_state)
        # sort valid meal sets by price # valid_states.sort(key=cost)
        # if there are more meal sets in the valid meal sets we intend to suggest # if len(valid_states) > n_suggestions:
        #   remove the most expensive one in the (sorted) list # valid_states.pop()

        return valid_states

    for n in range(n_values): # go through all possible indices
        next_state = current_state.copy() # make a copy of the meal set
        next_state.append(n) # and add the current meal to the set
        backtrack(n_values, n_variables, n_suggestions, next_state, valid_states) # get the next meal

    return valid_states # return the cheapest meal sets we found
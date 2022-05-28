n_variables = 3
n_values = 10
n_suggestions = 5

def backtrack(n_values, n_variables, n_suggestions, current_state = [], valid_states = []):
    # Recursive backtrack algorithm with depth n_variables
    # Variables are homogenous with domain n_values
    # Values are intended to be indices to database entries
    # Db or data must be accessed to interpret true meaning of the indices
    
    # max constraint checks #
    # 1. if too much calories
    # 2. if cost higher than bound
    # can be a separate function

    if len(current_state) >= n_variables:
        # min contraint checks #
        # 1. if each nutrient minimum is met

        # valid_states.append(current_state)
        # valid_states.sort(key=cost)
        # if len(valid_states) > n_suggestions:
        #   valid_states.pop()

        return valid_states

    for n in range(n_values):
        next_state = current_state.copy()
        next_state.append(n)
        backtrack(n_values, n_variables, n_suggestions, next_state, valid_states)

    return valid_states
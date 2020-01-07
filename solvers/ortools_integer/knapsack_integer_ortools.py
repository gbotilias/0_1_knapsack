from __future__ import print_function
from ortools.linear_solver import pywraplp

import time
import pandas as pd

# Create the mip solver with the CBC backend.
solver = pywraplp.Solver('simple_mip_program',
                         pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)


def knapsack_integer_programming_ortools():
    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    global sel_items, bin_weight, bin_value
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # Constraints
    # Each item can be in at most one bin.
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['bins']) <= 1)

    # The amount packed in each bin cannot exceed its capacity.
    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i]
                for i in data['items']) <= data['bin_capacities'][j])


    # Objective
    objective = solver.Objective()
    for i in data['items']:
        for j in data['bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])

    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        total_weight = 0
        for j in data['bins']:
            bin_weight = 0
            bin_value = 0
            sel_items = []

            for i in data['items']:
                if x[i, j].solution_value() > 0:
                    sel_items.append(data['items'][i])
                    bin_weight += data['weights'][i]
                    bin_value += data['values'][i]

            total_weight += bin_weight
    return bin_value, bin_weight, sel_items


def readFile(n, r, t, s):
    # Handle file problem with specific args
    file_handle = open('knapsack_prj/problem_' + str(n) + '_' + str(r) + '_' + str(t) + '_' + str(s) + '_' + '5.txt',
                       "r")
    line_list = file_handle.readlines()
    file_handle.close()

    global df, data, start_time
    # Initialize lists to fill them with indexes, values and weights
    data = {}
    indexes = []
    values = []
    weights = []

    # Parse file data
    num_of_items = (int(line_list[0]))  # First line = number of items
    for i in range(1, len(line_list) - 1):  # Split next lines and append them into indexes, values and weights
        splitter = line_list[i].split()
        indexes.append(splitter[0])
        values.append(int(splitter[1]))
        weights.append(int(splitter[2]))
    capacity = (int(line_list[-1]))  # Last line = capacity

    # Put all data in data{}
    data['weights'] = weights
    data['values'] = values
    data['items'] = list(range(len(weights)))
    data['num_items'] = num_of_items
    num_bins = 1
    data['bins'] = list(range(num_bins))
    data['bin_capacities'] = [capacity]

    # Call Integer Programming OrTools Solver algorithm to solve 0-1 knapsack problem
    # Return values -> 1.total_value 2.total_weight 3.selected_items
    # start() - stop() time
    start_time = time.time()
    total_value, total_weight, selected_items = knapsack_integer_programming_ortools()
    end_time = time.time()

    # Deal with dataframe to append the results
    df = df.append({'Problem': str(n) + "_" + str(r) + "_" + str(t) + "_" + str(s) + '_5',
                    'Total_Value': total_value,
                    'Total_Weight': total_weight,
                    'Selected_Items': "-".join(map(str, selected_items[:])).replace('[', '').replace(']', ''),
                    'Time': end_time - start_time},
                   ignore_index=True)


if __name__ == "__main__":
    # Create a 2-d data structure with row and columns dataframe
    df = pd.DataFrame(columns=['Problem', 'Total_Value', 'Total_Weight', 'Selected_Items', 'Time'])

    # Set lists of problem entries
    n_table = [10, 50, 100, 500]
    r_table = [50, 100, 500, 1000]

    # # All cases problems of knapsack generator
    for n in n_table:
        for r in r_table:
            for t in range(1, 5, 1):
                for s in range(1, 6, 1):
                    readFile(n, r, t, s)

    # Dataframe to csv
    df.to_csv("Integer_ortools_result.csv", index=False)

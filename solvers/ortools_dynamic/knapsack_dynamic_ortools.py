from ortools.algorithms import pywrapknapsack_solver
import time
import pandas as pd

solver = pywrapknapsack_solver.KnapsackSolver(
    pywrapknapsack_solver.KnapsackSolver
        .KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER,
    'Dynamic Programming solver')


def readFile(n, r, t, s):
    # Handle file problem with specific args
    file_handle = open('knapsack_prj/problem_' + str(n) + '_' + str(r) + '_' + str(t) + '_' + str(s) + '_' + '5.txt',
                       "r")
    line_list = file_handle.readlines()
    file_handle.close()

    # Initialize lists to fill them with indexes, values and weights
    global df
    values = []
    weights = []
    capacities = []
    items = []
    templist = []

    # Parse file data
    num_of_items = (int(line_list[0]))
    for g in range(1, len(line_list) - 1):
        splitter = line_list[g].split()
        items.append(splitter[0])
        values.append(int(splitter[1]))
        templist.append(int(splitter[2]))
    weights.append(templist)
    capacities.append(int(line_list[-1]))

    # Init solver with Data
    solver.Init(values, weights, capacities)

    # Call solver
    start_time = time.time()
    total_value = solver.Solve()
    end_time = time.time()

    # Find best solution(weights, items) for total value
    selected_items = []
    packed_weights = []
    total_weight = 0
    for i in range(num_of_items):
        if solver.BestSolutionContains(i):
            selected_items.append(items[i])
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]

    # Deal with dataframe to append the results
    df = df.append({'Problem': str(n) + "_" + str(r) + "_" + str(t) + "_" + str(s) + '_5',
                    'Total_Value': total_value,
                    'Total_Weight': total_weight,
                    'Selected_Items': "-".join(map(str, selected_items[:])).replace('[', '').replace(']', ''),
                    'Time': end_time - start_time},
                   ignore_index=True)


if __name__ == '__main__':
    # Create a 2-d data structure with row and columns dataframe
    df = pd.DataFrame(columns=['Problem', 'Total_Value', 'Total_Weight', 'Selected_Items', 'Time'])

    # Set lists of problem entries
    n_table = [10, 50, 100, 500]
    r_table = [50, 100, 500, 1000]

    # All cases problems of knapsack generator
    for n in n_table:
        for r in r_table:
            for t in range(1, 5, 1):
                for s in range(1, 6, 1):
                    readFile(n, r, t, s)

    # Dataframe to csv
    df.to_csv("Dynamic_ortools_result.csv", index=False)

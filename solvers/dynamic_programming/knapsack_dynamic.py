import time
import pandas as pd
import numpy as np


def knapsack_dynamic_programming(n, val, wt, W):
    table = np.zeros((n + 1, W + 1), dtype=np.float32)
    keep = np.zeros((n + 1, W + 1), dtype=np.float32)

    # Table K[][]
    for i in range(1, n + 1):
        for w in range(0, W + 1):
            wi = wt[i - 1]  # weight of current item
            vi = val[i - 1]  # value of current item
            if (wi <= w) and (vi + table[i - 1, w - wi] > table[i - 1, w]):
                table[i, w] = vi + table[i - 1, w - wi]
                keep[i, w] = 1

                # Check timer for 10 sec
                end_time = time.time()
                t = end_time - start_time
                if t > 10.0:
                    break
            else:
                table[i, w] = table[i - 1, w]

    # Initialize variables
    sel_items = []
    total_val = 0
    total_wt = 0

    # Find Total value, Total weight and Selected items
    for i in range(n, 0, -1):
        if keep[i, W] == 1:
            sel_items.append(i)
            W -= wt[i - 1]
            total_wt += wt[i - 1]
            total_val += val[i - 1]

    sel_items = [x for x in sel_items]  # change to 0-index

    return total_val, total_wt, sel_items


def readFile(n, r, t, s):
    # Handle file problem with specific args
    file_handle = open('knapsack_prj/problem_' + str(n) + '_' + str(r) + '_' + str(t) + '_' + str(s) + '_' + '5.txt',
                       "r")
    line_list = file_handle.readlines()
    file_handle.close()

    global df, total_value, total_weight, selected_items, start_time, end_time, items, capacity, num_of_items
    # Initialize lists to fill them with indexes, values and weights
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

    # Call Dynamic algorithm to solve 0-1 knapsack problem
    # Return values -> 1.total_value 2.total_weight 3.selected_items
    # start() - stop() time
    start_time = time.time()
    total_value, total_weight, selected_items = knapsack_dynamic_programming(num_of_items, values, weights, capacity)
    end_time = time.time()

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
    df.to_csv("Dynamic_result.csv", index=False)

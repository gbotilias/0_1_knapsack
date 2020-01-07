import time
import pandas as pd
import numpy as np
from operator import truediv


def knapsack_0_1_greedy(data_sorted_list, num_of_items, capacity):
    # Initialize variables
    total_value = 0
    total_weight = 0
    selected_items = []

    for i in range(num_of_items):
        inner_sel_item = []  # Inner list to keep select items in loop
        curIn = int(data_sorted_list[i][0])  # Index of specific item
        curVal = int(data_sorted_list[i][1])  # Value of specific item
        curWt = int(data_sorted_list[i][2])  # Weight of specific item
        if capacity - curWt >= 0:  # If weight of item fits in the knapsack
            capacity -= curWt  # Substract weight from capacity
            total_weight += curWt  # Add weight in total_weight
            total_value += curVal  # Add value in total_value
            inner_sel_item.append(curIn)  # Append index into inner list
        else:  # Else continue to next item
            continue

        selected_items.append(inner_sel_item)  # Append indexes tha we use to fill knapsack

    return total_value, total_weight, selected_items  # Return variables to make the result


def readFile(n, r, t, s):
    # Handle file problem with specific args
    file_handle = open('knapsack_prj/problem_' + str(n) + '_' + str(r) + '_' + str(t) + '_' + str(s) + '_' + '5.txt',
                       "r")
    line_list = file_handle.readlines()
    file_handle.close()

    global df
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

    # Find costs = v/w for greedy algorithm
    v_div_w = list(map(truediv, values, weights))
    costs = np.array(v_div_w, dtype=np.float32)

    # 4 subset lists into one list
    data_in_list = np.column_stack((indexes, values, weights, costs.astype(np.object)))

    # Sort List with subsets basis to bigger cost
    data_sorted_list = data_in_list[data_in_list[:, 3].argsort()[::-1][:num_of_items]]

    # Call Greedy algorithm to solve 0-1 knapsack problem
    # Return values -> 1.total_value 2.total_weight 3.selected_items
    # start() - stop() time
    start_time = time.time()
    total_value, total_weight, selected_items = knapsack_0_1_greedy(data_sorted_list, num_of_items, capacity)
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

    # All cases problems of knapsack generator
    for n in n_table:
        for r in r_table:
            for t in range(1, 5, 1):
                for s in range(1, 6, 1):
                    readFile(n, r, t, s)

    # Dataframe to csv
    df.to_csv("Greedy_result.csv", index=False)

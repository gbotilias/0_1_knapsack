import time
import pandas as pd


def knapsack_brute_force(items, capacity):
    global start_time, end_time, total_val, total_wt, sel_items
    # Initialize variables
    sel_items = []
    total_val = 0
    total_wt = 0

    # Create powersets([[],[1,v1,w1],[2,p2,w2]...[(1,p1,w1),..,(10,p10,w10)]] with all combinations for items data
    res = [[]]
    for item in items:
        new_set = [r + [item] for r in res]
        res.extend(new_set)

        # Check timer for 10 sec
        end_time = time.time()
        time_powerset = end_time - start_time
        if time_powerset > 5.0:
            break

    # Brute force algorithm in created powerset
    start_time2 = time.time()
    for item_set in res:
        set_value = sum(map(value, item_set))  # Sum values of each powerset
        set_weight = sum(map(weight, item_set))  # Sum weights of each powerset
        if set_value > total_val and set_weight <= capacity:  # If (current sumValue of powerset > totalValue) & (current sumWeight of powerset) < capacity
            total_wt = set_weight
            total_val = set_value
            sel_items = item_set
            # Check timer for 10 sec
            end_time = time.time()
            brute_time = end_time - start_time2
            if brute_time > 5.0:
                break

    return total_val, total_wt, sel_items


# Value in specific powerset
def value(item):
    return item[1]


# Weight in specific powerset
def weight(item):
    return item[2]


def readFile(n, r, t, s):
    # Handle file problem with specific args
    file_handle = open('knapsack_prj/problem_' + str(n) + '_' + str(r) + '_' + str(t) + '_' + str(s) + '_' + '5.txt',
                       "r")
    line_list = file_handle.readlines()
    file_handle.close()

    global df, total_value, total_weight, selected_items, start_time, end_time
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

    # Build data in tuple type(("ind1", "val1", "wt1"),("ind2", "val2", "wt2"),...) before call bruteForce
    items = [tuple((indexes[i], values[i], weights[i])) for i in range(0, num_of_items)]

    # Call Brute Force algorithm to solve 0-1 knapsack problem
    # Return values -> 1.total_value 2.total_weight 3.selected_items
    # start() - stop() time
    start_time = time.time()
    total_value, total_weight, selected_items = knapsack_brute_force(items, capacity)
    end_time = time.time()

    # Deal with dataFrame to append the results
    df = df.append({'Problem': str(n) + "_" + str(r) + "_" + str(t) + "_" + str(s) + '_5',
                    'Total_Value': total_value,
                    'Total_Weight': total_weight,
                    'Selected_Items': "-".join(sorted(item for item, _, _ in selected_items)),
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

    # DataFrame to csv
    df.to_csv("BruteForce_result.csv", index=False)

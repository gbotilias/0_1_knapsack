import time
import pandas as pd
from recordclass import recordclass
from collections import deque

# Struct to store Item info
Item = recordclass('Item', 'index value weight')
# Struct to store info of decision tree
# Level -> level of node in decision tree
# value -> profit of nodes on path from root to this node
# weight -> weight of nodes on path from root to this node
# items -> items of nodes on path from root to this node
Node = recordclass('Node', 'level value weight items')


def knapsack_branch_and_bound():
    # dummy node at starting
    v = Node(level=-1, value=0, weight=0, items=[])
    # make a queue for traversing the node
    Q = deque([])
    Q.append(v)

    # Initialize variables
    total_val = 0
    total_wt = 0
    sel_items = []

    while len(Q) != 0:
        # De-queue a node
        v = Q[0]
        Q.popleft()

        # Initialize Node
        u = Node(level=None, weight=None, value=None, items=[])

        u.level = v.level + 1  # Increment level
        u.weight = v.weight + items[u.level].weight  # Add current level's weight to node
        u.value = v.value + items[u.level].value  # Add current level's value to node
        u.items = list(v.items)  # Add current level's items[] to node
        u.items.append(items[u.level].index)  # Add to list of knapsack

        # Check if cumulated weight is less than capacity
        # and value is greater than previous total_val
        if u.weight <= capacity and u.value > total_val:
            total_val = u.value  # update total value
            total_wt = u.weight  # update total weight
            sel_items = u.items  # update selected items

        # Get the upper bound on profit to decide
        # whether to add v to Q or not.
        bound_u = bound(u, capacity, num_of_items, items)

        #  If bound value is greater than profit,
        #  then only push into queue for further consideration
        if bound_u > total_val:
            Q.append(u)

        #  Do the same thing,  but Without taking
        #  the item in knapsack
        u = Node(level=None, weight=None, value=None, items=[])
        u.level = v.level + 1
        u.weight = v.weight
        u.value = v.value
        u.items = list(v.items)

        bound_u = bound(u, capacity, num_of_items, items)

        if bound_u > total_val:
            Q.append(u)

        # Check timer for 10 sec
        end_time = time.time()
        t = end_time - start_time
        if t > 10.0:
            break

    # Get total value , weight and selected items
    output_data = str(total_val) + ' ' + str(total_wt) + '\n'
    output_data += ' '.join(map(str, sel_items))

    return total_val, total_wt, sel_items


# Returns bound of profit in subtree rooted with u.
# This function mainly uses Greedy solution to find
# an upper bound on maximum profit.
def bound(u, capacity, item_count, items):
    # if weight overcomes the knapsack capacity, return
    #  0 as expected bound
    if (u.weight >= capacity):
        return 0

    else:
        result = u.value  # initialize bound on profit by current profit
        # start including items from index 1 more to current
        # item index
        j = u.level + 1
        totweight = u.weight

        # checking index condition and knapsack capacity condition
        while (j < item_count and totweight + items[j].weight <= capacity):
            totweight = totweight + items[j].weight
            result = result + items[j].value
            j = j + 1

        # If k is not n, include last item partially for
        # upper bound on profit
        k = j
        if k <= item_count - 1:
            result = result + (capacity - totweight) * items[k].value / items[k].weight

        return result


def readFile(n, r, t, s):
    # Handle file problem with specific args
    file_handle = open('knapsack_prj/problem_' + str(n) + '_' + str(r) + '_' + str(t) + '_' + str(s) + '_' + '5.txt',
                       "r")
    line_list = file_handle.readlines()
    file_handle.close()

    global df, total_value, total_weight, selected_items, start_time, end_time, items, capacity, num_of_items
    # Initialize lists to fill them with indexes, values and weights
    items = []
    # Parse file data
    num_of_items = (int(line_list[0]))  # First line = number of items
    for i in range(1, len(line_list) - 1):  # Split next lines and append them into items->Items(i,p,w)
        splitter = line_list[i].split()
        items.append(Item(i, int(splitter[1]), int(splitter[2])))
    capacity = (int(line_list[-1]))  # Last line = capacity

    # Sort by cost
    items = sorted(items, key=lambda Item: Item.weight / Item.value)

    # Call Branch and Bound algorithm to solve 0-1 knapsack problem
    # Return values -> 1.total_value 2.total_weight 3.selected_items
    # start() - stop() time
    start_time = time.time()
    total_value, total_weight, selected_items = knapsack_branch_and_bound()
    end_time = time.time()

    # Deal with dataFrame to append the results
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
    df.to_csv("Branch&Bound_result.csv", index=False)

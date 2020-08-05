"""
Expanding Nebula
================

You've escaped Commander Lambda's exploding space station along with numerous escape pods full of bunnies. But - oh no! - one of the escape pods has flown into a nearby nebula, causing you to lose track of it. You start monitoring the nebula, but unfortunately, just a moment too late to find where the pod went. However, you do find that the gas of the steadily expanding nebula follows a simple pattern, meaning that you should be able to determine the previous state of the gas and narrow down where you might find the pod.

From the scans of the nebula, you have found that it is very flat and distributed in distinct patches, so you can model it as a 2D grid. You find that the current existence of gas in a cell of the grid is determined exactly by its 4 nearby cells, specifically, (1) that cell, (2) the cell below it, (3) the cell to the right of it, and (4) the cell below and to the right of it. If, in the current state, exactly 1 of those 4 cells in the 2x2 block has gas, then it will also have gas in the next state. Otherwise, the cell will be empty in the next state.

For example, let's say the previous state of the grid (p) was:
.O..
..O.
...O
O...

To see how this grid will change to become the current grid (c) over the next time step, consider the 2x2 blocks of cells around each cell.  Of the 2x2 block of [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which means this 2x2 block would become cell c[0][0] with gas in the next time step:
.O -> O
..

Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2], p[1][1], p[1][2]], two of the containing cells have gas, so in the next state of the grid, c[0][1] will NOT have gas:
O. -> .
.O

Following this pattern to its conclusion, from the previous state p, the current state of the grid c will be:
O.O
.O.
O.O

Note that the resulting output will have 1 fewer row and column, since the bottom and rightmost cells do not have a cell below and to the right of them, respectively.

Write a function solution(g) where g is an array of array of bools saying whether there is gas in each cell (the current scan of the nebula), and return an int with the number of possible previous states that could have resulted in that grid after 1 time step.  For instance, if the function were given the current state c above, it would deduce that the possible previous states were p (given above) as well as its horizontal and vertical reflections, and would return 4. The width of the grid will be between 3 and 50 inclusive, and the height of the grid will be between 3 and 9 inclusive.  The answer will always be less than one billion (10^9).
"""
import numpy as np
def bin_grid(num, m, x, y):
    return np.reshape(np.array(list(np.binary_repr(num).zfill(m))).astype(np.int8), (x,y))

def advance_day(grid):
    x = len(grid)
    y = len(grid[0])
    new_grid = [[0 for i in range(y-1)] for j in range(x-1)]
    for i in range(len(new_grid)):
        for j in range(len(new_grid[0])):
            if grid[i][j] + grid[i + 1][j] + grid[i][j + 1] + grid[i + 1][j + 1] == 1:
                new_grid[i][j] = 1
    return new_grid

def compare(g1, g2):
    if len(g1) != len(g2):
        return False
    if len(g1[0]) != len(g2[0]):
        return False
    for i in range(len(g1)):
        for j in range(len(g1[0])):
            if bool(g2[i][j]) != bool(g1[i][j]):
                return False
    return True
def brute_sol(grid):
    x = len(grid)
    y = len(grid[0])
    # print(advance_day(grid))
    count = 0
    for i in range(2 ** ((x+1)*(y+1))):
        test_grid = bin_grid(i, (x+1)*(y+1), x+1, y+1)
        advanced_test_grid = advance_day(test_grid)
        temp = compare(grid, advanced_test_grid)
        count += temp
        if temp != 0:
            print(test_grid)
    return count

def pred_col(col):
    start_zero = set([(0, 0), (3, 0), (0, 3), (1, 1), (2, 2), (1, 2), (2, 1), (3, 1), (1, 3), (2, 3), (3, 2), (3, 3)])
    start_one = set([(2, 0), (0, 2), (1, 0), (0, 1)])
    bits = [(0, 0), (0, 1), (1, 0), (1, 1)]
    start = [start_zero, start_one]
    h = len(col)
    s = []
    s.extend(start[col[0]])
    for i in range(1, h):
        temp = []
        goal = col[i]
        while len(s) > 0:
            cur = s.pop()
            left, right = cur[0] << 1, cur[1] << 1
            for combo in bits:
                new_left, new_right = left | combo[0], right | combo[1]
                if (new_left % 4, new_right % 4) in start[goal]:
                    temp.append([new_left, new_right])
        s = temp
    pred_graph = {}
    for pred in s:
        if pred[1] not in pred_graph:
            pred_graph[pred[1]] = []
        pred_graph[pred[1]].append(pred[0])
    return pred_graph

def combine_cols(freq_left, pred_right):
    if freq_left == None:
        return {key: len(pred_right[key]) for key in pred_right.keys()}
    freq_combined = {}
    for key in pred_right.keys():
        freq_combined[key] = sum([freq_left.get(val, 0) for val in pred_right[key]])
    return freq_combined

def solution(grid):
    pred_count = None
    for col in grid:
        pred_graph = pred_col(col)
        pred_count = combine_cols(pred_count, pred_graph)
    return sum(pred_count.values())

t1 = [
        [True, True, False, True, False, True, False, True, True, False], 
        [True, True, False, False, False, False, True, True, True, False], 
        [True, True, False, False, False, False, False, False, False, True], 
        [False, True, False, False, False, False, True, True, False, False]
    ]
t1_ans = 11567

t2 = [
        [True, False, True], 
        [False, True, False], 
        [True, False, True]
    ]
t2_ans = 4

t3 = [
        [True, False, False],
        [False, False, False],
        [False, True, True],
        [False, True, False]
    ]
# print(pred_col([1, 0, 1]))
# print(brute_sol(t2))
x = pred_col([1, 0, 1])
y = pred_col([0, 1, 0])

# print({key: len(x[key]) for key in x.keys()})
# for key in x.keys():
#     x[key] = len(x[key])
# print(x)
# print(combine_cols(x, y))
print(solution(t1))
print(solution(t2))
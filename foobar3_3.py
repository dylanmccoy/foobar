"""
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an solution in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].
"""
from fractions import Fraction
import numpy as np
import math
from collections import OrderedDict

def transform(mat, map):
    for key in map.keys():
        if key != map[key]:
            swap(mat, key, map[key])
    new_mat = [[] for i in range(len(mat))]
    for i in range(len(mat)):
        extend = []
        for j in range(len(mat)):
            if j in map:
                new_mat[i].append(mat[i][j])
            else:
                extend.append(mat[i][j])
        new_mat[i].extend(extend)
    return new_mat

def swap(mat, a, b):
    mat[a],mat[b] = mat[b],mat[a]

def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(arr,i,j):
    # print (i, j)
    # left = [] if i == 0 else m[:i]
    return arr[np.array(list(range(i))+list(range(i+1,arr.shape[0])))[:,np.newaxis],
            np.array(list(range(j))+list(range(j+1,arr.shape[1])))]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

def gcd(a, b):
    while(b):
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b / gcd(a, b)

def solution(mat):
    # mat = np.array(mat)
    # mat.sort(key=lambda row: row, reverse=True)
    # print(mat)
    if len(mat) == 1:
        return [1, 1]
    # mat = transform(mat)
    n = len(mat)
    m = len(mat[0])
    s, t = 0, 0                 # s = # stable states, t = # transient states
    last_trans = None
    cur_row = 0
    trans_map = OrderedDict()
    for j in range(n):
        row = mat[j]
        absorbing = True
        counts = 0
        for cell in row:
            if cell != 0:
                absorbing = False
            counts += cell
        if not absorbing:
            for i in range(m):
                row[i] = Fraction(row[i], counts)
            last_trans = j
            trans_map[j] = cur_row
            cur_row += 1
        s += absorbing
    mat = transform(mat, trans_map)
    # print(test)
    t = n - s
    # print(trans_map)
    # print(s, t)
    # print(trans_map)
    if t == 1:
        ans = []
        denom = 1
        for item in mat[last_trans]:
            denom = max(denom, item.denominator)
            ans.append(item.numerator)
        ans.append(denom)
        return ans
    

    q = [[0 for i in range(t)] for j in range(t)]       
    r = [[0 for i in range(s)] for j in range(t)]
    for x in range(t):
        for y in range(t):
            q[x][y] = mat[x][y]
        for y in range(t, m):
            r[x][y - t] = mat[x][y]
    q = np.array(q)
    r = np.array(r)
    
    # print(q, r)
    n = q
    n = getMatrixInverse(np.subtract(np.array([[1 if i == j else 0 for i in range(t)] for j in range(t)]), q))
    n = n[0]
    m = []
    denom = 1
    for i in range(s):
        cell = sum(n[j] * r[j][i] for j in range(t))
        denom = lcm(int(denom), int(cell.denominator))
        m.append(cell)

    ans = []
    for i in range(len(m)):
        frac = m[i]
        ans.append(int(frac.numerator * denom / frac.denominator))

    # for frac in m:
    ans.append(int(denom))
    # print(trans_map)
    # print(ans)
    return ans



m = [
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]

m1 = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
m2 = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]

m3 = [
  [0,0,0,0,0,0],  # s0, the initial state, goes to s1 and s5 with equal probability
  [0,1,0,0,0,1],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
# print(solution(m))
# print(solution(m3))
# print(solution(m1))

# print(solution(m2))

m4 = [
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
# test = np.array(m4)
# print(test)
# test.sort()
# print(test)
# print(solution(m4))
# test = np.array(m4)
# test[::-1].sort(axis=0)
# print(m4)
# m4.sort(key=lambda row: row, reverse=True)
# print(m4)
# print(test)

# solution([
#     [1, 2, 3, 0, 0, 0],
#     [4, 5, 6, 0, 0, 0],
#     [7, 8, 9, 1, 0, 0],
#     [0, 0, 0, 0, 1, 2],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0]
# ])
# solution([
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ])
# [1, 1, 1, 1, 1, 5]
# def simplify(x, y):
#     g = gcd(x, y)
#     return Fraction((x/g), (y/g))
# def transform1(mat):
#     sum_list = list(map(sum, mat))
#     bool_indices = list(map(lambda x: x == 0, sum_list))
#     indices = set([i for i, x in enumerate(bool_indices) if x])
#     new_mat = []
#     for i in range(len(mat)):
#         new_mat.append(list(map(lambda x: Fraction(0, 1) if(sum_list[i] == 0) else simplify(x, sum_list[i]), mat[i])))
#     # print("new_mat")
#     # for line in new_mat:
#     #     print(line)
#     transform_mat = []
#     zeros_mat = []
#     for i in range(len(new_mat)):
#         if i not in indices:
#             transform_mat.append(new_mat[i])
#         else:
#             zeros_mat.append(new_mat[i])
#     transform_mat.extend(zeros_mat)
#     print("tmat")
#     for line in transform_mat:
#         print(line)
#     tmat = []
#     for i in range(len(transform_mat)):
#         tmat.append([])
#         extend_mat = []
#         for j in range(len(transform_mat)):
#             if j not in indices:
#                 tmat[i].append(transform_mat[i][j])
#             else:
#                 extend_mat.append(transform_mat[i][j])
#         tmat[i].extend(extend_mat)
#     return tmat

# test = [
#     [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]

# test2 = [
#     [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]
# # test =[
# #     [0, 1, 2],
# #     [0, 0, 0],
# #     [1, 2, 3]
# # ]
# def find_map(mat):
#     cur_row = 0
#     absorbing = True
#     non_map = OrderedDict()
#     for i in range(len(mat)):
#         absorbing = True
#         for j in range(len(mat[0])):
#             if mat[i][j] != 0:
#                 absorbing = False
#         if not absorbing:
#             non_map[i] = cur_row
#             cur_row += 1
#     return non_map
# def transform(mat, map):
#     for key in map.keys():
#         if key != map[key]:
#             swap(mat, key, map[key])
#     new_mat = [[] for i in range(len(mat))]
#     for i in range(len(mat)):
#         extend = []
#         for j in range(len(mat)):
#             if j in map:
#                 new_mat[i].append(mat[i][j])
#             else:
#                 extend.append(mat[i][j])
#         new_mat[i].extend(extend)
#     for line in new_mat:
#         print(line)
#     # print(new_mat)
# def swap(mat, a, b):
#     mat[a],mat[b] = mat[b],mat[a]


# hi = find_map(test)
# print(hi)
# transform(test, hi)
# # for line in test:
# #     print(line)

# print("/////////")
# poop = transform1(test2)[0]
# for line in poop:
#     print(line)
assert (
    solution([
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]) == [7, 6, 8, 21]
)
 
assert (
    solution([
        [0, 1, 0, 0, 0, 1],
        [4, 0, 0, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]) == [0, 3, 2, 9, 14]
)
 
assert (
    solution([
        [1, 2, 3, 0, 0, 0],
        [4, 5, 6, 0, 0, 0],
        [7, 8, 9, 1, 0, 0],
        [0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]) == [1, 2, 3]
)
assert (
    solution([
        [0]
    ]) == [1, 1]
)
 
assert (
    solution([
        [0, 0, 12, 0, 15, 0, 0, 0, 1, 8],
        [0, 0, 60, 0, 0, 7, 13, 0, 0, 0],
        [0, 15, 0, 8, 7, 0, 0, 1, 9, 0],
        [23, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [37, 35, 0, 0, 0, 0, 3, 21, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [1, 2, 3, 4, 5, 15]
)
 
assert (
    solution([
        [0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
        [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
        [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
        [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
        [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [4, 5, 5, 4, 2, 20]
)
 
assert (
    solution([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [1, 1, 1, 1, 1, 5]
)
 
assert (
    solution([
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [2, 1, 1, 1, 1, 6]
)
 
assert (
    solution([
        [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
        [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
        [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [6, 44, 4, 11, 22, 13, 100]
)
 
assert (
    solution([
        [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
        [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
        [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
        [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [1, 1, 1, 2, 5]
)
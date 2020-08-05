"""
Escape Pods
===========

You've blown up the LAMBCHOP doomsday device and broken the bunnies out of Lambda's prison - and now you need to escape from the space station as quickly and as orderly as possible! The bunnies have all gathered in various locations throughout the station, and need to make their way towards the seemingly endless amount of escape pods positioned in other parts of the station. You need to get the numerous bunnies through the various rooms to the escape pods. Unfortunately, the corridors between the rooms can only fit so many bunnies at a time. What's more, many of the corridors were resized to accommodate the LAMBCHOP, so they vary in how many bunnies can move through them at a time. 

Given the starting room numbers of the groups of bunnies, the room numbers of the escape pods, and how many bunnies can fit through at a time in each direction of every corridor in between, figure out how many bunnies can safely make it to the escape pods at a time at peak.

Write a function answer(entrances, exits, path) that takes an array of integers denoting where the groups of gathered bunnies are, an array of integers denoting where the escape pods are located, and an array of an array of integers of the corridors, returning the total number of bunnies that can get through at each time step as an int. The entrances and exits are disjoint and thus will never overlap. The path element path[A][B] = C describes that the corridor going from A to B can fit C bunnies at each time step.  There are at most 50 rooms connected by the corridors and at most 2000000 bunnies that will fit at a time.

For example, if you have:
entrances = [0, 1]
exits = [4, 5]
path = [
  [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
  [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
  [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
  [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
  [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
  [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]

Then in each time step, the following might happen:
0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each time step.  (Note that in this example, room 3 could have sent any variation of 8 bunnies to 4 and 5, such as 2/6 and 6/6, but the final answer remains the same.)

Test cases
==========

Inputs:
    (int list) entrances = [0]
    (int list) exits = [3]
    (int) path = [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]
Output:
    (int) 6

Inputs:
    (int list) entrances = [0, 1]
    (int list) exits = [4, 5]
    (int) path = [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
Output:
    (int) 16
"""
from Queue import Queue

class Edge():
    def __init__(self, cap, s, t, flow=0):
        self.cap = cap
        self.flow = flow
        self.s = s
        self.t = t
    def __str__(self):
        return str(self.s) + "->" + str(self.t) + " " + str(self.flow) + "/" + str(self.cap)
    def __repr__(self):
        return self.__str__()
def describe(graph):
    print("----describing graph----")
    print("n =", len(graph))
    for line in graph:
        print(line)
    print("----done describing----")

def edmonds_karp(graph, s, t):
    n = len(graph)
    flow = 0
    while True:
        q = Queue()
        q.put(s)
        pred = [None] * n
        while not q.empty():
            cur = q.get()
            for e in graph[cur]:
                if pred[e.t] == None and e.t != s and e.cap > e.flow:
                    pred[e.t] = e
                    q.put(e.t)
        if pred[t] != None:
            df = float('inf')
            e = pred[t]
            while e != None:
                df = min(df, e.cap - e.flow)
                e = pred[e.s]
            e = pred[t]
            while e != None:
                e.flow += df
                e = pred[e.s]
            flow += df
        else:
            break
    return flow

def solution(entrances, exits, path):
    n = len(path)                                 # number of nodes
    adj_list = []
    for i in range(n):
        adj_row = []
        for j in range(n):
            if path[i][j] != 0:
                e = Edge(path[i][j], i, j)
                adj_row.append(e)
        adj_list.append(adj_row)
    source = []
    for room in entrances:
        e = Edge(float('inf'), n, room)
        source.append(e)
    adj_list.append(source)
    for room in exits:
        e = Edge(float('inf'), room, n+1)
        adj_list[room].append(e)
    adj_list.append([])
    describe(adj_list) 
    return edmonds_karp(adj_list, n, n+1)  

test1 = ([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
test2 = ([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])

ans1 = solution(test1[0], test1[1], test1[2])
ans2 = solution(test2[0], test2[1], test2[2])

print("ans1 =", ans1)
print("ans2 =", ans2)
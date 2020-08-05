"""
Bringing a Gun to a Guard Fight
===============================

Uh-oh - you've been cornered by one of Commander Lambdas elite guards! Fortunately, you grabbed a beam weapon from an abandoned guard post while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the elite guard: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either you or the guard, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, guard_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the guard's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite guard, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite guard are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite guard were positioned in a room with dimensions [3, 2], your_position [1, 1], guard_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite guard (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite guard with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite guard with a total shot distance of sqrt(5).

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
Solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9

-- Python cases --
Input:
solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9
"""
from Queue import Queue
import numpy as np
import math
class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def sq_dist(self, pos):
        return (pos.x - self.x) ** 2 + (pos.y - self.y) ** 2
    def unit_vec(self):
        if self.x == 0 and self.y == 0:
            return None
        v = np.array([self.x, self.y])
        return (v / np.linalg.norm(v))
    def diff(self, pos):
        return Position(pos.x - self.x, pos.y - self.y)
    def __eq__(self, obj):
        return self.x == obj.x and self.y == obj.y
    def __ne__(self, obj):
        return not self.__eq__(obj)
    def __hash__(self):
        return hash((self.x, self.y))
    def __str__(self):
        return "({},{})".format(self.x, self.y)
    def __repr__(self):
        return self.__str__()
    def __add__(self, pos):
        return Position(pos.x + self.x, pos.y + self.y)
    
def get_angle(shooter, target):
    return math.atan2(target.y - shooter.y, target.x - shooter.x)

def add_angles(shooter, target, targets):
    if shooter != target:
        angle = get_angle(shooter, target)
        dis = shooter.sq_dist(target)
        if angle in targets:
            targets[angle] = min(targets[angle], dis)
        else:
            targets[angle] = dis

def close_enough(x, y, max_dist):
    return x.sq_dist(y) <= max_dist ** 2
    
def offset(dim, pos, x_odd, y_odd):
    x_pos = dim[0] - pos.x if x_odd else pos.x
    y_pos = dim[1] - pos.y if y_odd else pos.y
    return Position(x_pos, y_pos)

def pos_from_coords(dim, pos_me, pos_guard, coords):
    ofst_me = offset(dim, pos_me, coords[0] % 2, coords[1] % 2)
    ofst_guard = offset(dim, pos_guard, coords[0] % 2, coords[1] % 2)
    bottom_left = Position(coords[0] * dim[0], coords[1] * dim[1])
    return [bottom_left + ofst_me, bottom_left + ofst_guard]

def solution(dim, pos_me, pos_guard, distance):
    pos_me = Position(pos_me[0], pos_me[1])
    pos_guard = Position(pos_guard[0], pos_guard[1])
    max_up = distance // dim[1] + 2
    max_left = distance // dim[0] + 2
    count_angles = 0
    obstacles = {}
    guards = {}

    for i in range(-1 * max_left, max_left + 1):
        for j in range(-1 * max_up, max_up + 1):
            new_me, new_guard = pos_from_coords(dim, pos_me, pos_guard, [i, j])
            if close_enough(pos_me, new_guard, distance):
                add_angles(pos_me, new_me, obstacles)
                add_angles(pos_me, new_guard, guards)
    for key in guards.keys():
        if key in obstacles:
            if guards[key] < obstacles[key]:
                count_angles += 1
        else:
            count_angles += 1

    return count_angles


pos1 = Position(1, 2)
pos2 = Position(-1,-2)
bad = Position(-3,-6)
# print(pos1 == pos2)

test1 = ([3,2], [1,1], [2,1], 4)
test2 = ([300,275], [150,150], [185,100], 500)
print(solution(test1[0], test1[1], test1[2], test1[3]))
print(solution(test2[0], test2[1], test2[2], test2[3]))
# print(Position(1,1) == Position(1,1))
# print(Position(1,1) != Position(1,1))
test3 = ([10,10], [4,4], [3,3], 5000)
test4 = ([23,10], [6,4], [3,2], 23)
print(solution(test3[0], test3[1], test3[2], test3[3]))
print(solution(test4[0], test4[1], test4[2], test4[3]))

test5 = ([2,5], [1,2], [1,4],11)
print(solution(test5[0], test5[1], test5[2], test5[3]))




# # from Queue import Queue
# # import numpy as np
# class Position():
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#     def sq_dist(self, pos):
#         return (pos.x - self.x) ** 2 + (pos.y - self.y) ** 2
#     def unit_vec(self):
#         if self.x == 0 and self.y == 0:
#             return None
#         v = np.array([self.x, self.y])
#         return (v / np.linalg.norm(v))
#     def diff(self, pos):
#         return Position(pos.x - self.x, pos.y - self.y)
#     def __eq__(self, obj):
#         return self.x == obj.x and self.y == obj.y
#     def __hash__(self):
#         return hash((self.x, self.y))
#     def __str__(self):
#         return "({},{})".format(self.x, self.y)
#     def __repr__(self):
#         return self.__str__()
    
# def in_the_way(pos_1, pos_2, obs):
#     if pos_1.sq_dist(obs) > pos_1.sq_dist(pos_2):
#         return False
#     else:
#         if obs == pos_1:
#             return False
#         slope_obs = float(obs.y - pos_1.y) / float(obs.x - pos_1.x)
#         slope_pos_2 = float(pos_2.y - pos_1.y) / float(pos_2.x - pos_1.x)
#         return slope_obs == slope_pos_2
# #TODO consider using slopes instead of positions to determine if a past thing has been done
# def can_fire(pos_1, pos_2, max_dist, obstacle, obstacles):
#     if pos_1.sq_dist(pos_2) <= max_dist ** 2:
#         if pos_1 != obstacle:
#             vec_obs = tuple(np.around(pos_1.diff(obstacle).unit_vec(), 4))
#             obstacles.add(vec_obs)
#             vec_1 = tuple(np.around(pos_1.diff(pos_2).unit_vec(), 4))
#             if vec_1 in obstacles:
#                 return False
#         return True
#     return False

# def mirror_pos(dim, pos, dir):
#     pos_new = Position(pos.x, pos.y)
#     if dir == "u":
#         # print("up")
#         pos_new.y += 2 * (dim[1] - (pos_new.y % dim[1]))
#     elif dir == "r":
#         # print("right")
#         pos_new.x += 2 * (dim[0] - (pos_new.x % dim[0]))
#     elif dir == "l":
#         # print("left")
#         pos_new.x -= 2 * ((pos_new.x % dim[0]))
#     elif dir == "d":
#         # print("down")
#         pos_new.y -= 2 * ((pos_new.y % dim[1]))
#     # print("hihihi", pos_new.x, pos_new.y)
#     return pos_new

# def solution(dim, pos_me, pos_guard, distance):
#     pos_me = Position(pos_me[0], pos_me[1])
#     pos_guard = Position(pos_guard[0], pos_guard[1])
#     q = Queue()
#     seen = set()
#     dirs = ["u", "d", "l", "r"]
#     q.put((pos_guard, pos_me))
#     count_angles = 0
#     obstacles = set()
#     angles = []
#     test =[]
#     vecs = []
#     while not q.empty():
#         cur_target, cur_obs = q.get()
#         vec = tuple(np.around(pos_me.diff(cur_target).unit_vec(), 4))
#         if vec in seen:
#             continue
#         seen.add(vec)
#         # print(cur_target)
#         if can_fire(pos_me, cur_target, distance, cur_obs, obstacles):
#             angles.append(cur_target)
#             test.append(cur_obs)
#             count_angles += 1
#             vecs.append(vec)
#             # for d in dirs:
#             #     new_target = mirror_pos(dim, cur_target, d)
#             #     new_obs = mirror_pos(dim, cur_obs, d)
#             #     target_vec = tuple(np.around(pos_me.diff(new_target).unit_vec(), 4))
#             #     # print("new", pos_new.x, pos_new.y)
#             #     if target_vec not in seen:
#             #         q.put((new_target, new_obs))
#         for d in dirs:
#             new_target = mirror_pos(dim, cur_target, d)
#             new_obs = mirror_pos(dim, cur_obs, d)
#             target_vec = tuple(np.around(pos_me.diff(new_target).unit_vec(), 4))
#             # print("new", pos_new.x, pos_new.y)
#             # if pos_me.sq_dist(new_target) <= distance ** 2:
#             if target_vec not in seen:
#                 q.put((new_target, new_obs))

#     print(angles)
#     print(test)
#     print(vecs)
#     return count_angles

# print(solution(test5[0], test5[1], test5[2], test5[3]))

# a = [(-9,4), (-9,6), (-7,-4), (-7,4), (-7,6), (-5,-6), (-5,-4), (-5,4), (-5,6), (-3,-6), (-3,-4), (-1,-6), (-1,-4), (-1,6), (1,4), (3,-6), (3,-4), (3,4), (3,6), (5,-4), (5,4), (7,-6), (7,4), (7,6), (9,-4), (9,4), (11,4), (11,6)]
# b = [(-9,2), (-9,8), (-7,-2), (-7,2), (-7,8), (-5,-8), (-5,-2), (-5,2), (-5,8), (-3,-8), (-3,-2), (-1,-8), (-1,-2), (-1,8), (1,2), (3,-8), (3,-2), (3,2), (3,8), (5,-2), (5,2), (7,-8), (7,2), (7,8), (9,-2), (9,2), (11,2), (11,8)]
# e = [(-0.9806, 0.1961), (-0.9285, 0.3714), (-0.8, -0.6), (-0.9701, 0.2425), (-0.8944, 0.4472), (-0.6, -0.8), (-0.7071, -0.7071), (-0.9487, 0.3162), (-0.8321, 0.5547), (-0.4472, -0.8944), (-0.5547, -0.8321), (-0.2425, -0.9701), (-0.3162, -0.9487), (-0.4472, 0.8944), (0.0, 1.0), (0.2425, 
# -0.9701), (0.3162, -0.9487), (0.7071, 0.7071), (0.4472, 0.8944), (0.5547, -0.8321), (0.8944, 0.4472), (0.6, -0.8), (0.9487, 0.3162), (0.8321, 0.5547), (0.8, -0.6), (0.9701, 0.2425), (0.9806, 0.1961), (0.9285, 0.3714)]

# c = [(1,4), (-1,4), (3,4), (-1,-4), (3,-4), (-1,6), (-3,4), (3,6), (5,4), (-1,-6), (-3,-4), (3,-6), (5,-4), (-5,4), (7,4), (-5,6), (-7,4), (7,6), (9,4), (-5,-6), (-7,-4), (7,-6), (9,-4), (-9,4), (11,4), (-9,6), (11,6)]
# d = [(1,2), (-1,2), (3,2), (-1,-2), (3,-2), (-1,8), (-3,2), (3,8), (5,2), (-1,-8), (-3,-2), (3,-8), (5,-2), (-5,2), (7,2), (-5,8), (-7,2), (7,8), (9,2), (-5,-8), (-7,-2), (7,-8), (9,-2), (-9,2), (11,2), (-9,8), (11,8)]
# f = [(0.0, 1.0), (-0.7071, 0.7071), (0.7071, 0.7071), (-0.3162, -0.9487), (0.3162, -0.9487), (-0.4472, 0.8944), (-0.8944, 0.4472), (0.4472, 0.8944), (0.8944, 0.4472), (-0.2425, -0.9701), (-0.5547, -0.8321), (0.2425, -0.9701), (0.5547, -0.8321), (-0.9487, 0.3162), (0.9487, 0.3162), (-0.8321, 0.5547), (-0.9701, 0.2425), (0.8321, 0.5547), (0.9701, 0.2425), (-0.6, -0.8), (-0.8, -0.6), (0.6, -0.8), (0.8, -0.6), (-0.9806, 0.1961), (0.9806, 0.1961), (-0.9285, 0.3714), (0.9285, 0.3714)]

# for i in range(len(a)):
#     if a[i] not in c:
#         print(a[i], b[i])
# print("hi")
# for i in range(len(c)):
#     if c[i] not in a:
#         print(c[i], d[i])

# for i in range(len(f)):
#     if f[i] not in e:
#         print(f[i], c[i], d[i])
"""
THE FOLLOWING PASSING FOR ALL BUT TEST CASE 3, BUT IT IS BROKEN?
# from Queue import Queue
# import numpy as np
# class Position():
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#     def sq_dist(self, pos):
#         return (pos.x - self.x) ** 2 + (pos.y - self.y) ** 2
#     def unit_vec(self):
#         if self.x == 0 and self.y == 0:
#             return None
#         v = np.array([self.x, self.y])
#         return (v / np.linalg.norm(v))
#     def diff(self, pos):
#         return Position(pos.x - self.x, pos.y - self.y)
#     def __eq__(self, obj):
#         return self.x == obj.x and self.y == obj.y
#     def __hash__(self):
#         return hash((self.x, self.y))
#     def __str__(self):
#         return "({},{})".format(self.x, self.y)
#     def __repr__(self):
#         return self.__str__()
    
# def in_the_way(pos_1, pos_2, obs):
#     if pos_1.sq_dist(obs) > pos_1.sq_dist(pos_2):
#         return False
#     else:
#         if obs == pos_1:
#             return False
#         slope_obs = float(obs.y - pos_1.y) / float(obs.x - pos_1.x)
#         slope_pos_2 = float(pos_2.y - pos_1.y) / float(pos_2.x - pos_1.x)
#         return slope_obs == slope_pos_2
# #TODO consider using slopes instead of positions to determine if a past thing has been done
# def can_fire(pos_1, pos_2, max_dist, obstacle):
#     if pos_1.sq_dist(pos_2) <= max_dist ** 2:
#         if pos_1.sq_dist(pos_2) > pos_1.sq_dist(obstacle):
#             vec_1 = pos_1.diff(pos_2).unit_vec()
#             vec_obs = pos_1.diff(obstacle).unit_vec()
#             if all(vec_1 == vec_obs):
#                 return False
#         return True
#     return False

# def mirror_pos(dim, pos, dir):
#     pos_new = Position(pos.x, pos.y)
#     if dir == "u":
#         # print("up")
#         pos_new.y += 2 * (dim[1] - (pos_new.y % dim[1]))
#     elif dir == "r":
#         # print("right")
#         pos_new.x += 2 * (dim[0] - (pos_new.x % dim[0]))
#     elif dir == "l":
#         # print("left")
#         pos_new.x -= 2 * ((pos_new.x % dim[0]))
#     elif dir == "d":
#         # print("down")
#         pos_new.y -= 2 * ((pos_new.y % dim[1]))
#     # print("hihihi", pos_new.x, pos_new.y)
#     return pos_new

# def solution(dim, pos_me, pos_guard, distance):
#     pos_me = Position(pos_me[0], pos_me[1])
#     pos_guard = Position(pos_guard[0], pos_guard[1])
#     q = Queue()
#     seen = set()
#     dirs = ["u", "d", "l", "r"]
#     q.put((pos_guard, pos_me))
#     count_angles = 0
#     angles = []
#     while not q.empty():
#         cur_target, cur_obs = q.get()
#         vec = tuple(pos_me.diff(cur_target).unit_vec())
#         if vec in seen:
#             continue
#         seen.add(vec)
#         # print(cur_target)
#         if can_fire(pos_me, cur_target, distance, cur_obs):
#             angles.append(cur_target)
#             count_angles += 1
#             for d in dirs:
#                 new_target = mirror_pos(dim, cur_target, d)
#                 new_obs = mirror_pos(dim, cur_obs, d)
#                 target_vec = tuple(pos_me.diff(new_target).unit_vec())
#                 # print("new", pos_new.x, pos_new.y)
#                 if target_vec not in seen:
#                     q.put((new_target, new_obs))
#     # print(angles)
#     return count_angles
"""
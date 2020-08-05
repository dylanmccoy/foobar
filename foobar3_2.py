"""

Fuel Injection Perfection
=========================

Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for her LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP - and maybe sneak in a bit of sabotage while you're at it - so you took the job gladly. 

Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. 

The fuel control mechanisms have three operations: 

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.

For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution('15')
Output:
    5

Input:
solution.solution('4')
Output:
    2

"""

import unittest

def split_recur(n, dp = {1 : 0}):
    # print(n)
    if n in dp:
        return dp[n]
    else:
        if n % 2 == 0:
            dp[n] = split_recur(n // 2, dp) + 1
        else:
            add = split_recur((n + 1) // 2, dp)
            remove = split_recur((n - 1) // 2, dp)
            dp[n] = min(add, remove) + 2
    return dp[n]

def solution1(n_str):
    n = int(n_str)
    dp = {}
    i = 1
    count = 0
    while i < n:
        dp[i] = count
        i *= 2
        count += 1
    return split_recur(n, dp)

def solution(n_str):
    n = int(n_str)
    ops = 0
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            # try adding
            if n == 3:
                n = 2
            else:
                n = n + 1 if ((n + 1) // 2) % 2 == 0 else n - 1
        ops += 1
    return ops

class TestStringMethods(unittest.TestCase):
    def test1(self):
        n = "15"
        self.assertEqual(solution(n), 5)
    def test2(self):
        n = "4"
        self.assertEqual(solution(n), 2)
    def test3(self):
        n = "16"
        self.assertEqual(solution(n), 4)
    def test_long(self):
        n = str(2 ** 1000)
        self.assertEqual(solution(n), 1000)
    def test_three(self):
        n = str(3)
        self.assertEqual(solution(n), 2)
    # def test_long_10(self):
    #     n = str(10 ** 300 + 1234324724)
    #     self.assertEqual(solution(n), 413)
# import sys
unittest.main()
# print(sys.getrecursionlimit())
# print("15=", split_recur(15))
# print("4=", split_recur(4))
# print("16=", split_recur(16))
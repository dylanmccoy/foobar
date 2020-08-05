def re_id(n):
    max_sieve = 3 * (n + 5)
    sieve = [True] * max_sieve
    primes = []
    len_so_far = 0
    overshoot = 0
    for next_p in range(2, max_sieve):
        if len_so_far >= n + 5:
            break
        if sieve[next_p]:
            len_so_far += len(str(next_p))
            if len_so_far > n:
                if len_so_far - len(str(next_p)) < n:
                    overshoot = len_so_far - (n + 1)
                    print(next_p, len_so_far, n)
                primes.append(str(next_p))
                # print(overshoot)
            # primes.append(str(next_p))
            for next_c in range(next_p * next_p, max_sieve, next_p):
                sieve[next_c] = False
    print("overshoot", overshoot)
    print("".join(primes))
    return "".join(primes)[overshoot:overshoot + 5]

def isPrime(n): 
      
    # Corner case 
    if (n <= 1): 
        return False
  
    # Check from 2 to n-1 
    for i in range(2, n): 
        if (n % i == 0): 
            return False
  
    return True
# primes = []
# for i in range(110):
#     if isPrime(i):
#         primes.append(str(i))
# check = "".join(primes)
# print("".join(primes))
# # print(re_id(5))
# for i in range(48):
#     ans = re_id(i)
#     # print("re_id({}), {}".format(i, ans))
#     if ans != check[i: i+5]:
#         print(i, "did not work")
#         print("expected", check[i: i+5])
#         print("actual", ans)
from Queue import Queue
def min_moves(start, target):
    # moves = [[2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]
    moves = [10, 17, 15, 6, -17, -10, -15, -6]
    board = [False] * 64
    q = Queue()
    q.put([start, 0])
    while not q.empty():
        cur, num_moves = q.get()
        board[cur] = True
        for move in moves:
            new_move = move + cur
            if new_move == target:
                return num_moves + 1
            elif 0 <= new_move < 64 and board[new_move] == False:
                q.put([new_move, num_moves + 1])
    return None

# board = [False] * 64
# print(min_moves(19, 36))

# Python3 code to find minimum steps to reach  
# to specific cell in minimum moves by Knight  
class cell: 
      
    def __init__(self, x = 0, y = 0, dist = 0): 
        self.x = x 
        self.y = y 
        self.dist = dist 
          
# checks whether given position is  
# inside the board 
def isInside(x, y, N): 
    if (x >= 1 and x <= N and 
        y >= 1 and y <= N):  
        return True
    return False
      
# Method returns minimum step to reach 
# target position  
def minStepToReachTarget(knightpos,  
                         targetpos, N): 
      
    #all possible movments for the knight 
    dx = [2, 2, -2, -2, 1, 1, -1, -1] 
    dy = [1, -1, 1, -1, 2, -2, 2, -2] 
      
    queue = [] 
      
    # push starting position of knight 
    # with 0 distance 
    queue.append(cell(knightpos[0], knightpos[1], 0)) 
      
    # make all cell unvisited  
    visited = [[False for i in range(N + 1)]  
                      for j in range(N + 1)] 
      
    # visit starting state 
    visited[knightpos[0]][knightpos[1]] = True
      
    # loop untill we have one element in queue  
    while(len(queue) > 0): 
          
        t = queue[0] 
        queue.pop(0) 
          
        # if current cell is equal to target  
        # cell, return its distance  
        if(t.x == targetpos[0] and 
           t.y == targetpos[1]): 
            return t.dist 
              
        # iterate for all reachable states  
        for i in range(8): 
              
            x = t.x + dx[i] 
            y = t.y + dy[i] 
              
            if(isInside(x, y, N) and not visited[x][y]): 
                visited[x][y] = True
                queue.append(cell(x, y, t.dist + 1)) 
  
# Driver Code      
if __name__=='__main__':  
    N = 8
    knightpos = [0, 0] 
    targetpos = [0, 1] 
    print(minStepToReachTarget(knightpos, 
                               targetpos, N)) 
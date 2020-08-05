from collections import deque


# queue node used in BFS
class Node:
	# (x, y) represents chess board coordinates
	# dist represent its minimum distance from the source
	def __init__(self, x, y, dist=0):

		self.x = x
		self.y = y
		self.dist = dist

	# As we are using Node as a key in a dictionary,
	# we need to implement hashCode() and equals()
	def __hash__(self):

		return hash((self.x, self.y, self.dist))

	def __eq__(self, other):

		return (self.x, self.y, self.dist) == (other.x, other.y, other.dist)


# Below lists details all 8 possible movements for a knight
row = [2, 2, -2, -2, 1, 1, -1, -1]
col = [-1, 1, 1, -1, 2, -2, 2, -2]


# Check if (x, y) is valid chess board coordinates
# Note that a knight cannot go out of the chessboard
def valid(x, y, N):
	return not (x < 0 or y < 0 or x >= N or y >= N)


# Find minimum number of steps taken by the knight
# from source to reach destination using BFS
def BFS(src, dest, N):

	# set to check if matrix cell is visited before or not
	visited = set()

	# create a queue and enqueue first node
	q = deque()
	q.append(src)

	# run till queue is not empty
	while q:

		# pop front node from queue and process it
		node = q.popleft()

		x = node.x
		y = node.y
		dist = node.dist

		# if destination is reached, return distance
		if x == dest.x and y == dest.y:
			return dist

		# Skip if location is visited before
		if node not in visited:
			# mark current node as visited
			visited.add(node)

			# check for all 8 possible movements for a knight
			# and enqueue each valid movement into the queue
			for i in range(8):
				# Get the valid position of Knight from current position on
				# chessboard and enqueue it with +1 distance
				x1 = x + row[i]
				y1 = y + col[i]

				if valid(x1, y1, N):
					q.append(Node(x1, y1, dist + 1))

	# return INFINITY if path is not possible
	return float('inf')

from queue import Queue
def in_bounds(x, y):
    if 0 <= x < 8 and 0 <= y < 8:
        return True
    else:
        return False
def min_moves(start, target):
    moves = [[2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]
    if start == target:
        return 0
    # moves = [10, 17, 15, 6, -17, -10, -15, -6]
    board = [[False] * 8 for i in range(8)]
    start_loc = (start % 8, start // 8)
    target_loc = (target % 8, target // 8)
    q = Queue()
    q.put([start_loc, 0])
    while not q.empty():
        cur, num_moves = q.get()
        board[cur[0]][cur[1]] = True
        for move in moves:
            new_move = (cur[0] + move[0], cur[1] + move[1])
            if new_move == target_loc:
                return num_moves + 1
            elif in_bounds(new_move[0], new_move[1]) and board[new_move[0]][new_move[1]] == False:
                q.put([new_move, num_moves + 1])
    return None

if __name__ == '__main__':
    N = 8

    src = Node(0, 0)   # source coordinates
    dest = Node(1, 0)  # destination coordinates
    print(min_moves(63, 54))
    print("Minimum number of steps required is", BFS(src, dest, N))
    for i in range(8):
        for j in range(8):
            for x in range(8):
                for y in range(8):
                    src = Node(i, j)
                    dest = Node(x, y)
                    source = i + 8 * j
                    target = x + 8 * y
                    mine = min_moves(source, target)
                    theirs = BFS(src, dest, N)
                    if mine != theirs:
                        print("wrong answer for", source, target)
                        print("mine", mine)
                        print("theirs", theirs)
                

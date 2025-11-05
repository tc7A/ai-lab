import heapq

class PuzzleState:
    def __init__(self, row, col, board, start, goal, g=0, parent=None):
        self.row = row
        self.col = col
        self.board = board
        self.start = start
        self.goal = goal
        self.g = g  
        self.h = self.heuristic()
        self.f = self.g + self.h
        self.parent = parent
    
    def heuristic(self):
        distance = 0
        for i in range(self.row):
            for j in range(self.col):
                val = self.board[i][j]
                if val != 0:
                    goal_i, goal_j = self.goal
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance
    
    def __lt__(self, other):
        return self.f < other.f

    def find_zero(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i][j] == 0:
                    return i, j

    def get_neighbors(self):
        neighbors = []
        x, y = self.find_zero()
        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.row and 0 <= ny < self.col:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                neighbors.append(PuzzleState(self.row, self.col, new_board, self.start, self.goal, self.g + 1, self))
        return neighbors
    
    def reconstruct_path(self):
        path = []
        state = self
        while state:
            path.append(state.find_zero())
            state = state.parent
        return path[::-1]

if __name__ == "__main__":
    # x = int(input("Enter number of row: "))
    # y = int(input("Enter number of col: "))

    # board = []
    # for i in range(x):
    #     row = []
    #     for j in range(y):
    #         a = int(input(f"Enter G[{i}][{j}]: "))
    #         row.append(a)
    #     board.append(row)
    board = [
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
    ]
    
    # start = []
    # print("Enter Start Position: ", end="")
    # for i in range(2):
    #     x = input()
    #     start.append(x)

    # goal = []
    # print("Enter Goal Position: ", end="")
    # for i in range(2):
    #     x = input()
    #     goal.append(x)

    x, y = 5, 5
    start_pos = ( 0, 0)
    goal_pos = ( 4, 4)

    puzzle = PuzzleState(x, y, board, start_pos, goal_pos)

    open_list =[]
    heapq.heappush(open_list, puzzle)
    visited = set()

    while open_list:
        current = heapq.heappop(open_list)
        if current.find_zero() == goal_pos:
            path = current.reconstruct_path()
            print(f"Path: {path}")
            print(f"Total Path Cost: {current.g}")
            break

        for neighbor in current.get_neighbors():
            if tuple(map(tuple, neighbor.board)) not in visited:
                visited.add(tuple(map(tuple, neighbor.board)))
                heapq.heappush(open_list, neighbor)
    else:
        print("No Path Found")
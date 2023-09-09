import random

def generateRandomBoard(N):
    board = [[0] * N for _ in range(N)]
    numbers = list(range(1, N * N))
    random.shuffle(numbers)
    for i in range(N):
        for j in range(N):
            if i == N - 1 and j == N - 1:
                board[i][j] = 0
            else:
                board[i][j] = numbers.pop(0)
    return board

def isGoal(board):
    N = len(board)
    n = 1
    for i in range(N):
        for j in range(N):
            if n == N * N:
                return board[i][j] == 0
            if board[i][j] != n:
                return False
            n += 1

def manhattanDistance(board):
    N = len(board)
    distance = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                continue
            target_val = board[i][j] - 1
            target_x, target_y = divmod(target_val, N)
            distance += abs(i - target_x) + abs(j - target_y)
    return distance

def idaStar(board):
    N = len(board)
    path = []
    visited = set()

    def dfs(board, g, bound):
        state_str = str(board)
        if state_str in visited:
            return float('inf')
        visited.add(state_str)

        h = manhattanDistance(board)
        f = g + h

        if f > bound:
            return f

        if isGoal(board):
            return -1

        min_bound = float('inf')
        zero_x, zero_y = 0, 0

        for i in range(N):
            for j in range(N):
                if board[i][j] == 0:
                    zero_x, zero_y = i, j

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = zero_x + dx, zero_y + dy

            if 0 <= new_x < N and 0 <= new_y < N:
                board[zero_x][zero_y], board[new_x][new_y] = board[new_x][new_y], board[zero_x][zero_y]
                path.append((new_x, new_y))

                t = dfs(board, g + 1, bound)

                if t == -1:
                    return -1
                if t < min_bound:
                    min_bound = t

                path.pop()
                board[zero_x][zero_y], board[new_x][new_y] = board[new_x][new_y], board[zero_x][zero_y]

        visited.remove(state_str)
        return min_bound

    bound = manhattanDistance(board)
    while True:
        visited.clear()
        t = dfs(board, 0, bound)
        if t == -1:
            return path
        if t == float('inf'):
            return None
        bound = t

if __name__ == "__main__":
    N = 4
    board = generateRandomBoard(N)

    print("Random Initial Board:")
    for row in board:
        print(row)

    solutionPath = idaStar(board)
    if solutionPath:
        print("\nSolution found:")
        for move in solutionPath:
            print(move)
    else:
        print("\nNo solution found")

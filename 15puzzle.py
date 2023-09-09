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
                board[i][j] = numbers.pop()
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
            targetVal = board[i][j] - 1
            targetX, targetY = divmod(targetVal, N)
            distance += abs(i - targetX) + abs(j - targetY)
    return distance

def isSolvable(board):
    N = len(board)
    invCount = 0
    flatBoard = [cell for row in board for cell in row if cell != 0]
    for i in range(len(flatBoard) - 1):
        for j in range(i+1, len(flatBoard)):
            if flatBoard[i] > flatBoard[j]:
                invCount += 1
    return invCount % 2 == 0

def idaStar(board):
    N = len(board)
    path = []

    def dfs(board, g, bound, parentX, parentY):
        h = manhattanDistance(board)
        f = g + h

        if f > bound:
            return f

        if isGoal(board):
            return -1

        minBound = float('inf')
        zeroX, zeroY = 0, 0

        for i in range(N):
            for j in range(N):
                if board[i][j] == 0:
                    zeroX, zeroY = i, j

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newX, newY = zeroX + dx, zeroY + dy

            if 0 <= newX < N and 0 <= newY < N and (newX != parentX or newY != parentY):
                board[zeroX][zeroY], board[newX][newY] = board[newX][newY], board[zeroX][zeroY]
                path.append((newX, newY))

                t = dfs(board, g + 1, bound, zeroX, zeroY)

                if t == -1:
                    return -1
                if t < minBound:
                    minBound = t

                path.pop()
                board[zeroX][zeroY], board[newX][newY] = board[newX][newY], board[zeroX][zeroY]

        return minBound

    bound = manhattanDistance(board)
    while True:
        t = dfs(board, 0, bound, -1, -1)
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

    if isSolvable(board):
        solutionPath = idaStar(board)
        if solutionPath:
            print("\nSolution found:")
            for move in solutionPath:
                print(move)
        else:
            print("\nNo solution found")
    else:
        print("\nThis puzzle is not solvable")

import random

# Function to generate a random and solvable NxN puzzle board
def generateRandomBoard(boardSize):
    while True:
        board = [0] * (boardSize * boardSize)
        numbers = list(range(1, boardSize * boardSize))
        random.shuffle(numbers)
        for i in range(boardSize * boardSize - 1):
            board[i] = numbers.pop()
        board[-1] = 0

        if isSolvable(board, boardSize):
            return board

# Function to check if the current board is the goal state
def isGoal(board, boardSize):
    for i in range(boardSize * boardSize):
        if board[i] != i:
            return False
    return True

# Function to calculate the Manhattan distance heuristic for a given board
def manhattanDistance(board, boardSize):
    distance = 0
    for i in range(boardSize * boardSize):
        if board[i] == 0:
            continue
        targetVal = board[i] - 1
        x, y = divmod(i, boardSize)
        targetX, targetY = divmod(targetVal, boardSize)
        distance += abs(x - targetX) + abs(y - targetY)
    return distance

# Function to incrementally update Manhattan distance after a move
def manhattanDelta(board, oldIndex, newIndex, boardSize):
    delta = 0
    for oi, ni in [(oldIndex, newIndex), (newIndex, oldIndex)]:
        value = board[oi]
        if value == 0:
            continue
        targetVal = value - 1
        x, y = divmod(oi, boardSize)
        targetX, targetY = divmod(targetVal, boardSize)
        newX, newY = divmod(ni, boardSize)
        delta += abs(targetX - newX) + abs(targetY - newY) - abs(targetX - x) - abs(targetY - y)
    return delta

'''
If the total number of inversions is even, the puzzle is solvable.
If the total number of inversions is odd, the puzzle is unsolvable.
This is a proven property of the N-puzzle problem and is based on the idea of parity. 
In puzzles with an odd number of inversions, there is no way to transform the puzzle into a solved state by swapping tiles 
because each swap changes the parity (odd to even or even to odd), making it impossible to reach a solved 
state with an even number of inversions.
'''

# Function to check if a given board is solvable
def isSolvable(board, boardSize):
    inversionCount = 0
    flatBoard = [cell for cell in board if cell != 0]
    for i in range(len(flatBoard) - 1):
        for j in range(i + 1, len(flatBoard)):
            if flatBoard[i] > flatBoard[j]:
                inversionCount += 1
    return inversionCount % 2 == 0

# Function to perform the IDA* search algorithm to find a solution path
def idaStar(board, boardSize):
    path = []

    def dfs(board, g, bound, zeroIndex):
        h = manhattanDistance(board, boardSize)
        f = g + h
        if f > bound:
            return f
        if isGoal(board, boardSize):
            return -1
        minBound = float('inf')
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = divmod(zeroIndex, boardSize)
            newX, newY = x + dx, y + dy
            if 0 <= newX < boardSize and 0 <= newY < boardSize:
                newZeroIndex = newX * boardSize + newY
                delta = manhattanDelta(board, zeroIndex, newZeroIndex, boardSize)
                h += delta
                board[zeroIndex], board[newZeroIndex] = board[newZeroIndex], board[zeroIndex]
                path.append(newZeroIndex)
                t = dfs(board, g + 1, bound, newZeroIndex)
                if t == -1:
                    return -1
                if t < minBound:
                    minBound = t
                path.pop()
                board[zeroIndex], board[newZeroIndex] = board[newZeroIndex], board[zeroIndex]
                h -= delta
        return minBound

    bound = manhattanDistance(board, boardSize)
    zeroIndex = board.index(0)
    while True:
        t = dfs(board, 0, bound, zeroIndex)
        if t == -1:
            return path
        if t == float('inf'):
            return None
        bound = t

if __name__ == "__main__":
    boardSize = 4
    board = generateRandomBoard(boardSize)
    print("Random Initial Board:", board)
    if isSolvable(board, boardSize):
        solutionPath = idaStar(board, boardSize)
        if solutionPath:
            print("\nSolution found:", solutionPath)
        else:
            print("\nNo solution found")
    else:
        print("\nThis puzzle is not solvable")

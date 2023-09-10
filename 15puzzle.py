import random

#Function to generate a random and solvable NxN puzzle board
def generateRandomBoard(boardSize):
    while True:
        board = [[0] * boardSize for _ in range(boardSize)]
        numbers = list(range(1, boardSize * boardSize))
        random.shuffle(numbers)
        for i in range(boardSize):
            for j in range(boardSize):
                if i == boardSize - 1 and j == boardSize - 1:
                    board[i][j] = 0
                else:
                    board[i][j] = numbers.pop()
        
        #Ensure that the generated board is solvable
        if isSolvable(board):
            return board

#Function to check if the current board is the goal state
def isGoal(board):
    boardSize = len(board)
    n = 0   #Initialize counter variable
    for i in range(boardSize):
        for j in range(boardSize):
            if board[i][j] != n:
                return False
            n = (n + 1) % (boardSize * boardSize)
    return True

#Function to calculate the Manhattan distance heuristic for a given board
def manhattanDistance(board):
    boardSize = len(board)
    distance = 0
    for i in range(boardSize):
        for j in range(boardSize):
            if board[i][j] == 0:
                continue
            targetVal = board[i][j] - 1
            targetX, targetY = divmod(targetVal, boardSize)
            distance += abs(i - targetX) + abs(j - targetY)
    return distance

#Function to incrementally update Manhattan distance after a move
def manhattanDelta(board, oldX, oldY, newX, newY, boardSize):
    delta = 0
    for (ox, oy, nx, ny) in [(oldX, oldY, newX, newY), (newX, newY, oldX, oldY)]:
        value = board[ox][oy]
        if value == 0:
            continue
        targetX, targetY = divmod(value - 1, boardSize)
        delta += abs(targetX - nx) + abs(targetY - ny) - abs(targetX - ox) - abs(targetY - oy)
    return delta

'''
If the total number of inversions is even, the puzzle is solvable.
If the total number of inversions is odd, the puzzle is unsolvable.
This is a proven property of the N-puzzle problem and is based on the idea of parity. 
In puzzles with an odd number of inversions, there is no way to transform the puzzle into a solved state by swapping tiles 
because each swap changes the parity (odd to even or even to odd), making it impossible to reach a solved 
state with an even number of inversions.
'''

#Function to check if a given board is solvable
def isSolvable(board):
    boardSize = len(board)
    inversionCount = 0
    flatBoard = [cell for row in board for cell in row if cell != 0]
    for i in range(len(flatBoard) - 1):
        for j in range(i + 1, len(flatBoard)):
            if flatBoard[i] > flatBoard[j]:
                inversionCount += 1
    return inversionCount % 2 == 0

#Function to perform the IDA* search algorithm to find a solution path
def idaStar(board):
    boardSize = len(board)
    path = []   #To store the solution path

    #Internal DFS function for IDA*
    def dfs(board, g, bound, zeroX, zeroY):
        h = manhattanDistance(board)  #Calculate heuristic
        f = g + h 
        #f = total cost, g = actual cost (incremented at each step), h = heuristic cost (computed using Manhattan distance)

        print("Current Board:") #Display the board at each step
        for row in board:
            print(row)

        #Bound check
        if f > bound:
            return f

        #Goal check
        if isGoal(board):
            return -1

        minBound = float('inf') #Initialize minBound

        #Explore adjacent moves (up, down, left, right)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newX, newY = zeroX + dx, zeroY + dy

            if 0 <= newX < boardSize and 0 <= newY < boardSize:
                delta = manhattanDelta(board, zeroX, zeroY, newX, newY, boardSize)
                h += delta

                #Swap the empty cell with the neighboring cell
                board[zeroX][zeroY], board[newX][newY] = board[newX][newY], board[zeroX][zeroY]
                path.append((newX, newY))

                #Recursively perform DFS
                t = dfs(board, g + 1, bound, newX, newY)

                #If a solution is found
                if t == -1:
                    return -1

                #Update the minimum bound for the next iteration
                if t < minBound:
                    minBound = t

                #Backtrack
                path.pop()
                board[zeroX][zeroY], board[newX][newY] = board[newX][newY], board[zeroX][zeroY]
                h -= delta

        return minBound

    bound = manhattanDistance(board)    #Start the IDA* algorithm
    zeroX, zeroY = 0, 0 #Position of zero (empty cell)

    for i in range(boardSize):
        for j in range(boardSize):
            if board[i][j] == 0:
                zeroX, zeroY = i, j

    while True:
        t = dfs(board, 0, bound, zeroX, zeroY)
        if t == -1:
            return path
        if t == float('inf'):
            return None
        bound = t

if __name__ == "__main__":
    boardSize = 4
    board = generateRandomBoard(boardSize)

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

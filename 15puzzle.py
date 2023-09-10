import random

def generateRandomBoard(boardSize): #Function to generate a random NxN puzzle board
    board = [[0] * boardSize for _ in range(boardSize)] #Initialize the board as a 2D list filled with zeros
    numbers = list(range(1, boardSize * boardSize)) #Create a list of numbers from 1 to (N*N - 1)
    random.shuffle(numbers) #Shuffle the numbers randomly
    for i in range(boardSize):  #Fill the board with shuffled numbers, leaving one cell as 0
        for j in range(boardSize):
            if i == boardSize - 1 and j == boardSize - 1:
                board[i][j] = 0
            else:
                board[i][j] = numbers.pop()
    return board

def isGoal(board):  #Function to check if the current board is the goal state
    boardSize = len(board)
    n = 1
    for i in range(boardSize):
        for j in range(boardSize):
            if n == boardSize * boardSize:
                return board[i][j] == 0
            if board[i][j] != n:
                return False
            n += 1

def manhattanDistance(board):   #Function to calculate the Manhattan distance heuristic for a given board
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

def manhattanDelta(board, oldX, oldY, newX, newY, boardSize):   #Function to incrementally update Manhattan distance after a move
    delta = 0
    for (x, y) in [(oldX, oldY), (newX, newY)]: #Calculate the delta for both old and new positions
        value = board[x][y]
        if value == 0:
            continue
        targetX, targetY = divmod(value - 1, boardSize)
        delta -= abs(x - targetX) + abs(y - targetY)
        targetX, targetY = divmod(value - 1, boardSize)
        delta += abs((x + newX - oldX) - targetX) + abs((y + newY - oldY) - targetY)
    return delta

'''
If the total number of inversions is even, the puzzle is solvable.
If the total number of inversions is odd, the puzzle is unsolvable.
This is a proven property of the N-puzzle problem and is based on the idea of parity. 
In puzzles with an odd number of inversions, there is no way to transform the puzzle into a solved state by swapping tiles 
because each swap changes the parity (odd to even or even to odd), making it impossible to reach a solved 
state with an even number of inversions.
'''

def isSolvable(board):  #Function to check if a given board is solvable
    boardSize = len(board)
    inversionCount = 0
    flatBoard = [cell for row in board for cell in row if cell != 0]    #Flatten the board and count inversions
    for i in range(len(flatBoard) - 1):
        for j in range(i + 1, len(flatBoard)):
            if flatBoard[i] > flatBoard[j]:
                inversionCount += 1
    return inversionCount % 2 == 0  #A board is solvable if the inversion count is even

def idaStar(board): #Function to perform the IDA* search algorithm to find a solution path
    boardSize = len(board)
    path = []
    visited = set()

    def dfs(board, g, bound, parentX, parentY): #Internal DFS function for IDA*
        h = manhattanDistance(board)
        f = g + h
        boardTuple = tuple(tuple(row) for row in board)

        print("Current Board:") #Display the board at each step
        for row in board:
            print(row)

        if boardTuple in visited:   #Avoid revisiting the same state
            return float('inf')

        visited.add(boardTuple)

        if f > bound:   #Bound check
            visited.remove(boardTuple)
            return f

        if isGoal(board):   #Goal check
            visited.remove(boardTuple)
            return -1

        minBound = float('inf')
        zeroX, zeroY = 0, 0

        for i in range(boardSize):  #Find the position of the zero (empty) cell
            for j in range(boardSize):
                if board[i][j] == 0:
                    zeroX, zeroY = i, j

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:   #Explore adjacent moves (up, down, left, right)
            newX, newY = zeroX + dx, zeroY + dy

            if 0 <= newX < boardSize and 0 <= newY < boardSize and (newX != parentX or newY != parentY):
                delta = manhattanDelta(board, zeroX, zeroY, newX, newY, boardSize)
                h += delta

                board[zeroX][zeroY], board[newX][newY] = board[newX][newY], board[zeroX][zeroY] #Swap the empty cell with the neighboring cell
                path.append((newX, newY))

                t = dfs(board, g + 1, bound, zeroX, zeroY)  #Recursively perform DFS

                if t == -1: #If a solution is found
                    return -1
                if t < minBound:    #Update the minimum bound for the next iteration
                    minBound = t

                path.pop()  #Backtrack
                board[zeroX][zeroY], board[newX][newY] = board[newX][newY], board[zeroX][zeroY]
                h -= delta

        visited.remove(boardTuple)
        return minBound

    bound = manhattanDistance(board)    #Start the IDA* algorithm
    while True:
        t = dfs(board, 0, bound, -1, -1)
        if t == -1:
            return path
        if t == float('inf'):
            return None
        bound = t

if __name__ == "__main__":  #Main code to execute the program
    boardSize = 4
    board = generateRandomBoard(boardSize)

    print("Random Initial Board:")
    for row in board:
        print(row)

    if isSolvable(board):   #Check if the board is solvable and solve it if it is
        solutionPath = idaStar(board)
        if solutionPath:
            print("\nSolution found:")
            for move in solutionPath:
                print(move)
        else:
            print("\nNo solution found")
    else:
        print("\nThis puzzle is not solvable")

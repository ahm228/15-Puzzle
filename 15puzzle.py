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
        for j in range(boardSize): #If n reaches the last value (N*N), the last cell should be 0
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
        for j in range(i+1, len(flatBoard)):
            if flatBoard[i] > flatBoard[j]:
                inversionCount += 1
    return inversionCount % 2 == 0  #A board is solvable if the inversion count is even

def idaStar(board): #Function to perform the IDA* search algorithm to find a solution path
    boardSize = len(board)
    path = []

    def dfs(board, g, bound, parentX, parentY):
        h = manhattanDistance(board)
        f = g + h

        # Display the board at each step
        print("Current Board:")
        for row in board:
            print(row)

        if f > bound:  # If the current cost exceeds the bound, backtrack
            return f

        if isGoal(board):  # If the board is the goal state, return -1 to indicate success
            return -1

        minBound = float('inf')
        zeroX, zeroY = 0, 0

        for i in range(boardSize):  # Find the position of the zero (empty) cell
            for j in range(boardSize):
                if board[i][j] == 0:
                    zeroX, zeroY = i, j

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Explore adjacent moves (up, down, left, right)
            newX, newY = zeroX + dx, zeroY + dy

            # Check if the new position is within bounds and not the parent position
            if 0 <= newX < boardSize and 0 <= newY < boardSize and (newX != parentX or newY != parentY):
                # Swap the empty cell with the neighboring cell
                board[zeroX][zeroY], board[newX][newY] = board[newX][newY], board[zeroX][zeroY]
                path.append((newX, newY))

                t = dfs(board, g + 1, bound, zeroX, zeroY)  # Recursively explore this move

                if t == -1:  # If a solution is found, return -1
                    return -1
                if t < minBound:  # Update the minimum bound for this branch
                    minBound = t

                path.pop()  # Backtrack by undoing the move
                board[zeroX][zeroY], board[newX][newY] = board[newX][newY], board[zeroX][zeroY]

        return minBound

    bound = manhattanDistance(board)
    while True:
        t = dfs(board, 0, bound, -1, -1)
        if t == -1:
            return path #Return the solution path
        if t == float('inf'):
            return None #No solution found
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

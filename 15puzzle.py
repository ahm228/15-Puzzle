import random

def generateRandomBoard(boardSize, numMoves=70):
    #Create a 1D list representing the board, initialize it with numbers from 1 to (boardSize*boardSize - 1) and append a 0 at the end
    board = list(range(1, boardSize * boardSize)) + [0]
    #Initialize the position of the zero (empty slot) on the board
    zeroIndex = boardSize * boardSize - 1

    #Perform numMoves number of random moves to shuffle the board
    for _ in range(numMoves):
        #Initialize an empty list to store the possible new positions for the zero tile
        possibleMoves = []
        
        #Loop through possible moves
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            #Calculate the current x, y coordinate of the zero based on its index in the 1D list
            x, y = divmod(zeroIndex, boardSize)
            #Calculate the new potential x, y coordinates for the zero
            newX, newY = x + dx, y + dy
            
            #Check if the new coordinates are within the bounds of the board
            if 0 <= newX < boardSize and 0 <= newY < boardSize:
                newZeroIndex = newX * boardSize + newY
                possibleMoves.append(newZeroIndex)

        #Randomly select one of the possible moves        
        newZeroIndex = random.choice(possibleMoves)
        #Swap the zero and the selected tile
        board[zeroIndex], board[newZeroIndex] = board[newZeroIndex], board[zeroIndex]
        zeroIndex = newZeroIndex

    return board

def printBoard(board, boardSize):
    for i in range(boardSize): 
        for j in range(boardSize):
            print(board[i * boardSize + j], end='\t')
        print()

#Function to check if the current board is in the goal state
def isGoal(board, boardSize):
    #Check if the last tile is 0
    if board[-1] != 0:
        return False
    
    #Loop through the rest of the board
    for i in range(boardSize * boardSize - 1):
        #Each tile should be at its correct position (tile n should be at index n - 1)
        if board[i] != i + 1:
            return False
        
    return True

#Function to calculate the Manhattan distance heuristic for a given board
def manhattanDistance(board, boardSize):
    distance = 0
    
    #Loop through all positions in the flattened 1D board
    for i in range(boardSize * boardSize):
        #Skip if the tile is 0
        if board[i] == 0:
            continue
        
        #Calculate the target position (goal state) of the current tile
        targetVal = board[i] - 1    #Target value is one less than the current value
        
        #Convert 1D index to 2D coordinates for current position
        x, y = divmod(i, boardSize) 

        #divmod function takes two numbers and returns a pair where the first element of the pair is the quotient, and the second is the remainder
        #Quotient represents the row number in the 2D board
        #Remainder represents the column number in the 2D board
        
        #Convert 1D index to 2D coordinates for target position
        targetX, targetY = divmod(targetVal, boardSize)
        
        #Add the Manhattan distance for the current tile to the total distance
        #Manhattan distance is calculated as the sum of the horizontal and vertical distances to the target position
        distance += abs(x - targetX) + abs(y - targetY)
    
    return distance

# Function to incrementally update Manhattan distance after making a move
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

# Updated DFS function
def dfs(board, g, bound, zeroIndex, h, path):  # Add 'path' as an argument
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
            t = dfs(board, g + 1, bound, newZeroIndex, h, path)  # Pass 'path' to the recursive call
            if t == -1:
                return -1
            if t < minBound:
                minBound = t
            path.pop()
            board[zeroIndex], board[newZeroIndex] = board[newZeroIndex], board[zeroIndex]
            h -= delta  # Revert the heuristic to its previous value
    return minBound

# Updated IDA* function
def idaStar(board, boardSize):
    path = []
    bound = manhattanDistance(board, boardSize)
    h = bound  # Initialize h to the initial full Manhattan distance
    zeroIndex = board.index(0)
    while True:
        t = dfs(board, 0, bound, zeroIndex, h, path)  # Pass 'path' as an argument
        if t == -1:
            return path
        bound = t


if __name__ == "__main__":
    while True:  #Keep asking for input until a valid board size is entered
        try:
            boardSize = int(input("Enter the board size (N for NxN): "))
            
            #Check if boardSize is greater than 1
            if boardSize <= 1:
                print("The board size must be greater than 1.")
                continue

            break  #Exit the loop if the input is valid

        except ValueError:  #Handle the case where input cannot be converted to an integer
            print("Invalid input. Please enter an integer.")

    board = generateRandomBoard(boardSize)

    print("Random Initial Board:")
    printBoard(board, boardSize)
    
    solutionPath = idaStar(board, boardSize)
    #Each entry in the solutionPath represents the new position of the zero tile after making a move
    
    if solutionPath:
        print("\nSolution found:", solutionPath)
    else:
        print("\nNo solution found")

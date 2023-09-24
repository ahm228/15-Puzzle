import random

def generateRandomBoard(boardSize, numMoves=70):

    #Create a 1D list representing the board, initialize it with numbers from 1 to (boardSize*boardSize - 1) and append a 0 at the end
    board = list(range(1, boardSize * boardSize)) + [0]
    zeroIndex = boardSize * boardSize - 1

    #Perform numMoves number of random moves to shuffle the board
    for _ in range(numMoves):
        possibleMoves = []  #Initialize an empty list to store the possible new positions for the zero tile
        
        #Loop through possible moves
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = divmod(zeroIndex, boardSize) #Calculate the current x, y coordinate of the zero based on its index in the 1D list
            newX, newY = x + dx, y + dy #Calculate the new potential x, y coordinates for the zero
            
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
    if board[-1] != 0:  #Check if the last tile is 0
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
        
        #divmod function takes two numbers and returns a pair where the first element of the pair is the quotient, and the second is the remainder
        #Quotient represents the row number in the 2D board
        #Remainder represents the column number in the 2D board

        #Convert 1D index to 2D coordinates for current position
        x, y = divmod(i, boardSize) 
        
        #Convert 1D index to 2D coordinates for target position
        targetX, targetY = divmod(targetVal, boardSize)
        
        #Add the Manhattan distance for the current tile to the total distance
        #Manhattan distance is calculated as the sum of the horizontal and vertical distances to the target position
        distance += abs(x - targetX) + abs(y - targetY)
    
    return distance

#Function to incrementally update Manhattan distance after making a move
def manhattanDelta(board, oldIndex, newIndex, boardSize):
    delta = 0   #Initialize a variable delta to store the change in Manhattan distance

    #Loop through both old and new positions of the moved tile
    #Use this loop to compute the delta for both the tile that's moving to the zero tile
    #and the zero tile itself that's moving to the tile's spot
    for oi, ni in [(oldIndex, newIndex), (newIndex, oldIndex)]:
        value = board[oi]   #Retrieve the value at the old position
        
        if value == 0: #Skip if the tile is the zero tile
            continue

        #Calculate the target position of the tile based on its ideal position in the solved board
        targetVal = value - 1

        x, y = divmod(oi, boardSize)
        targetX, targetY = divmod(targetVal, boardSize)
        newX, newY = divmod(ni, boardSize)

        #Update the change in Manhattan distance
        delta += abs(targetX - newX) + abs(targetY - newY) - abs(targetX - x) - abs(targetY - y)

    return delta

def dfs(board, g, bound, zeroIndex, h, path):
    #Calculate the total estimated cost f for the current board state
    f = g + h   #g = actual cost, h = heuristic cost (Manhattan distance)

    #If the estimated cost exceeds the current bound, return the estimated cost
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
            h += delta  #Update the heuristic cost

            board[zeroIndex], board[newZeroIndex] = board[newZeroIndex], board[zeroIndex]
            path.append(newZeroIndex)

            #Recursively call DFS with the new board state
            t = dfs(board, g + 1, bound, newZeroIndex, h, path)

            if t == -1: #If a solution is found, return -1 to indicate success
                return -1
            
            if t < minBound:    #Update minBound if the estimated cost is lower
                minBound = t

            #Backtrack
            path.pop()
            board[zeroIndex], board[newZeroIndex] = board[newZeroIndex], board[zeroIndex]
            h -= delta

    return minBound

def idaStar(board, boardSize):
    path = []   #Initialize an empty list to keep track of the solution path
    bound = manhattanDistance(board, boardSize) 
    h = bound
    zeroIndex = board.index(0)

    while True:
        #Perform depth-first search up to the current bound
        t = dfs(board, 0, bound, zeroIndex, h, path)
        
        if t == -1: #If a solution is found, break the loop and return the path
            return path
        
        bound = t   #Update the bound for the next iteration


if __name__ == "__main__":
    while True:
        try:
            boardSize = int(input("Enter the board size (N for NxN): "))
            
            if boardSize <= 1:
                print("The board size must be greater than 1.")
                continue

            break

        except ValueError:
            print("Invalid input. Please enter an integer.")

    board = generateRandomBoard(boardSize)

    print("Random Initial Board:")
    printBoard(board, boardSize)
    
    solutionPath = idaStar(board, boardSize)
    
    if solutionPath:
        print("\nSolution found:", solutionPath)
    else:
        print("\nNo solution found")

import random

# Function to generate a random and solvable NxN puzzle board
def generateRandomBoard(boardSize):
    # Continue trying until a solvable board is found
    while True:
        # Initialize a 1D board of length boardSize * boardSize with zeros
        board = [0] * (boardSize * boardSize)
        
        # Create a list of numbers from 1 up to (boardSize * boardSize) - 1
        # These numbers represent the tiles that will go on the board
        numbers = list(range(1, boardSize * boardSize))
        
        # Shuffle the list of numbers to randomize the initial state of the board
        random.shuffle(numbers)
        
        # Fill in the board with the shuffled numbers
        for i in range(boardSize * boardSize - 1):
            board[i] = numbers.pop()
        
        # Set the last position on the board as empty (0)
        board[-1] = 0

        # Check if the generated board is solvable
        if isSolvable(board, boardSize):
            # If it is solvable, return the board
            return board
        
def printBoard(board, boardSize):
    for i in range(boardSize): 
        for j in range(boardSize):
            print(board[i * boardSize + j], end='\t')
        print()

# Function to check if the current board is in the goal state.
def isGoal(board, boardSize):
    # Check if the last tile is 0 (the empty tile should be in the final position)
    if board[-1] != 0:
        return False
    
    # Loop through the rest of the board
    for i in range(boardSize * boardSize - 1):
        # Each tile should be at its correct position (i.e., tile numbered 'n' should be at index 'n - 1')
        if board[i] != i + 1:
            return False
    
    # If the function hasn't returned False yet, the board is in the goal state
    return True

# Function to calculate the Manhattan distance heuristic for a given board
def manhattanDistance(board, boardSize):
    # Initialize the variable that will store the total Manhattan distance for the board
    distance = 0
    
    # Loop through all positions in the flattened 1D board
    for i in range(boardSize * boardSize):
        # Skip if the tile is empty (value is 0)
        if board[i] == 0:
            continue
        
        # Calculate the target position (goal state) of the current tile
        targetVal = board[i] - 1  # Target value is one less than the current value
        
        # Convert 1D index to 2D coordinates for current position
        x, y = divmod(i, boardSize)  # x and y are row and column coordinates, respectively
        
        # Convert 1D index to 2D coordinates for target position
        targetX, targetY = divmod(targetVal, boardSize)  # targetX and targetY are row and column coordinates, respectively
        
        # Add the Manhattan distance for the current tile to the total distance
        # Manhattan distance is calculated as the sum of the horizontal and vertical distances to the target position
        distance += abs(x - targetX) + abs(y - targetY)
    
    # Return the total Manhattan distance for the board
    return distance

# Function to incrementally update Manhattan distance after making a move
def manhattanDelta(board, oldIndex, newIndex, boardSize):
    # Initialize the delta variable, which will store the change in Manhattan distance
    delta = 0
    
    # Loop through both old and new positions of the moved tile
    for oi, ni in [(oldIndex, newIndex), (newIndex, oldIndex)]:
        # Retrieve the value at the old position
        value = board[oi]
        
        # Skip if the tile is empty (value is 0)
        if value == 0:
            continue
        
        # Calculate the target position of the tile
        targetVal = value - 1
        x, y = divmod(oi, boardSize)  # Current x and y coordinates
        targetX, targetY = divmod(targetVal, boardSize)  # Target x and y coordinates
        newX, newY = divmod(ni, boardSize)  # New x and y coordinates
        
        # Update the delta (change in Manhattan distance)
        # Add the Manhattan distance from the new position to the target position
        # Subtract the Manhattan distance from the old position to the target position
        delta += abs(targetX - newX) + abs(targetY - newY) - abs(targetX - x) - abs(targetY - y)
    
    # Return the calculated delta value
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
    # Initialize the inversion counter to 0
    inversionCount = 0
    
    # Loop through the board to count inversions
    for i in range(len(board) - 1):  # Iterate from the first element to the second-to-last element
        if board[i] == 0:  # Skip the zero tile
            continue
       
        for j in range(i + 1, len(board)):  # Iterate from the element after i to the last element
            if board[j] == 0:  # Skip the zero tile
                continue
            
            # Check if an inversion exists, i.e., a larger number appears before a smaller number
            if board[i] > board[j]:
                inversionCount += 1  # Increment the inversion count
    
    # For a board to be solvable, the number of inversions must be even
    return inversionCount % 2 == 0

#Function to perform the IDA* search algorithm to find a solution path
def idaStar(board, boardSize):
    path = []

    def dfs(board, g, bound, zeroIndex):
        h = manhattanDistance(board, boardSize)
        f = g + h

        #f = total cost, g = actual cost (incremented at each step), h = heuristic cost (computed using Manhattan distance)
        if f > bound: #If the estimated cost exceeds the current bound, return the estimated cost
            return f
        
        if isGoal(board, boardSize): #Check if the current board is the goal state
            return -1
        
        minBound = float('inf') #Initialize minBound to an arbitrarily large number
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]: #Explore adjacent moves (up, down, left, right)
            x, y = divmod(zeroIndex, boardSize) #Get the current x, y coordinates of the zero (empty cell)
            newX, newY = x + dx, y + dy #Calculate new coordinates for zero after mov
            
            if 0 <= newX < boardSize and 0 <= newY < boardSize: #Check if new coordinates are valid (within bounds)
                newZeroIndex = newX * boardSize + newY #Calculate new linear index for zero
                delta = manhattanDelta(board, zeroIndex, newZeroIndex, boardSize) #Calculate how this move will affect the Manhattan distance
                h += delta #Add the delta to the heuristic
                board[zeroIndex], board[newZeroIndex] = board[newZeroIndex], board[zeroIndex] #Perform the move (swap zero and the adjacent cell)
                path.append(newZeroIndex) #Add this move to the path
                t = dfs(board, g + 1, bound, newZeroIndex) #Recursively call DFS with new board state
                
                if t == -1: #Goal is found
                    return -1
                
                if t < minBound: #Update the minimum bound needed for next iteration
                    minBound = t
                path.pop() #Backtrack, undo the move and remove the last added move in path
                board[zeroIndex], board[newZeroIndex] = board[newZeroIndex], board[zeroIndex]
                h -= delta #Subtract the delta from the heuristic to backtrack

        return minBound #Return the minimum bound for the next iteration

    bound = manhattanDistance(board, boardSize)
    zeroIndex = board.index(0)

    #Enter an infinite loop, will break when solution is found or proven unsolvable
    while True:
        t = dfs(board, 0, bound, zeroIndex) #Call the DFS function to explore nodes up to the current bound
        
        if t == -1:
            return path
        
        if t == float('inf'):
            return None
        
        bound = t #Update the bound for the next round of IDA*

if __name__ == "__main__":
    boardSize = 4 #consider taking this as an input, allow for board sizes other than 4 x 4
    board = generateRandomBoard(boardSize)

    print("Random Initial Board:")
    printBoard(board, boardSize)
    
    if isSolvable(board, boardSize):
        solutionPath = idaStar(board, boardSize)
        
        if solutionPath:
            print("\nSolution found:", solutionPath)
        
        else:
            print("\nNo solution found")

    else:
        print("\nThis puzzle is not solvable")

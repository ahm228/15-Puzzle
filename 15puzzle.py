import random

def generateRandomBoard(N):
    board = [[0] * N for _ in range(N)] #Create an empty N x N game board filled with zeros
    numbers = list(range(1, N * N)) #Generate a list of numbers from 1 to N*N - 1 (excluding 0)
    random.shuffle(numbers) #Shuffle the list of numbers randomly to create a random puzzle configuration
    numbers_iter = iter(numbers)    #Create an iterator for the shuffled numbers

    for i in range(N):  #Populate the game board with shuffled numbers, leaving one cell empty (0)
        for j in range(N):  #If we are at the last cell, set it as an empty cell (0)
            if (i == N - 1) and (j == N - 1):
                board[i][j] = 0  # Empty cell
            else:   #Place the next shuffled number on the board
                board[i][j] = next(numbers_iter)

    return board #Return the randomly generated game board

def isGoal(board): #Define a function to check if a given board is in a goal state
    N = len(board)  #Get the size of the board (N x N)
    n = 1   #Initialize a variable to keep track of the expected value
    for i in range(N):
        for j in range(N):  #Check if the current cell value is equal to the expected value
            if board[i][j] != n:
                return False    #If not, return False
            n += 1  #Increment the expected value
            if n == N * N:
                return True #If all values are in order, return True

def manhattanDistance(board):  #Define a function to calculate the Manhattan distance heuristic for a given board
    N = len(board)  # Get the size of the board (N x N)
    distance = 0    # Initialize the total Manhattan distance
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                continue    #Skip the empty cell
            targetVal = board[i][j] - 1    #Calculate the target value for the cell
            targetX, targetY = divmod(targetVal, N)  #Calculate the target position
            distance += abs(i - targetX) + abs(j - targetY)   #Calculate Manhattan distance
    return distance

def idaStar(board):    #Define the IDA* (Iterative Deepening A*) search algorithm
    N = len(board)  #Get the size of the board (N x N)
    path = []   #Initialize a list to store the solution path
    
    def dfs(board, g, bound, path): #Define a depth-first search function with a depth limit (bound)
        h = manhattanDistance(board)   #Calculate the Manhattan distance heuristic
        f = g + h   #Calculate the evaluation function value (f = g + h)
        if f > bound:
            return f    #If f is greater than the current bound, prune this branch
        if isGoal(board):
            return -1   #If the board is in the goal state, return -1 to signal success
        minBound = float('inf')    #Initialize the minimum bound for this branch
        
        zeroX, zeroY = 0, 0   #Initialize the coordinates of the empty cell
        for i in range(N):
            for j in range(N):
                if board[i][j] == 0:
                    zeroX, zeroY = i, j   #Find the coordinates of the empty cell
                    
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:   #Try moving the empty cell in four possible directions: right, down, left, up
            newX, newY = zeroX + dx, zeroY + dy #Calculate the new position
            if 0 <= newX < N and 0 <= newY < N:   #Swap the values between the empty cell and the neighboring cell
                board[zeroX][zeroY], board[newX][newY] = board[newX][newY], board[zeroX][zeroY]
                path.append((newX, newY)) #Add the move to the path
                
                t = dfs(board, g + 1, bound, path)  #Recursively explore this move with an increased depth (g + 1)
                
                if t == -1:
                    return -1   #If the goal is found in this branch, return -1
                if t < minBound:
                    minBound = t   #Update the minimum bound
                
                path.pop()  #Remove the move from the path (backtrack)
                board[zeroX][zeroY], board[newX][newY] = board[newX][newY], board[zeroX][zeroY] #Undo the move
        
        return minBound    #Return the minimum bound for this branch

    bound = manhattanDistance(board)   #Initialize the bound with the Manhattan distance heuristic
    while True:
        t = dfs(board, 0, bound, path)  #Perform iterative deepening search
        if t == -1:
            return path #If a solution is found, return the solution path
        if t == float('inf'):
            return None #If no solution is found, return None

if __name__ == "__main__":
    N = 4   #Specify the size of the board (N x N)
    board = generateRandomBoard(N)  #Generate a random starting board

    print("Random Initial Board:")
    for row in board:
        print(row)
    
    solutionPath = idaStar(board)   #Run the IDA* algorithm to find a solution path
    if solutionPath:    #Display the result
        print("\nSolution found:")
        for move in solutionPath:
            print(move) #Print each move in the solution path
    else:
        print("\nNo solution found")    #Print a message if no solution is found

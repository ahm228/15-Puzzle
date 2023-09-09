def is_goal(board): #Define a function to check if a given board is in a goal state
    N = len(board)  #Get the size of the board (N x N)
    n = 1   #Initialize a variable to keep track of the expected value
    for i in range(N):
        for j in range(N):  #Check if the current cell value is equal to the expected value
            if board[i][j] != n:
                return False    #If not, return False
            n += 1  #Increment the expected value
            if n == N * N:
                return True #If all values are in order, return True

def manhattan_distance(board):  #Define a function to calculate the Manhattan distance heuristic for a given board
    N = len(board)  # Get the size of the board (N x N)
    distance = 0    # Initialize the total Manhattan distance
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                continue    #Skip the empty cell
            target_val = board[i][j] - 1    #Calculate the target value for the cell
            target_x, target_y = divmod(target_val, N)  #Calculate the target position
            distance += abs(i - target_x) + abs(j - target_y)   #Calculate Manhattan distance
    return distance

def ida_star(board):    #Define the IDA* (Iterative Deepening A*) search algorithm
    N = len(board)  #Get the size of the board (N x N)
    path = []   #Initialize a list to store the solution path
    
    def dfs(board, g, bound, path): #Define a depth-first search function with a depth limit (bound)
        h = manhattan_distance(board)   #Calculate the Manhattan distance heuristic
        f = g + h   #Calculate the evaluation function value (f = g + h)
        if f > bound:
            return f    #If f is greater than the current bound, prune this branch
        if is_goal(board):
            return -1   #If the board is in the goal state, return -1 to signal success
        min_bound = float('inf')    #Initialize the minimum bound for this branch
        
        zero_x, zero_y = 0, 0   #Initialize the coordinates of the empty cell
        for i in range(N):
            for j in range(N):
                if board[i][j] == 0:
                    zero_x, zero_y = i, j   #Find the coordinates of the empty cell
                    
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:   #Try moving the empty cell in four possible directions: right, down, left, up
            new_x, new_y = zero_x + dx, zero_y + dy #Calculate the new position
            if 0 <= new_x < N and 0 <= new_y < N:   #Swap the values between the empty cell and the neighboring cell
                board[zero_x][zero_y], board[new_x][new_y] = board[new_x][new_y], board[zero_x][zero_y]
                path.append((new_x, new_y)) #Add the move to the path
                
                t = dfs(board, g + 1, bound, path)  #Recursively explore this move with an increased depth (g + 1)
                
                if t == -1:
                    return -1   #If the goal is found in this branch, return -1
                if t < min_bound:
                    min_bound = t   #Update the minimum bound
                
                path.pop()  #Remove the move from the path (backtrack)
                board[zero_x][zero_y], board[new_x][new_y] = board[new_x][new_y], board[zero_x][zero_y] #Undo the move
        
        return min_bound    #Return the minimum bound for this branch

    bound = manhattan_distance(board)   #Initialize the bound with the Manhattan distance heuristic
    while True:
        t = dfs(board, 0, bound, path)  #Perform iterative deepening search
        if t == -1:
            return path #If a solution is found, return the solution path
        if t == float('inf'):
            return None #If no solution is found, return None

if __name__ == "__main__":  #Main program entry point
    board = [   #Define the initial state of the board
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 7, 11],
        [13, 14, 15, 12]
    ]
    
    solution_path = ida_star(board) #Run the IDA* algorithm to find a solution path
    if solution_path:   #Display the result
        print("Solution found:")
        for move in solution_path:
            print(move) #Print each move in the solution path
    else:
        print("No solution found")  #Print a message if no solution is found

N-Puzzle Solver using IDA* Algorithm

    This Python script solves the N-Puzzle problem using the IDA* (Iterative-Deepening A*) algorithm. It employs Manhattan distance as a heuristic to estimate the cost of reaching the goal state from the current state. The code is capable of generating random, solvable N x N boards and finding the solution path.
    
    Functions
        generateRandomBoard(boardSize)
            This function generates a random solvable N x N puzzle board. It uses a while loop to continue generating boards until it finds one that is solvable.
        
        isGoal(board)
            This function checks if the current board state is the goal state by iterating through the board's elements and comparing them with the expected goal state.

        manhattanDistance(board)
            This function calculates the Manhattan distance for a given board state. Manhattan distance is the sum of the absolute differences between each tile's current position and its position in the goal state.

        manhattanDelta(board, oldX, oldY, newX, newY, boardSize)
            This function incrementally updates the Manhattan distance after each move to improve the performance of the heuristic calculation.

        isSolvable(board)
            This function checks if a given board is solvable by counting the number of inversions in the board. An inversion is a pair of tiles that are in the wrong order relative to their positions in the goal state.

        idaStar(board)
            This function performs the IDA* search algorithm to find the solution path for a given board. It explores different states of the board by moving the empty tile (0) and updates the cost (f) of each state to determine the most promising path to the goal state.

    Usage

        Run the script.
        The initial random board will be displayed.
        The script will output each board state as it iterates through the IDA* algorithm.
        If a solution is found, the solution path will be displayed.

    Example Output

        Random Initial Board:
        [12, 5, 8, 3]
        [7, 15, 1, 9]
        [2, 10, 11, 14]
        [4, 13, 6, 0]

        Solution found:
        [(3, 2), (2, 2), (1, 2), ...]

    or

        Random Initial Board:
        [7, 2, 3, 8]
        [9, 5, 1, 4]
        [0, 15, 14, 10]
        [13, 11, 12, 6]

        This puzzle is not solvable

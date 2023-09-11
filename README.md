N-Puzzle Solver using IDA* Algorithm

    This Python script solves the N-Puzzle problem using the IDA* (Iterative-Deepening A*) algorithm. The program employs a 1D list to represent the board state and utilizes an efficient method to update the Manhattan distance after each move. It is capable of generating random, solvable N x N boards and finding the solution path.

    Functions

        generateRandomBoard(boardSize)
            This function generates a random solvable N x N puzzle board. It uses a while loop to continue generating boards until it finds one that is solvable.

        isGoal(board, boardSize)
            This function checks if the current board state is the goal state. It ensures that the last tile is zero and that the rest of the tiles are in ascending order.

        manhattanDistance(board, boardSize)
            This function calculates the Manhattan distance for a given board state. Manhattan distance is the sum of the absolute differences between each tile's current position and its position in the goal state.

        manhattanDelta(board, oldIndex, newIndex, boardSize)
            This function incrementally updates the Manhattan distance after each move. This improves the efficiency of heuristic calculation.

        isSolvable(board, boardSize)
            This function checks if a given board is solvable by counting the number of inversions in the board. An inversion is a pair of tiles that are in the wrong order relative to their positions in the goal state.

        idaStar(board, boardSize)
            This function performs the IDA* search algorithm to find the solution path for a given board. It explores different states of the board by swapping the empty tile (0) with adjacent tiles and updates the bound based on the heuristic and cost-to-come.

    Usage

        Run the script.
        The initial random board will be displayed.
        The script will output the current board state at each step as it iterates through the IDA* algorithm.
        If a solution is found, the solution path will be displayed.

    Example Output
    
    Random Initial Board:
    0	12	5	8	
    7	15	1	3	
    2	10	11	9	
    4	13	14	6	

    Solution found:
    [(3, 2), (2, 2), (1, 2), ...]

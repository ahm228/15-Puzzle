Overview

15puzzle.py is a Python script that implements the classic 15-puzzle game. It uses the Iterative Deepening A* (IDA*) algorithm to find a solution to a given board state. The board is represented as a 1D list and shuffled randomly at the beginning of the game.

Features

    Randomly generates an initial board of NxN size.
    Uses the Manhattan distance heuristic for optimizing the IDA* algorithm.
    Displays the initial board and the solution path.

Dependencies

    Python 3.x
    random module (built-in)

Usage

    Running the Script

    To execute the script, simply run the following command in your terminal:
    python 15puzzle.py
    You will be prompted to enter the board size (N for an NxN board).

Example Output

    Enter the board size (N for NxN): 4
    Random Initial Board:
    1	2	3	4	
    5	6	7	8	
    9	10	11	12	
    13	14	15	0	

    Solution found: [14, 15, ...]

Functions

    generateRandomBoard(boardSize, numMoves=70)
    Generates a random board by making numMoves random moves on a solved board.

    printBoard(board, boardSize)
    Displays the board in a human-readable format.

    isGoal(board, boardSize)
    Checks if the current board is in the goal state.

    manhattanDistance(board, boardSize)
    Calculates the Manhattan distance heuristic for a given board.

    manhattanDelta(board, oldIndex, newIndex, boardSize)
    Calculates the change in Manhattan distance after a single move.

    dfs(board, g, bound, zeroIndex, h, path)
    Performs a depth-first search up to a certain bound, updating the path list with the solution steps if found.

    idaStar(board, boardSize)
    Uses IDA* algorithm to find a solution path for the puzzle.

Limitations

    The program's performance might decline for larger board sizes.

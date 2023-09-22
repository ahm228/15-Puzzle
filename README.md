Overview

The 15puzzle.py script is an implementation of the classic 15-puzzle (or N-puzzle) game using Iterative Deepening A* (IDA*) for solving the puzzle. The 15-puzzle is a sliding puzzle that consists of a frame of numbered square tiles in random order with one tile missing.
Features

    Generate a random NxN puzzle board.
    Display the board in the terminal.
    Check if a given board is in the goal state.
    Calculate the Manhattan Distance as a heuristic for the A* search algorithm.
    Solve the puzzle using the IDA* search algorithm.

Functions
generateRandomBoard(boardSize, numMoves=70)

    Generates a random board based on the given board size.
    Optionally, you can also specify the number of random moves to shuffle the board.

printBoard(board, boardSize)

    Prints the board to the console.

isGoal(board, boardSize)

    Checks if the current board is in the goal state.

manhattanDistance(board, boardSize)

    Computes the Manhattan Distance for a given board as the heuristic for the A* search algorithm.

manhattanDelta(board, oldIndex, newIndex, boardSize)

    Incrementally updates the Manhattan Distance heuristic after making a move.

idaStar(board, boardSize)

    Solves the puzzle board using the IDA* search algorithm and returns the solution path as a list of zero tile moves.

Usage

    Run python 15puzzle.py
    Enter the board size when prompted (e.g., 4 for a 4x4 board, which is the classic 15-puzzle).
    The script will generate a random board, display it, and then solve it using IDA*.
    The solution, if found, will be displayed as a list of zero tile positions.

Example
    Enter the board size (N for NxN): 4
    Random Initial Board:
    1	2	3	4	
    5	6	7	8	
    9	10	11	12	
    13	14	15	0	

    Solution found: [14, 15, 11, 10, 9, 13, 14, 15, 11, 10, 9, 8, 12, 13, 14, 15]

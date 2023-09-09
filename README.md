Overview

The 15puzzle.py program is designed to solve the 15-puzzle game, which is a sliding puzzle that consists of a frame of numbered square tiles in random order with one tile missing. The program uses the Iterative-Deepening A* (IDA*) search algorithm and includes features to check the solvability of the puzzle.
Features

    Generates a random puzzle board of size NxN.
    Checks if the puzzle is solvable.
    Uses Manhattan distance heuristic for optimization.
    Solves the puzzle using the IDA* algorithm.

Dependencies

    Python 3.x
    random module (Built-in)

How to Run

    Make sure Python 3.x is installed.

    Run the script from your terminal:
    python 15puzzle.py

Functions

generateRandomBoard(boardSize)
Generates a random NxN board for the puzzle.

isGoal(board)
Checks if the board is in a goal state.

manhattanDistance(board)
Computes the Manhattan distance heuristic for the given board state.

isSolvable(board)
Checks if the puzzle is solvable based on the inversion count.

idaStar(board)
Solves the puzzle using the IDA* algorithm and returns the solution path if exists.

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

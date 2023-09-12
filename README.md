NxN Puzzle Solver with IDA* Algorithm
Description

This Python script is a solver for the NxN puzzle game using the Iterative-Deepening A* (IDA*) search algorithm. The puzzle consists of an NxN grid of tiles labeled from 1 to N*N - 1, with one tile missing (represented as 0). The puzzle is solved when all tiles are in ascending order, ending with the missing tile at the bottom-right corner.
Features

    Generate a random and solvable NxN board
    Display the board in a readable format
    Check if a board is in its goal state
    Calculate the Manhattan distance heuristic for a board
    Incrementally update Manhattan distance when making a move
    Check if a given board is solvable using inversion count
    Solve the puzzle using the IDA* algorithm

Requirements

    Python 3.x
    No additional libraries are required

How to Use

    Clone the repository or download the Python script.
    Run the script: python <script-name>.py
    Input the board size when prompted (N for an NxN board).
    The script will generate a random solvable board, display it, and then find a solution path if one exists.

Code Structure
Functions

    generateRandomBoard(boardSize): Generates a random and solvable board of size NxN.
    printBoard(board, boardSize): Prints the board in a readable format.
    isGoal(board, boardSize): Checks if the board is in the goal state.
    manhattanDistance(board, boardSize): Calculates the Manhattan distance heuristic for a board.
    manhattanDelta(board, oldIndex, newIndex, boardSize): Incrementally updates the Manhattan distance when making a move.
    isSolvable(board, boardSize): Checks if a given board is solvable.
    idaStar(board, boardSize): Main function to perform the IDA* algorithm.

Algorithms

    IDA* Algorithm: Used for solving the puzzle.
    Manhattan Distance: Used as a heuristic to estimate the distance to the goal state.

Limitations

    The program may take a long time to find the solution for large board sizes.

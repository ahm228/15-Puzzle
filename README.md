15-Puzzle Solver

This Python program, 15puzzle.py, is a simple implementation of a solver for the classic 15-puzzle game. The 15-puzzle is a sliding puzzle that consists of a 4x4 grid with 15 numbered tiles and one blank space. The objective is to rearrange the tiles by sliding them into the blank space to achieve a specific goal state.
How to Use

    Make sure you have Python 3 installed on your system.

    Download the 15puzzle.py file.

    Run the program using the following command:
    python 15puzzle.py

    The program will generate a random initial board configuration and attempt to solve it using the IDA* (Iterative Deepening A*) algorithm. If a solution is found, it will display the steps to solve the puzzle; otherwise, it will indicate that no solution was found.

Functions

generateRandomBoard(N)
This function generates a random initial board configuration for the 15-puzzle. It takes a single argument N, which specifies the size of the puzzle (4x4 in this case). It returns a 4x4 list representing the board.

isGoal(board)
This function checks if a given board is in the goal state, where all tiles are in ascending order from left to right, top to bottom, with the blank space at the bottom-right corner.

manhattanDistance(board)
This function calculates the Manhattan distance heuristic for a given board configuration. The Manhattan distance is the sum of the distances of each tile from its goal position.

idaStar(board)
This function implements the IDA* algorithm to solve the 15-puzzle. It uses depth-first search (DFS) with a heuristic to find the optimal solution. If a solution is found, it returns a list of moves to solve the puzzle; otherwise, it returns None to indicate that no solution was found.

Main Execution
The program's main execution begins when __name__ is equal to "__main__". It generates a random initial board, displays it, and then attempts to solve the puzzle using the idaStar function. If a solution is found, it displays the sequence of moves to solve the puzzle; otherwise, it informs the user that no solution was found.

Example execution

Random Initial Board:
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13, 14, 15, 0]

Solution found:
(3, 3)
(3, 2)
(3, 1)
(3, 0)
(2, 0)
(2, 1)
(2, 2)
(2, 3)
(1, 3)
(1, 2)
(1, 1)
(1, 0)
(0, 0)
(0, 1)
(0, 2)
(0, 3)

In this example, the program generates a random initial board configuration for the 15-puzzle and then successfully finds a solution using the IDA* algorithm. It displays the initial board and the sequence of moves required to solve the puzzle. Each move is represented as a pair of coordinates (row, column) indicating the tile to be moved into the blank space. The goal state is achieved when the board looks like this:
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13, 14, 15, 0]

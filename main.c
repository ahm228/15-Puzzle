#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N 4  // 4x4 board for the 15-puzzle

typedef struct {
    int board[N][N];
    int zero_x;
    int zero_y;
} State;

// Function to calculate Manhattan distance
int manhattan_distance(State *state) {
    int distance = 0;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            if (state->board[i][j] == 0) continue;
            int target_val = state->board[i][j] - 1;
            int target_x = target_val / N;
            int target_y = target_val % N;
            distance += abs(i - target_x) + abs(j - target_y);
        }
    }
    return distance;
}

// Function to check if state is the goal state
int is_goal(State *state) {
    int val = 1;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            if (state->board[i][j] != val) return 0;
            ++val;
            if (val == N * N) return 1;
        }
    }
    return 0;
}

// Function to copy state
void copy_state(State *dest, State *src) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            dest->board[i][j] = src->board[i][j];
        }
    }
    dest->zero_x = src->zero_x;
    dest->zero_y = src->zero_y;
}

int dfs(State *state, int g, int bound) {
    int h = manhattan_distance(state);
    int f = g + h;
    if (f > bound) return f;
    if (is_goal(state)) return -1;

    int min_bound = 1000000;  // a large number
    for (int dx = -1; dx <= 1; ++dx) {
        for (int dy = -1; dy <= 1; ++dy) {
            // Skip diagonals and 0-moves
            if (abs(dx) + abs(dy) != 1) continue;

            int new_x = state->zero_x + dx;
            int new_y = state->zero_y + dy;
            if (new_x >= 0 && new_x < N && new_y >= 0 && new_y < N) {
                // Swap
                int temp = state->board[state->zero_x][state->zero_y];
                state->board[state->zero_x][state->zero_y] = state->board[new_x][new_y];
                state->board[new_x][new_y] = temp;
                
                state->zero_x = new_x;
                state->zero_y = new_y;

                int t = dfs(state, g + 1, bound);

                if (t == -1) return -1;
                if (t < min_bound) min_bound = t;

                // Undo swap
                state->board[new_x][new_y] = state->board[state->zero_x][state->zero_y];
                state->board[state->zero_x][state->zero_y] = temp;

                state->zero_x -= dx;
                state->zero_y -= dy;
            }
        }
    }
    return min_bound;
}

int ida_star(State *initial_state) {
    int bound = manhattan_distance(initial_state);
    while (1) {
        int t = dfs(initial_state, 0, bound);
        if (t == -1) return 1;  // found
        if (t == 1000000) return 0;  // not found
        bound = t;
    }
}

int main() {
    State initial_state = {
        .board = {
            {1, 2, 3, 4},
            {5, 6, 0, 8},
            {9, 10, 7, 11},
            {13, 14, 15, 12}
        },
        .zero_x = 1,
        .zero_y = 2
    };

    if (ida_star(&initial_state)) {
        printf("Solution found!\n");
    } else {
        printf("No solution found.\n");
    }
    return 0;
}

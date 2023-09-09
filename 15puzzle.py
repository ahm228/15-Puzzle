from typing import List, Tuple

def is_goal(board: List[List[int]]) -> bool:
    N = len(board)
    n = 1
    for i in range(N):
        for j in range(N):
            if board[i][j] != n:
                return False
            n += 1
            if n == N * N:
                return True

def manhattan_distance(board: List[List[int]]) -> int:
    N = len(board)
    distance = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                continue
            target_val = board[i][j] - 1
            target_x, target_y = divmod(target_val, N)
            distance += abs(i - target_x) + abs(j - target_y)
    return distance

def ida_star(board: List[List[int]]) -> List[Tuple[int, int]]:
    N = len(board)
    path = []
    
    def dfs(board: List[List[int]], g: int, bound: int, path: List[Tuple[int, int]]) -> int:
        h = manhattan_distance(board)
        f = g + h
        if f > bound:
            return f
        if is_goal(board):
            return -1
        min_bound = float('inf')
        
        zero_x, zero_y = 0, 0
        for i in range(N):
            for j in range(N):
                if board[i][j] == 0:
                    zero_x, zero_y = i, j
                    
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = zero_x + dx, zero_y + dy
            if 0 <= new_x < N and 0 <= new_y < N:
                board[zero_x][zero_y], board[new_x][new_y] = board[new_x][new_y], board[zero_x][zero_y]
                path.append((new_x, new_y))
                
                t = dfs(board, g + 1, bound, path)
                
                if t == -1:
                    return -1
                if t < min_bound:
                    min_bound = t
                
                path.pop()
                board[zero_x][zero_y], board[new_x][new_y] = board[new_x][new_y], board[zero_x][zero_y]
        
        return min_bound

    bound = manhattan_distance(board)
    while True:
        t = dfs(board, 0, bound, path)
        if t == -1:
            return path
        if t == float('inf'):
            return None
        bound = t

if __name__ == "__main__":
    board = [
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 7, 11],
        [13, 14, 15, 12]
    ]
    
    solution_path = ida_star(board)
    if solution_path:
        print("Solution found:")
        for move in solution_path:
            print(move)
    else:
        print("No solution found")

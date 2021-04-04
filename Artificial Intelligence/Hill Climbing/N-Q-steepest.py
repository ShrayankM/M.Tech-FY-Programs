
#* Simple Hill Climbing (N - Queens Problem)

import random
import copy
from collections import Counter
# random.seed(3)

N = 5
C = N - 2

t_solutions = 0

initial_board = [random.randrange(N) for _ in range(N)]

#* Generates solution after 36 neighbours
# initial_board = [0, 1, 3, 1]

def calculate_heuristic(board):
    heuristics = 0
    a, b, c = [Counter() for _ in range(C)]

    for i in range(len(board)):
        row, col = i, board[i]
        a[col] += 1
        b[row - col] += 1
        c[row + col] += 1
    
    for count in [a, b, c]:
        for key in count:
            heuristics += count[key] * (count[key] - 1) / 2
    
    return heuristics

def generate_neighbours(board):
    neighbours = []
    for i in range(N):
        for j in range(N):
            if j != board[i]:
                new_neighbour = list(board)
                new_neighbour[i] = j
                neighbours.append(new_neighbour)
    return neighbours

def print_board(board):
    b = []
    for i in range(N):
        for j in range(N):
            if j != board[i]:
                b.append(' - ')
            else:
                b.append(' Q ')
        b.append('\n')
    print(''.join(b))

def generate_solutions(board, current_cost):
    neighbours = generate_neighbours(board)

    global t_solutions
    t_solutions += len(neighbours)

    for n in neighbours:
        # print(n)
        cost = calculate_heuristic(n)

        if cost < current_cost:
            current_cost = cost
            board = n
    return board, current_cost

if __name__ == '__main__':
    print_board(initial_board)
    heuristic_cost = calculate_heuristic(initial_board)

    
    while(True):
        board, board_cost = generate_solutions(initial_board, heuristic_cost)

        if board_cost < heuristic_cost:
            heuristic_cost = board_cost
            initial_board = copy.deepcopy(board)
        else:
            break
    
    print("Steepest Ascent Hill Climbing")
    print("Total Solutions Checked = " + str(t_solutions))
    print("Final Solution")
    print_board(initial_board)

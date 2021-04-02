
#* Simple Hill Climbing (8-puzzle problem)
import copy
import math

t_solutions = 0

#* Gets Solution [DOES NOT GET STUCK ON LOCAL MAXIMA]
# intital_board = [
#     ['1', '4', '2'],
#     [' ', '3', '5'],
#     ['6', '7', '8']
# ]

#* Does Not Get Solution [GETS STUCK ON LOCAL MAXIMA]
intital_board = [
    [' ', '2', '3'],
    ['1', '8', '4'],
    ['7', '6', '5']
]

goal_board = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', ' ']
]

R = 2
C = 2

def decrease_col(index, board):
    r, c = index
    t = board[r][c]
    board[r][c] = board[r][c - 1]
    board[r][c - 1] = t
    return board 

def increase_col(index, board):
    r, c = index
    t = board[r][c]
    board[r][c] = board[r][c + 1]
    board[r][c + 1] = t
    return board 

def decrease_row(index, board):
    r, c = index
    t = board[r][c]
    board[r][c] = board[r - 1][c]
    board[r - 1][c] = t
    return board 

def increase_row(index, board):
    r, c = index
    t = board[r][c]
    board[r][c] = board[r + 1][c]
    board[r + 1][c] = t
    return board 


def manhattan_distance(board):
    m_distance = 0
    n = len(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ': continue
            v = int(board[i][j])
            r = int(math.ceil(v / n))
            c = v % n
            if c == 0: c == n
            m_distance += abs(i - r) + abs(c - j)
    return m_distance

def generate_solutions(board):
    solutions = []
    index_blank = None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                index_blank = tuple([i, j])
                break
            if index_blank != None:
                break
    
    #* Move the blank to left side
    if index_blank[1] > 0:
        solutions.append(decrease_col(index_blank, copy.deepcopy(board)))
    
    #* Move the blank to right side
    if index_blank[1] < C:
        solutions.append(increase_col(index_blank, copy.deepcopy(board)))
    
    #* Move the blank to top side
    if index_blank[0] > 0:
        solutions.append(decrease_row(index_blank, copy.deepcopy(board)))

    #* Move the blank to bottom side
    if index_blank[0] < R:
        solutions.append(increase_row(index_blank, copy.deepcopy(board)))

    global t_solutions
    t_solutions += len(solutions)
    
    current_cost = manhattan_distance(board)
    
    for sol in solutions:
        get_cost = manhattan_distance(sol)
        
        if get_cost < current_cost:
            current_cost = get_cost
            board = sol
    
    return board, current_cost

if __name__ == '__main__':
    cost = manhattan_distance(intital_board)

    while(True):
        board, board_cost = generate_solutions(intital_board)
        if board_cost < cost:
            cost = board_cost
            intital_board = copy.deepcopy(board)
        else:
            break

    print("Total Solutions Checked = " + str(t_solutions))
    print('Final Solution')
    for i in range(len(intital_board)):
        print(intital_board[i])
        
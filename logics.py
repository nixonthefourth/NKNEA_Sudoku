GRID_COUNT = 9

def is_safe(sudoku, x, y, num):
    for i in range(9):
        if sudoku[x][i] == num:
            return False

    for i in range(9):
        if sudoku[i][y] == num:
            return False

    small_x = x - x % 3
    small_y = y - y % 3

    for i in range(3):
        for j in range(3):
            if sudoku[small_x + i][small_y + j] == num:
                return False

    return True
 
def sudoku_solution(sudoku, x, y):
    if x == GRID_COUNT - 1 and y == GRID_COUNT:
        return True

    if y == GRID_COUNT:
        x += 1
        y = 0

    if sudoku[x][y] > 0:
        return sudoku_solution(sudoku, x, y+1)
    
    for i in range(1, GRID_COUNT + 1):
        if is_safe(sudoku, x, y, i):
            sudoku[x][y] = i

            if sudoku_solution(sudoku, x, y+1):
                return True

        sudoku[x][y] = 0

    return False

def sudoku_validation(sudoku_dict):
    for i in range(9):
        x_dict = {}
        y_dict = {}
        block_dict = {}

        x_cube = 3 * (i // 3)
        y_cube = 3 * (i % 3)

        for j in range(9):
            if sudoku_dict[i][j] != 0 and sudoku_dict[i][j] in x_dict:
                return False

            x_dict[sudoku_dict[i][j]] = 1

            if sudoku_dict[j][i] != 0 and sudoku_dict[j][i] in y_dict:
                return False
    
            y_dict[sudoku_dict[j][i]] = 1

            x_index = x_cube + j // 3
            y_index = y_cube + j % 3

            if sudoku_dict[x_index][y_index] in block_dict and sudoku_dict[x_index][y_index] != 0:
                return False

            block_dict[sudoku_dict[x_index][y_index]] = 1

            return True

def logics(sudoku_data):
    if sudoku_validation(sudoku_data):
        sudoku_solution(sudoku_data, 0, 0)
        return sudoku_data
    else:
        return 'No'
import numpy as np

def contains_in_row(row, num):
    for i in range(9):
        if sudoku[row][i] == num:
            return True
    return False


def contains_in_col(col, num):
    for i in range(9):
        if sudoku[i][col] == num:
            return True
    return False


def contains_in_box(row, col, num):
    r = row - row % 3
    c = col - col % 3

    for i in range(r, r + 3):
        for j in range(c, c + 3):
            if sudoku[i][j] == num:
                return True
    return False


def is_allowed(row, col, num):
    return not(contains_in_row(row, num) or contains_in_col(col, num) or contains_in_box(row, col, num))


def solve(sudoku):
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                for num in range(1, 10):
                    if is_allowed(row, col, num):
                        sudoku[row][col] = num
                        if solve(sudoku):
                            return True
                        else:
                            sudoku[row][col] = 0
                return False
    return True


if __name__ == "__main__":
    sudoku = np.array([[0, 0, 2, 0, 0, 0, 0, 0, 0],
                       [6, 1, 0, 8, 0, 3, 4, 7, 0],
                       [0, 8, 0, 0, 1, 0, 0, 0, 5],
                       [0, 0, 9, 0, 0, 0, 0, 0, 0],
                       [4, 5, 0, 0, 0, 0, 7, 0, 6],
                       [0, 0, 0, 0, 0, 0, 0, 3, 0],
                       [9, 0, 7, 4, 6, 0, 8, 0, 1],
                       [0, 6, 0, 0, 0, 5, 0, 0, 9],
                       [0, 0, 0, 0, 0, 0, 0, 2, 0]])


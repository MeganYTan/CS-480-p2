def print_matrx(matrix):
    for row in matrix:
        print()
        # print("-+" * 9)
        print("|", end = "")
        for col in row:
            print (col, end="|")
    print()


def is_valid(puzzle, row, col, num):
    # Check if the number is not repeated in the current row, column and 3x3 grid
    for i in range(9):
        if puzzle[row][i] == num or puzzle[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if puzzle[start_row + i][start_col + j] == num:
                return False

    return True

def solve_sudoku(puzzle):
    empty = find_empty(puzzle)
    if not empty:
        return True  # Puzzle solved
    row, col = empty

    for num in range(1, 10):
        for row in range(0,9):
            for col in range(0,9):
                if is_valid(puzzle, row, col, num):
                    puzzle[row][col] = num

                    if solve_sudoku(puzzle):
                        return True

                    puzzle[row][col] = 0  # Backtrack

    return False

def find_empty(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == 0:
                return (i, j)  # row, col
    return None

# Define a Sudoku puzzle
puzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0]
     ]

if __name__ == '__main__':
    # Solve the puzzle
    if solve_sudoku(puzzle):
        solved_puzzle = puzzle
    else:
        solved_puzzle = "No solution exists"

    print_matrx(solved_puzzle)

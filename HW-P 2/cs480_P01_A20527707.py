from math import floor
import sys
import copy
# import pandas
import csv
have_printed = False
# OPTION 1 BRUTE FORCE
def brute_force(matrix, count):
    print_matrx(matrix)

    for i in range(1, 10):
        for row in range(0, 9):
            for col in range(0, 9):
                if is_valid(matrix, i, row, col):
                    # put the number in
                    matrix[row][col] = i
                    can_solve, count = brute_force(matrix, count + 1)
                    if can_solve:
                        return True, count
                matrix[row][col] = 0

    return False, count


# option 2 backtracking - resource: https://www.youtube.com/watch?v=tvP_FZ-D9Ng
def find_next_empty(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            # return i,j if 0
            if matrix[i][j] == 0:
                return i, j
    return None, None


def is_valid(matrix, guess, row, col):
    # check if valid in its current state
    # all rows must have different num
    if guess in matrix[row]:
        return False
    for i in range(len(matrix)):
        if matrix[i][col] == guess:
            return False
    # all boxes must have different num
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            if matrix[i][j] == guess:
                return False
    return True


def backtracking(matrix, count):
    print_matrx(matrix)
    row, col = find_next_empty(matrix)
    if row is None:
        # matrix is full
        return True, count

    for i in range(1, 10):
        if is_valid(matrix, i, row, col):
            # put the number in
            matrix[row][col] = i
            can_solve, count = backtracking(matrix, count + 1)
            if can_solve:
                return True, count
        matrix[row][col] = 0

    return False, count


# OPTION 3 MRV
# mrv is the cell with the most rows, columns, box cells filled
# keep track of domain of each cell instead
def find_all_empty(matrix):
    empty_cells = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            # return i,j if 0
            if matrix[i][j] == 0:
                empty_cells.append((i,j))
    return empty_cells

def find_cell_domain(matrix, row_index, col_index,):
    # check rows
    # check cols
    # check box
    cell_domain = {1,2,3,4,5,6,7,8,9}
    for col in matrix[row_index]:
        if col != 0 and col in cell_domain:
            cell_domain.remove(col)
    for i in range(len(matrix)):
        cell_val = matrix[i][col_index]
        if cell_val != 0 and cell_val in cell_domain:
            cell_domain.remove(cell_val)
    row_start = (row_index // 3) * 3
    col_start = (col_index // 3) * 3
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            cell_val = matrix[i][j]
            if cell_val != 0 and cell_val in cell_domain:
                cell_domain.remove(cell_val)
    return list(cell_domain)


# domain is a 9x9 matrix corresponding to each cell in the sudoku grid
# mrv cell is the one with the least numbers in the domain
def find_mrv_cell(empty_cells,domain):
    min = 10 # max 9 option so set min to 10
    min_cell = None
    # iterate through
    for cell in empty_cells:
        cell_domain = domain[cell]
        if len(cell_domain) < min:
            min = len(cell_domain)
            min_cell = cell
    print(min_cell)
    return min_cell



def forward_check(matrix, empty_cells, domain):
    new_domain = copy.deepcopy(domain)
    for cell in empty_cells:
        row, col = cell
        values = new_domain[(row, col)]
        # Check row
        for j in range(9):
            if matrix[row][j] in values:
                values.remove(matrix[row][j])
        # Check column
        for i in range(9):
            if matrix[i][col] in values:
                values.remove(matrix[i][col])
        # Check box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if matrix[i][j] in values:
                    values.remove(matrix[i][j])
        new_domain[(row, col)] = values
    return new_domain
# forward check, take empty cell, row/col, domain, matrix
# def forward_check(matrix, empty_cells, domain, cell):
#     new_domain = copy.deepcopy(domain)
#     cell_row = cell[0]
#     cell_col = cell[1]
#     value_to_remove = matrix[cell_row][cell_col]
#     for check_cell in empty_cells:
#         check_cell_row = check_cell[0]
#         check_cell_col = check_cell[1]
#         check_cell_domain = new_domain[(check_cell_row, check_cell_col)]
#         # check row
#         if check_cell_row == cell_row and value_to_remove in check_cell_domain:
#            check_cell_domain.remove(value_to_remove)
#         # check col
#         if check_cell_col == cell_col and value_to_remove in check_cell_domain:
#             check_cell_domain.remove(value_to_remove)
#         # check box
#         box_row = (cell_row // 3) * 3
#         box_col = (cell_col // 3) * 3
#         for i in range(box_row, box_row + 3):
#             for j in range(box_col, box_col+3):
#                 if check_cell_row == i and check_cell_col == j and value_to_remove in check_cell_domain:
#                     check_cell_domain.remove(value_to_remove)
#         new_domain[(check_cell_row, check_cell_col)] = check_cell_domain
#     return new_domain

def is_valid_mrv(domain, empty_cells):
    # domain cannot be empty
    # return all(len(domain[cell]) > 0 for cell in empty_cells)
    for cell in empty_cells:
        if len(domain[cell]) == 0:
            return False
    return True


def mrv(matrix, empty_cells, domain, count):
    print_matrx(matrix)
    if not empty_cells:
        # solved
        return True, count
    # find mrv
    cell = find_mrv_cell(empty_cells, domain)
    cell_domain = domain[cell]
    row = cell[0]
    col = cell[1]
    for value in cell_domain:
        #  place each value in the mrv cell and forward check
        matrix[row][col] = value
        empty_cells.remove(cell)

        new_domain = forward_check(matrix, empty_cells, domain)

        if is_valid_mrv(domain, empty_cells): #new_empty_cells
            result, count = mrv(matrix, empty_cells, new_domain, count + 1)
            if result:
                return True, count
            # back track
            matrix[row][col] = 0
            empty_cells.append(cell)
    return False, count

def handle_mrv(matrix):
    empty_cells = find_all_empty(matrix)
    domain = {}
    for cell in empty_cells:
        domain[cell] = find_cell_domain(matrix, cell[0], cell[1])
    return mrv(matrix, empty_cells, domain, 0)

# OPTION 4 CHECK
def check_correct(matrix):
    # all rows must have different num
    for row in matrix:
        # have a dict/hashset and put numbers in the set. if number alr exists then return false
        dict = {}
        for i in row:
            if i in dict:
                return False
            elif i != 0:
                dict[i] = 1
    # all cols must have different num
    for col in range(len(matrix[0])):
        dict = {}
        for row in range(len(matrix)):
            if matrix[row][col] in dict:
                return False
            elif col != 0:
                dict[matrix[row][col]] = 1
    # all boxes must have different num
    arr = [0, 3, 6]
    for i in arr:
        for j in arr:
            dict = {}
            for row in range(0 + i, 3 + i):
                for col in range(0 + j, 3 + j):
                    if matrix[row][col] in dict:
                        return False
                    elif matrix[row][col] != 0:
                        dict[matrix[row][col]] = 1
    return True





# This function prints the details at the start of the program containing the user param inputs
def print_details(algorithm, input_file):
    algorithm_string = ""
    if algorithm == 1:
        algorithm_string = "Brute Force"
    elif algorithm == 2:
        algorithm_string = "CSP Back Tracking"
    elif algorithm == 3:
        algorithm_string = "CSP with forward-checking and MRV heuristics"
    elif algorithm == 4:
        algorithm_string = "Check if Sudoku is correct"
    print('Tan, Megan, A20527707 solution:'
          '\nInput File: ', input_file,
          '\nAlgorithm: ', algorithm_string)


def print_row_divider():
    print("+-------+-------+-------+")


def print_matrx(matrix):
    print_row_divider()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if j == 0:
                print("|", end=" ")
            print(matrix[i][j], end=" ")
            if j == 2 or j == 5 or j == 8:
                print("|", end=" ")
        print()
        if i == 2 or i == 5:
            print_row_divider()
    print_row_divider()


def print_cl_error():
    print("ERROR: Not enough/too many/illegal input arguments.")
    sys.exit()

def init_matrix(input_file_name):
    # read file and convert to matrix
    file = open(input_file_name,mode="r")
    matrix = []
    for line in file:
        replaced_line = line.replace('X', '0').replace('\n', '')
        line_arr = replaced_line.split(',')
        matrix.append(line_arr)
    return matrix

if __name__ == '__main__':
    algorithm = 3  # 1 brute, 2 CSP, 3 CSP MRV, 4 test
    input_file = "testcase2.csv"
    # matrix =[[1, 2, 3, 4, 5, 6, 7, 8, 9],
    #          [4, 5, 6, 7, 8, 9, 1, 2, 3],
    #          [7, 8, 9, 1, 2, 3, 4, 5, 6],
    #          [2, 1, 4, 3, 6, 5, 8, 9, 7],
    #          [3, 6, 5, 8, 9, 7, 2, 1, 4],
    #          [8, 9, 7, 2, 1, 4, 3, 6, 5],
    #          [5, 3, 1, 6, 4, 2, 9, 7, 8],
    #          [6, 4, 2, 9, 7, 8, 5, 3, 1],
    #          [9, 7, 8, 5, 3, 1, 6, 4, 2]]
    # empty sudoku
    matrix = [[6, 0, 0, 0, 4, 0, 0, 2, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
              ]
    # matrix = init_matrix(input_file)
    # if ran from command line
    cl_arguments = sys.argv[1:]
    print (cl_arguments)
    if len(cl_arguments) != 0:
        if len(cl_arguments) != 2:
            print_cl_error()
        else:
            algorithm = cl_arguments[0]
            input_file = cl_arguments[1]
            if algorithm != "1" and algorithm != "2" and algorithm != "3" and algorithm != "4":
                print_cl_error()
            else:
                matrix = init_matrix(input_file)
                algorithm = int(algorithm)

    print_details(algorithm, input_file)
    print_matrx(matrix)
    if algorithm == 1:
        is_solvable, count = brute_force(matrix, 0)
    elif algorithm == 2:
        is_solvable, count = backtracking(matrix, 0)
        print(count)
    elif algorithm == 3:
        is_solvable, count = handle_mrv(matrix)
        print(count)
    elif algorithm == 4:
        corr = check_correct(matrix)
        if corr:
            print("This is a valid, solved, Sudoku matrix.")
        else:
            print("ERROR: This is NOT a solved Sudoku matrix.")

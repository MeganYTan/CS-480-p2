from math import floor
import sys
import copy
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
def find_mrv_cell(domain):
    min = 10 # max 9 option so set min to 10
    min_cell = None
    # iterate through
    for row_index in range(len(domain)):
        for col_index in range(len(domain[row_index])):
            cell_domain = domain[row_index][col_index]
            if len(cell_domain) < min:
                min = len(cell_domain)
                min_cell = (row_index,col_index)
    return min_cell


# #return matrix in the size of sudoku matrix that is the domain for each cell
def find_cell_domains(matrix):
    domain = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for row_index in range(len(matrix)):
        for col_index in range(len(matrix[row_index])):
            if matrix[row_index][col_index] != 0:
                eliminate_possibilities(matrix, domain, row_index, col_index, matrix[row_index][col_index])
    return domain



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

def mrv(matrix, domain, count):
    print_matrx(matrix)
    mrv_cell = find_mrv_cell(domain)
    if mrv_cell is None:
        # matrix is full
        return True, count
    row_index = mrv_cell[0]
    col_index = mrv_cell[1]
    cell_domain = domain[row_index][col_index].copy()
    for value in cell_domain:
        if is_valid_with_domain(domain, row_index, col_index, value):
            matrix[row_index][col_index] = value
            saved_domain = [row.copy() for row in domain]
            eliminate_possibilities(matrix, domain, row_index, col_index, value)

            can_solve, count = mrv(matrix, domain, count+1)
            if can_solve:
                return True, count

            domain[row_index][col_index] = 0  # Backtrack
            domain = saved_domain  # Restore possibilities

    return False, count

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


def input_to_matrix(input):
    # input = '''X,6,X,2,X,4,X,5,X
    # 4,7,X,X,6,X,X,8,3
    # X,X,5,X,7,X,1,X,X
    # 9,X,X,1,X,3,X,X,2
    # X,1,2,X,X,X,3,4,X
    # 6,X,X,7,X,9,X,X,8
    # X,X,6,X,8,X,7,X,X
    # 1,4,X,X,9,X,X,2,5
    # X,8,X,3,X,5,X,9,X
    # '''
    replaced_input = input.replace('X', '0')
    rows = replaced_input.split('\n')
    for i in range(len(rows)):
        rows[i] = rows[i].split(',')
    return rows


if __name__ == '__main__':
    algorithm = 3  # 1 brute, 2 CSP, 3 CSP MRV, 4 test
    input_file = "N/A"

    # if ran from command line
    cl_arguments = sys.argv[1:]
    if len(cl_arguments) != 0:
        if len(cl_arguments) != 2:
            print_cl_error()
        else:
            algorithm = cl_arguments[0]
            input_file = cl_arguments[1]
            if (algorithm != "1" and algorithm != "2" and algorithm != "3" and algorithm != "4"):
                print_cl_error()
            else:
                # read file and convert to matrix
                file = open(input_file, 'r')
                # convert to matrix
                matrix = input_to_matrix(input)
                algorithm = int(algorithm)

    else:
        print("Not command line")
        # completed sudoku
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
        matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]
                  ]
    print_details(algorithm, input_file)
    print_matrx(matrix)
    if algorithm == 1:
        is_solvable, count = brute_force(matrix, 0)
    elif algorithm == 2:
        is_solvable, count = backtracking(matrix, 0)
        print(count)
    elif algorithm == 3:
        domain = find_cell_domains(matrix)
        is_solvable, count = mrv(matrix,domain,0)
        print(count)
    elif algorithm == 4:
        corr = check_correct(matrix)
        if corr:
            print("This is a valid, solved, Sudoku matrix.")
        else:
            print("ERROR: This is NOT a solved Sudoku matrix.")

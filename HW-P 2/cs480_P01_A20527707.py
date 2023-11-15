from math import floor
import sys


def check_constrains(matrix, contrains=None):
    return not check_correct(matrix)


# OPTION 1 BRUTE FORCE
def brute_force(matrix):
    counter = 0
    for i in range(1, 10):
        for row in range(0, 9):
            for col in range(0, 9):
                counter = counter + 1
                matrix[row][col] = i
                # check if constraint violated
                if check_constrains(matrix):
                    matrix[row][col] = 0
                # if constaint violated reset
                print_matrx(matrix)
    print(counter)


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


def print_matrx(matrix):
    print("print matrix")
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")
            if j == 2 or j == 5:
                print("|", end=" ")
        print()
        if i == 2 or i == 5:
            print("------+-------+-------")




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


def print_cl_error():
    print("ERROR: Not enough/too many/illegal input arguments.")
    sys.exit()


def input_to_matrix():
    input = '''X,6,X,2,X,4,X,5,X
4,7,X,X,6,X,X,8,3
X,X,5,X,7,X,1,X,X
9,X,X,1,X,3,X,X,2
X,1,2,X,X,X,3,4,X
6,X,X,7,X,9,X,X,8
X,X,6,X,8,X,7,X,X
1,4,X,X,9,X,X,2,5
X,8,X,3,X,5,X,9,X
'''
    return 0


if __name__ == '__main__':
    algorithm = 1  # 1 brute, 2 CSP, 3 CSP MRV, 4 test
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
                input_to_matrix(input)
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
        # partial sudoku
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
        brute_force(matrix)
    elif algorithm == 2:
        print("DO BRUTE FORCE")
    elif algorithm == 3:
        print("DO BRUTE FORCE")
    elif algorithm == 4:
        corr = check_correct(matrix)
        if corr:
            print("This is a valid, solved, Sudoku puzzle.")
        else:
            print("ERROR: This is NOT a solved Sudoku puzzle.")

import copy


def sudoku_solver(matrix):
    def find_all_empty(matrix):
        empty_cells = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                # return i,j if 0
                if matrix[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells

    def find_cell_domain(matrix, row_index, col_index):
        cell_domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
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

    def find_mrv_cell(empty_cells, domain):
        min = 10  # max 9 option so set min to 10
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



    def mrv(matrix, empty_cells, domain, count):
        print_matrx(matrix)
        if not empty_cells:
            #solved
            return True, count
        # find mrv
        cell = find_mrv_cell(empty_cells, domain)
        cell_domain = domain[cell]
        row = cell[0]
        col = cell[1]
        for value in cell_domain:
            #  place each value in the mrv cell and forward check
            # matrix[row][col] = value
            # empty_cells.remove(cell)
            # new_domain = forward_check(matrix, empty_cells, domain, cell)

            new_matrix = copy.deepcopy(matrix)
            new_matrix[cell[0]][cell[1]] = value
            new_empty_cells = empty_cells.copy()
            new_empty_cells.remove(cell)
            new_domain = forward_check(new_matrix, new_empty_cells, domain)
            if all(len(new_domain[cell]) > 0 for cell in new_empty_cells):
                result, count = mrv(new_matrix, new_empty_cells, new_domain, count+1)
                if result:
                    return True, count
                # matrix[row][col] = 0
                # empty_cells.append(cell)
        return False, count

    # Initialize domain for each empty cell
    empty_cells = find_all_empty(matrix)
    domain = {}
    for cell in empty_cells:
        domain[cell] = find_cell_domain(matrix, cell[0], cell[1])

    # Solve the matrix
    solved_matrix, count = mrv(matrix, empty_cells, domain,0)

    return solved_matrix, count

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

if __name__=='__main__':
    print("main")
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

    solved_matrix, count = sudoku_solver(matrix)
    # print_matrx(solved_matrix)
    print(solved_matrix)
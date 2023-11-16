import copy


def sudoku_solver(board):
    """
    This function takes a 9x9 Sudoku board as input and returns the solved board.
    It uses forward checking and minimum remaining values (MRV) heuristic to solve the board.

    Parameters:
    board (list): A 9x9 list representing the Sudoku board. 0 represents an empty cell.

    Returns:
    list: A 9x9 list representing the solved Sudoku board.
    """

    # Define helper functions

    def get_empty_cells(board):
        """
        This function takes a Sudoku board as input and returns a list of empty cells.

        Parameters:
        board (list): A 9x9 list representing the Sudoku board. 0 represents an empty cell.

        Returns:
        list: A list of tuples representing the row and column indices of empty cells.
        """
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells

    def get_possible_values(board, row, col):
        """
        This function takes a Sudoku board and a cell position as input and returns a list of possible values for that cell.

        Parameters:
        board (list): A 9x9 list representing the Sudoku board. 0 represents an empty cell.
        row (int): The row index of the cell.
        col (int): The column index of the cell.

        Returns:
        list: A list of possible values for the cell.
        """
        values = set(range(1, 10))
        # Check row
        for j in range(9):
            if board[row][j] in values:
                values.remove(board[row][j])
        # Check column
        for i in range(9):
            if board[i][col] in values:
                values.remove(board[i][col])
        # Check box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] in values:
                    values.remove(board[i][j])
        return list(values)

    def forward_checking(board, empty_cells, domain):
        """
        This function takes a Sudoku board, a list of empty cells, and a dictionary of domains as input.
        It performs forward checking and returns a new dictionary of domains.

        Parameters:
        board (list): A 9x9 list representing the Sudoku board. 0 represents an empty cell.
        empty_cells (list): A list of tuples representing the row and column indices of empty cells.
        domain (dict): A dictionary of domains for each empty cell.

        Returns:
        dict: A new dictionary of domains after forward checking.
        """
        new_domain = copy.deepcopy(domain)
        for cell in empty_cells:
            row, col = cell
            values = new_domain[(row, col)]
            # Check row
            for j in range(9):
                if board[row][j] in values:
                    values.remove(board[row][j])
            # Check column
            for i in range(9):
                if board[i][col] in values:
                    values.remove(board[i][col])
            # Check box
            box_row = (row // 3) * 3
            box_col = (col // 3) * 3
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if board[i][j] in values:
                        values.remove(board[i][j])
            new_domain[(row, col)] = values
        return new_domain

    def mrv(empty_cells, domain):
        """
        This function takes a list of empty cells and a dictionary of domains as input and returns the cell with the minimum remaining values.

        Parameters:
        empty_cells (list): A list of tuples representing the row and column indices of empty cells.
        domain (dict): A dictionary of domains for each empty cell.

        Returns:
        tuple: A tuple representing the row and column indices of the cell with the minimum remaining values.
        """
        min_cell = None
        min_values = float('inf')
        for cell in empty_cells:
            values = domain[cell]
            if len(values) < min_values:
                min_cell = cell
                min_values = len(values)
        return min_cell

    def solve(board, empty_cells, domain):
        """
        This function takes a Sudoku board, a list of empty cells, and a dictionary of domains as input and returns the solved board.

        Parameters:
        board (list): A 9x9 list representing the Sudoku board. 0 represents an empty cell.
        empty_cells (list): A list of tuples representing the row and column indices of empty cells.
        domain (dict): A dictionary of domains for each empty cell.

        Returns:
        list: A 9x9 list representing the solved Sudoku board.
        """
        if not empty_cells:
            return board
        cell = mrv(empty_cells, domain)
        values = domain[cell]
        for value in values:
            new_board = copy.deepcopy(board)
            new_board[cell[0]][cell[1]] = value
            new_empty_cells = empty_cells.copy()
            new_empty_cells.remove(cell)
            new_domain = forward_checking(new_board, new_empty_cells, domain)
            if all(len(new_domain[cell]) > 0 for cell in new_empty_cells):
                result = solve(new_board, new_empty_cells, new_domain)
                if result:
                    return result
        return None

    # Initialize domain for each empty cell
    empty_cells = get_empty_cells(board)
    domain = {}
    for cell in empty_cells:
        domain[cell] = get_possible_values(board, cell[0], cell[1])

    # Solve the board
    solved_board = solve(board, empty_cells, domain)

    return solved_board

if __name__=='__main__':
    print("main")
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
    solved_matrix = sudoku_solver(matrix)
    print(solved_matrix)
import numpy as np


def display_matrix(matrix, n_rows, n_columns):      # function for display a matrix from 2D array
    for row in range(n_rows):
        for column in range(n_columns+1):
            if round(matrix[row][column], 2) - int(matrix[row][column]) == 0:
                print("%6.0d" % matrix[row][column], end='')

            else:
                print("%6.2f" % matrix[row][column], end='')

        print("\n")


def display_set_vectors(vector_set, n_vectors, dimension):  # this function display a set of matrix like null bases
    vector_set = np.array(vector_set, dtype=float)

    for row in range(dimension):
        for vector in range(n_vectors):
            if int(vector_set[vector][row]) != vector_set[vector][row]:
                print('%5.2f' % vector_set[vector][row], end='\t\t\t')
            else:
                print('%5.d' % vector_set[vector][row], end='\t\t\t')
        print('\n')


def det_nonzero_column(matrix, column, start_row_number, n_rows):   # this function detect of existence of a nonzero
    for row in range(start_row_number, n_rows):                       # element in specific column to change rows
        if round(matrix[row][column], 2) != 0:
            return row
    else:
        return -1


def interchange_rows(matrix, first_row, second_row):       # this function interchange two rows
    matrix[[first_row, second_row]] = matrix[[second_row, first_row]]
    return matrix


def row_replacements_forward(matrix, n_rows, n_columns, pivot_row, pivot_column):   # this function make 0
    for row in range(pivot_row + 1, n_rows):                             # elements that below the pivot positions
        if matrix[row][pivot_column] != 0:
            scale = (-1) * (matrix[row][pivot_column] / matrix[pivot_row][pivot_column])
            for column in range(n_columns+1):
                matrix[row][column] = (scale * matrix[pivot_row][column]) + matrix[row][column]
    return matrix


def scale_pivots(matrix, n_columns, pivot_row, pivot_column):  # this function make 1 pivot positions
    scale = matrix[pivot_row][pivot_column]
    if scale != 1:
        for column in range(n_columns+1):
            matrix[pivot_row][column] = round(matrix[pivot_row][column] / scale, 2)
    return matrix


def round_matrix(matrix, n_rows, n_columns):   # this function round entry of matrix like 2.32
    for row in range(n_rows):
        for column in range(n_columns):
            matrix[row][column] = round(matrix[row][column], 2)


def detect_nonzero_row(matrix, n_rows, n_columns):  # this function detect nonzero row
    nonzero_row_number = []
    for row in range(n_rows):
        for column in range(n_columns):
            if round(matrix[row][column], 2) != 0:
                nonzero_row_number.append(row)
                break

    return nonzero_row_number


def row_replacements_backward(matrix, n_columns, pivot_row, pivot_column):      # this function make 0
    for row in range(pivot_row):                                           # elements that above the pivot positions
        scale = (-1) * matrix[row][pivot_column]
        for column in range(n_columns+1):
            matrix[row][column] = (scale * matrix[pivot_row][column]) + matrix[row][column]
    return matrix


def make_reduced_echelon(matrix, n_rows, n_columns, pivot_positions: list):  # this function convert a matrix to RREF
    complete_row = 0
    for column in range(n_columns+1):

        pivot_r_position = det_nonzero_column(matrix, column, complete_row, n_rows)  # find the first none_zero

        if pivot_r_position == -1:  # elements in specific column
            continue

        pivot_positions.append(tuple([complete_row, column]))  # add pivot position to list of them
        matrix = interchange_rows(matrix, complete_row, pivot_r_position)
        matrix = row_replacements_forward(matrix, n_rows, n_columns, complete_row, column)

        complete_row += 1

    round_matrix(matrix, n_rows, n_columns)
    for pivot_row, pivot_column in pivot_positions:  # this section make 1 pivot positions
        matrix = scale_pivots(matrix, n_columns, pivot_row, pivot_column)

    for pivot_row, pivot_column in reversed(pivot_positions):  # this section make 0 elements that above the pivot positions
        matrix = row_replacements_backward(matrix, n_columns, pivot_row, pivot_column)

    return pivot_positions


def make_null_vectors(dependent_vectors: dict, dependent_columns_number: set):  # this function create null bases vector
    vectors = []
    for key, values in dependent_vectors.items():
        temp_vector = [-x for x in dependent_vectors.get(key)]
        for index in dependent_columns_number:
            if index == key:
                temp_vector.insert(index, 1)
            else:
                temp_vector.insert(index, 0)
        vectors.append(temp_vector)
    return vectors

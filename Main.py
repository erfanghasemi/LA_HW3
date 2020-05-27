import numpy as np
import operations as op

print("Please enter size of your Matrix. ")

size = input("Size(m*n): ").split(' ')
m = int(size[0])
n = int(size[1])

entries = []    # array for elements of matrix

for row in range(m):
    entries = entries + list(map(float, input().split()))     # input elements of each line
matrix_A = np.array(entries).reshape(m, n)      # create n * n array with numpy library by using reshape func

zero_vector = np.zeros((m, 1), dtype=float)

augmented_matrix = np.column_stack((matrix_A, zero_vector))     # create augmented matrix of [A | 0]

pivot_positions = []    # list of pivot positions

pivot_positions = op.make_reduced_echelon(augmented_matrix, m, n, pivot_positions)  # convert augmented matrix to RREF

print("\n\n")
op.display_matrix(augmented_matrix, m, n)
print("\n\n")

row_bases_vector = []
column_bases_vector = []
null_bases_vector = {}  # key is number of column and value is column
dependent_vector = []

for row_number in op.detect_nonzero_row(augmented_matrix, m, n):  # detect nonzero row in RREF form
    row_bases_vector.append(augmented_matrix[row_number][:-1])

print("Row Bases : \n")
op.display_set_vectors(row_bases_vector, len(row_bases_vector), n)   # display row bases

pivot_columns_number = []  # list of number of columns that pivot
for row, column in pivot_positions:
    pivot_columns_number.append(column)
    column_bases_vector.append(matrix_A[:, column])

print('\n\n')
print("Column Bases : \n")
op.display_set_vectors(column_bases_vector, len(column_bases_vector), m)    # display column bases

dependent_columns_number = set(list(range(n))) - set(pivot_columns_number)  # list of number of dependent columns
for column in dependent_columns_number:
    null_bases_vector[column] = list(augmented_matrix[:, column])
    dependent_vector.append(matrix_A[:, column])

print('\n\n')
print("Null Bases : \n")
op.display_set_vectors(op.make_null_vectors(null_bases_vector, dependent_columns_number), n-len(column_bases_vector), n)

column_bases_vector = np.array(column_bases_vector).transpose()

coordinates = []
# coordinates of linear combination
for vector in dependent_vector:
    pivot_positions = []
    augmented_matrix_2 = np.column_stack((column_bases_vector, np.array(vector)))
    op.make_reduced_echelon(augmented_matrix_2, m, len(pivot_columns_number), pivot_positions)
    coordinate = augmented_matrix_2[:, -1]
    for number in range(len(coordinate)):
        coordinate[number] = round(coordinate[number], 2)
    coordinates.append(coordinate)


print("\nLinear Combination of dependent vectors : \n")
for vector in range(len(dependent_vector)):
    print(f"{dependent_vector[vector]}   = ", end='')
    for index in range(len(column_bases_vector)):
        if coordinates[vector][index] == 0:
            continue
        print(f"{coordinates[vector][index]} * {column_bases_vector[:, index]} ", end='   ')
    print("\n\n")



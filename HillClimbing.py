import numpy as np


# Busca números duplicados en un arreglo dado
def findNumDupe(nums):
    counter = 0
    for i in range(9):
        row_counter = 0
        for j in range(9):
            if nums[j] == i + 1:
                row_counter += 1
        if row_counter > 0:
            row_counter -= 1
        counter += row_counter
    return counter


# Busca números duplicados en un cuadrado 3x3 del sudoku
def dupeInSquare(grid, square):
    # Determina el cuadrado donde se va a buscar
    if square == 0:
        temp = np.copy(grid[0:3, 0:3])
    elif square == 1:
        temp = np.copy(grid[0:3, 3:6])
    elif square == 2:
        temp = np.copy(grid[0:3, 6:9])
    elif square == 3:
        temp = np.copy(grid[3:6, 0:3])
    elif square == 4:
        temp = np.copy(grid[3:6, 3:6])
    elif square == 5:
        temp = np.copy(grid[3:6, 6:9])
    elif square == 6:
        temp = np.copy(grid[6:9, 0:3])
    elif square == 7:
        temp = np.copy(grid[6:9, 3:6])
    else:
        temp = np.copy(grid[6:9, 6:9])

    # Simplifica la matriz en un arreglo para facilidad de búsqueda
    temp = temp.reshape(9)
    return findNumDupe(temp)


# Contabiliza los duplicados en columnas y cuadrados 3x3 para determinar el valor de la heurística
def totalDupes(state):
    counter = 0
    for i in range(9):
        counter += dupeInSquare(state, i)
    for i in range(9):
        counter += findNumDupe(state[:, i])
    return counter


# Coloca los números faltantes en una fila mezclados aleatoriamente
def randomize(state, i):
    nums = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    row = state[i, :].copy()
    unused = np.zeros(0, dtype=int)
    pos = 0
    for a in range(9):
        if row[a] != 0:
            nums[row[a] - 1] = 0
    for a in range(9):
        if nums[a] != 0:
            unused = np.append(unused, nums[a])
    np.random.shuffle(unused)
    for a in range(9):
        if row[a] == 0:
            row[a] = unused[pos]
            pos += 1
    grid = state.copy()
    grid[i] = row
    return grid


# Algoritmo principal de Hill Climbing
def hillClimbing(initial_state):
    current_state = initial_state.copy()
    row = 0
    counter = 0

    while True:
        resetting = False
        new_state = randomize(current_state.copy(), row)
        errors = totalDupes(new_state)
        # Se buscan 0 errores en cada iteración
        while errors > 0:
            counter += 1
            # Contador para evitar bucles infinitos
            if counter > 1000:
                print("Resetting...")
                current_state = initial_state.copy()
                row = 0
                counter = 0
                resetting = True
                break
            new_state = randomize(current_state.copy(), row)
            errors = totalDupes(new_state)
        if not resetting:
            row += 1
            current_state = new_state.copy()
        print("Current row: " + str(row))
        if row == 9:
            break

    return current_state


# Función a ejecutar para resolver el sudoku
def solveSudoku(mat):
    grid = hillClimbing(mat)
    print(grid)
    return grid

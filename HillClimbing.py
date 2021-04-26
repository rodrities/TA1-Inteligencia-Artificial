import numpy as np


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


def dupeInSquare(grid, square):
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

    temp = temp.reshape(9)
    return findNumDupe(temp)


def totalDupes(state):
    counter = 0
    for i in range(9):
        counter += dupeInSquare(state, i)
    for i in range(9):
        counter += findNumDupe(state[:, i])
    return counter


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


def hillClimbing(initial_state):
    current_state = initial_state.copy()
    row = 0
    counter = 0

    while True:
        resetting = False
        new_state = randomize(current_state.copy(), row)
        errors = totalDupes(new_state)
        while errors > 0:
            counter += 1
            if counter > 50000:
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


def solveSudoku(mat):
    grid = hillClimbing(mat)
    print(grid)
    return grid

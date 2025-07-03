import random
import copy

def generate_empty_maze(maze_size):
    maze = {}
    for row in range(maze_size[1]):
        maze[row] = {}
        for col in range(maze_size[0]):
            maze[row][col] = ["E"]
    return maze

def get_finish_zone(maze_size, zone_size=4):
    mid_col = maze_size[0] // 2
    mid_row = maze_size[1] // 2
    start_col = mid_col - zone_size // 2
    start_row = mid_row - zone_size // 2
    coords = []
    for row in range(start_row, start_row + zone_size):
        for col in range(start_col, start_col + zone_size):
            coords.append((col, row))
    return coords

def generate_maze_structure(maze, finish_cells):
    for row in maze:
        for col in maze[row]:
            if (col, row) in finish_cells:
                maze[row][col] = ["F"]
                continue

            # Compute closest finish cell
            closest = min(finish_cells, key=lambda f: abs(f[0] - col) + abs(f[1] - row))
            dx = closest[0] - col
            dy = closest[1] - row

            if abs(dx) >= abs(dy):
                maze[row][col] = ["R"] if dx > 0 else ["L"]
            else:
                maze[row][col] = ["D"] if dy > 0 else ["U"]

def take_step(maze, pivot, banned):
    pivot_row = pivot[1]
    pivot_col = pivot[0]

    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    LetterFromDir = {
        (-1, 0): "L",
        (1, 0): "R",
        (0, 1): "D",
        (0, -1): "U"
    }

    available = []
    for dx, dy in directions:
        row = pivot_row + dy
        col = pivot_col + dx
        if (col, row) == banned:
            continue
        if row in maze and col in maze[row]:
            available.append((dx, dy))

    if not available:
        return pivot

    dx, dy = random.choice(available)
    new_row = pivot_row + dy
    new_col = pivot_col + dx

    maze[pivot_row][pivot_col] = [LetterFromDir[(dx, dy)]]
    maze[new_row][new_col] = ["E"]
    return (new_col, new_row)

def fix_directions(maze):
    maze2 = copy.deepcopy(maze)

    directions = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1)
    }

    opposite = {
        "L": "R",
        "R": "L",
        "U": "D",
        "D": "U"
    }

    for row in maze2:
        for col in maze2[row]:
            for dir_letter, (dx, dy) in directions.items():
                row1, col1 = row + dy, col + dx
                if row1 in maze2 and col1 in maze2[row1]:
                    if opposite[dir_letter] in maze2[row1][col1]:
                        if dir_letter not in maze2[row][col]:
                            maze2[row][col].append(dir_letter)

    # Remove "E" from all cells
    for row in maze2:
        for col in maze2[row]:
            if "E" in maze2[row][col]:
                maze2[row][col].remove("E")
    return maze2

def connect_finish_cells(maze, finish_cells):
    directions = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1)
    }

    opposite = {
        "L": "R",
        "R": "L",
        "U": "D",
        "D": "U"
    }

    for col, row in finish_cells:
        for dir_letter, (dx, dy) in directions.items():
            ncol, nrow = col + dx, row + dy
            if nrow in maze and ncol in maze[nrow]:
                if "F" in maze[nrow][ncol]:
                    if dir_letter not in maze[row][col]:
                        maze[row][col].append(dir_letter)
                    if opposite[dir_letter] not in maze[nrow][ncol]:
                        maze[nrow][ncol].append(opposite[dir_letter])

def generate_maze(maze_size, scramble=1, finish_zone_size=4):
    maze = generate_empty_maze(maze_size)
    finish_cells = get_finish_zone(maze_size, finish_zone_size)
    generate_maze_structure(maze, finish_cells)

    # Pick a random starting point outside the finish zone
    all_coords = [(c, r) for r in range(maze_size[1]) for c in range(maze_size[0])]
    non_finish = [pos for pos in all_coords if pos not in finish_cells]
    newpivot = random.choice(non_finish)

    for _ in range(len(maze) * len(maze[0]) * 10 * scramble):
        oldpivot = newpivot
        newpivot = take_step(maze, newpivot, oldpivot)

    maze = fix_directions(maze)

    # Re-apply and connect all finish cells
    for col, row in finish_cells:
        if "F" not in maze[row][col]:
            maze[row][col].append("F")

    connect_finish_cells(maze, finish_cells)

    return maze

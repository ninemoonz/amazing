def read_maze(filename: str) -> list[list[int]]:
    converted_list: list[list[int]] = []
    with open(filename) as f:
        for line in f:
            converted_row: list[int] = []
            stripped = line.strip()
            if stripped == "":
                break
            for ch in stripped:
                converted_row.append(int(ch, 16))
            converted_list.append(converted_row)
    return converted_list


def render_maze(grid: list[list[int]]) -> None:
    height = len(grid)
    width = len(grid[0])
    print(f"height of the grid: {height}")
    print(f"width of the grid: {width}")
    canvas: list[list[str]] = []
    for _ in range(2 * height + 1):
        row = [' '] * (2 * width + 1)
        canvas.append(row)
    for r in range(height):
        for c in range(width):
            v = grid[r][c]
            print(f"cell at row {r}, col {c} has value {v}")
            cx = 2 * c + 1
            cy = 2 * r + 1
            if v & 1:
                canvas[cy - 1][cx] = '#'
            if v & 2:
                canvas[cy][cx + 1] = '#'
            if v & 4:
                canvas[cy + 1][cx] = '#'
            if v & 8:
                canvas[cy][cx - 1] = '#'
            for dy, dx in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
                canvas[cy + dy][cx + dx] = '#'
    for maze_row in canvas:
        new_row = ''.join(maze_row)
        print(new_row)


if __name__ == "__main__":
    con_list = read_maze("maze.txt")
    print(con_list)
    render_maze(con_list)

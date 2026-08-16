from validate_and_build import MazeConfig


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


def render_maze(grid: list[list[int]],
                entry_p: tuple[int, int],
                exit_p: tuple[int, int]) -> list[list[str]]:
    height = len(grid)
    width = len(grid[0])
    canvas: list[list[str]] = []
    wall = '■'
    for _ in range(2 * height + 1):
        row = [' '] * (2 * width + 1)
        canvas.append(row)
    for r in range(height):
        for c in range(width):
            v = grid[r][c]
            cx = 2 * c + 1
            cy = 2 * r + 1
            if r == entry_p[1] and c == entry_p[0]:
                canvas[cy][cx] = 'A'
            if r == exit_p[1] and c == exit_p[0]:
                canvas[cy][cx] = 'B'
            if v & 1:
                canvas[cy - 1][cx] = wall
            if v & 2:
                canvas[cy][cx + 1] = wall
            if v & 4:
                canvas[cy + 1][cx] = wall
            if v & 8:
                canvas[cy][cx - 1] = wall
            for dy, dx in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
                canvas[cy + dy][cx + dx] = wall
    for maze_row in canvas:
        new_row = ' '.join(maze_row)
        print(new_row)
    return canvas


def render_path(maze: list[list[str]]) -> None:
    ...

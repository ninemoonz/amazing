"""Maze rendering and visualization.

Provides functionality to render maze grids as ASCII art with colored
walls, markers for entry/exit points, and visualization of solution paths.
"""

from src.validate_and_build import MazeConfig


class MazeColor:
    """ANSI color codes for terminal output.

    Attributes:
        PINK: Magenta/pink color code.
        BLUE: Blue color code.
        GREEN: Green color code.
        YELLOW: Yellow color code.
        RED: Red color code.
        CYAN: Cyan color code.
        WHITE: White color code.
        BLACK: Black color code.
        RESET: Reset to default color.
    """

    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BLACK = '\033[90m'
    RESET = '\033[0m'


WALL_COLORS: list[str] = [MazeColor.PINK,
                          MazeColor.GREEN,
                          MazeColor.YELLOW,
                          MazeColor.CYAN,
                          MazeColor.WHITE
                          ]


def read_maze(filename: str) -> list[list[int]]:
    """Read hexadecimal maze from file.

    Parses maze file format where each character is a hex digit
    representing one cell's wall configuration.

    Args:
        filename: Path to maze output file.

    Returns:
        list[list[int]]: 2D grid of cell wall values (0-15).
    """
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
                exit_p: tuple[int, int],
                color_index: int = 0) -> list[list[str]]:
    """Render maze grid as colored ASCII art.

    Creates a doubled coordinate canvas where maze cells are
    centered and walls fill adjacent positions. Entry marked in red,
    exit marked in blue.

    Args:
        grid: 2D list of cell wall values.
        entry_p: (x, y) entry point coordinate.
        exit_p: (x, y) exit point coordinate.
        color_index: Index into WALL_COLORS list (0-4).

    Returns:
        list[list[str]]: 2D grid of ANSI-colored ASCII strings.
    """
    height = len(grid)
    width = len(grid[0])
    canvas: list[list[str]] = []
    wall = f'{WALL_COLORS[color_index]}██{MazeColor.RESET}'
    for _ in range(2 * height + 1):
        row = ['  '] * (2 * width + 1)
        canvas.append(row)
    for r in range(height):
        for c in range(width):
            v = grid[r][c]
            cx = 2 * c + 1
            cy = 2 * r + 1
            if r == entry_p[1] and c == entry_p[0]:
                canvas[cy][cx] = f'{MazeColor.RED}▓▓{MazeColor.RESET}'
            if r == exit_p[1] and c == exit_p[0]:
                canvas[cy][cx] = f'{MazeColor.BLUE}▓▓{MazeColor.RESET}'
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
    return canvas


def render_path(maze: list[list[str]],
                path: str,
                config_value: MazeConfig) -> None:
    """Overlay solution path on rendered maze.

    Walks the solution path from entry to exit, marking corridors
    with shade characters. Modifies maze canvas in-place.

    Args:
        maze: 2D canvas from render_maze (modified in-place).
        path: Solution path string (e.g. 'ENWSE').
        config_value: Configuration for maze dimensions.
    """
    height = config_value.height
    width = config_value.width if height else 0
    moves = {"N": (0, -1),
             "E": (1, 0),
             "S": (0, 1),
             "W": (-1, 0)}
    shade = "░░"
    cx = cy = -1
    for y in range(height):
        for x in range(width):
            if maze[y][x] == f'{MazeColor.RED}▓▓{MazeColor.RESET}':
                cx, cy = x, y
    if cx == -1:
        return
    for ch in path:
        dx, dy = moves[ch]
        gap_x, gap_y = cx + dx, cy + dy
        if maze[gap_y][gap_x] == "  ":
            maze[gap_y][gap_x] = shade
        cx, cy = cx + 2 * dx, cy + 2 * dy
        if maze[cy][cx] == "  ":
            maze[cy][cx] = shade

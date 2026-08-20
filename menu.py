from validate_and_build import build_config, MazeConfig
from maze_generator import generator, MazeCell
from output_generator import output_gen
import maze_display
from maze_display import read_maze, render_maze, render_path
from path_finder import find_path


def print_maze(maze: list[list[str]]) -> None:
    for maze_row in maze:
        print("".join(maze_row))


def build_maze(maze_info: MazeConfig) -> tuple[list[list[int]], str]:
    new_maze: list[list[MazeCell]] = generator(maze_info)
    route = find_path(new_maze, maze_info.entry_point, maze_info.exit_point)
    output_gen(new_maze, maze_info, route)
    grid = read_maze(maze_info.output_file)
    return grid, route


def menu_func(maze_info: MazeConfig) -> None:
    grid, route = build_maze(maze_info)
    show_path = False
    color_index = 0
    while True:
        maze = render_maze(grid,
                           maze_info.entry_point, maze_info.exit_point,
                           color_index)
        if show_path:
            render_path(maze, route, maze_info)
        print_maze(maze)
        print("=== A-Maze-Ing ===")
        print("[1] Re-generate a new maze\n"
              "[2] Show/Hide Path from entry to exit\n"
              "[3] Rotate maze colors\n"
              "[4] Quit Program\n")
        choice = input("Choice (1-4): ")
        if choice == "1":
            grid, route = build_maze(maze_info)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(maze_display.WALL_COLORS)
        elif choice == "4":
            break
        else:
            print("Choose number between 1-4")

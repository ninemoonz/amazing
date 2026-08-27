import sys
import random
from maze_generator import MazeCell, MazeGen
from src.validate_and_build import MazeConfig
from src.output_generator import output_gen
import src.maze_display as maze_display
from src.maze_display import read_maze, render_maze, render_path
from src.path_finder import find_path
from src.error_class import PathFindingError


def print_maze(maze: list[list[str]]) -> None:
    for maze_row in maze:
        print("".join(maze_row))


def build_maze(maze_info: MazeConfig) -> tuple[list[list[int]], str]:
    new_maze: list[list[MazeCell]] = generator(maze_info)
    route = find_path(new_maze, maze_info.entry_point, maze_info.exit_point)
    output_gen(new_maze, maze_info, route)
    grid = read_maze(maze_info.output_file)
    return grid, route


def generator(maze_info: MazeConfig) -> list[list[MazeCell]]:
    width: int = maze_info.width
    height: int = maze_info.height
    entry_p: tuple[int, int] = maze_info.entry_point
    exit_p: tuple[int, int] = maze_info.exit_point
    seed = (maze_info.seed if maze_info.seed is not None
            else random.randrange(2 ** 32))
    new_maze: MazeGen = MazeGen(width, height, entry_p, exit_p, seed)
    new_maze.gen_grid()
    new_maze.link_cells()
    new_maze.forty_two(MazeGen.FORTY_TWO)
    entry_x = entry_p[0]
    entry_y = entry_p[1]
    exit_x = exit_p[0]
    exit_y = exit_p[1]
    if (new_maze.maze_list[entry_y][entry_x].is_sign or
            new_maze.maze_list[exit_y][exit_x].is_sign):
        raise PathFindingError("[PathFindingError] entry or exit "
                               "point is in a sign")
    new_maze.carve_maze()
    if not maze_info.perfect:
        new_maze.braid_maze()
        new_maze.corridor_fix()
    return new_maze.maze_list


def menu_func(maze_info: MazeConfig) -> None:
    try:
        grid, route = build_maze(maze_info)
    except PathFindingError as e:
        print(e)
        sys.exit(1)
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

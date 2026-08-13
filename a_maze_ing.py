import sys
from parser import parse_config
from validate_and_build import build_config, MazeConfig
from error_class import ConfigError
from maze_generator import generator, MazeCell
from output_generator import output_gen
from maze_display import read_maze, render_maze
from path_finder import find_path


def main() -> MazeConfig:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)
    try:
        raw = parse_config(sys.argv[1])
        config = build_config(raw)
        return config
    except ConfigError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    maze_info: MazeConfig = main()
    print(maze_info)
    new_maze: list[list[MazeCell]] = generator(maze_info)
    route = find_path(new_maze, maze_info.entry_point, maze_info.exit_point)
    output_gen(new_maze, maze_info, route)
    output = read_maze(maze_info.output_file)
    render_maze(output)

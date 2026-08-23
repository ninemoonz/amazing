import sys
from src.parser import parse_config
from src.validate_and_build import build_config, MazeConfig
from src.error_class import ConfigError
from src.menu import menu_func


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
    menu_func(maze_info)

"""Main entry point for the Amazing Maze application.

This module orchestrates the maze generation and display workflow.
It parses command-line arguments, loads configuration, and initiates
the menu-driven user interface.
"""

import sys
from src import parse_config, build_config, MazeConfig, ConfigError, menu_func


def main() -> MazeConfig:
    """Parse and validate maze configuration from file.

    Reads configuration file from command-line argument and builds
    a MazeConfig object with validated parameters.

    Returns:
        MazeConfig: Validated maze configuration object.

    Raises:
        SystemExit: If wrong number of arguments or config is invalid.
    """
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

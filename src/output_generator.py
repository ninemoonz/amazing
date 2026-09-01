"""Maze output file generation.

Provides functionality to write generated maze data and solutions
to disk in the required hexadecimal format.
"""

from typing import TYPE_CHECKING
from src.validate_and_build import MazeConfig

if TYPE_CHECKING:
    from maze_generator import MazeCell


def output_gen(maze_txt: "list[list[MazeCell]]",
               maze_config: MazeConfig,
               route: str = "") -> None:
    """Write maze grid and solution to output file.

    Writes the maze in hexadecimal format (one cell per hex digit),
    followed by entry point, exit point, and optional solution route.

    Args:
        maze_txt: 2D grid of MazeCell objects from generator.
        maze_config: Configuration object with output path and coordinates.
        route: Optional shortest path string (e.g. 'ENWSE') to write.
    """
    with open(maze_config.output_file, "w") as f:
        for row in maze_txt:
            for element in row:
                f.write(f"{element.cell_value:x}")
            f.write("\n")
        f.write("\n")
        f.write(f"{maze_config.entry_point[0]},"
                f"{maze_config.entry_point[1]}\n")
        f.write(f"{maze_config.exit_point[0]},"
                f"{maze_config.exit_point[1]}\n")
        if route:
            f.write(f"{route}\n")

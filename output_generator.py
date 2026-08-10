from typing import TYPE_CHECKING
from validate_and_build import MazeConfig

if TYPE_CHECKING:
    from maze_generator import MazeCell


def output_gen(maze_txt: "list[list[MazeCell]]",
               maze_config: MazeConfig) -> None:
    with open("maze.txt", "w") as f:
        for row in maze_txt:
            for element in row:
                f.write(f"{element.cell_value:x}")
            f.write("\n")
        f.write("\n")
        f.write(f"{maze_config.entry_point[0]},"
                f"{maze_config.entry_point[1]}\n")
        f.write(f"{maze_config.exit_point[0]},"
                f"{maze_config.exit_point[1]}")

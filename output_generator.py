from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maze_generator import MazeCell


def output_gen(maze_txt: "list[list[MazeCell]]") -> None:
    with open("maze.txt", "w") as f:
        for row in maze_txt:
            for element in row:
                f.write(f"{element.cell_value:x}")
            f.write("\n")

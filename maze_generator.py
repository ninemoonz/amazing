from validate_and_build import MazeConfig
import random


class MazeGen:
    def __init__(self, width: int, height: int, entry_point: tuple[int, int],
                 exit_point: tuple[int, int], seed: int = 0) -> None:
        self.width = width
        self.height = height
        self.maze_list: list[list[int]] = []

    def make_maze(self) -> None:
        for _ in range(self.height):
            row_list: list[int] = []
            for _ in range(self.width):
                row_list.append(15)
            self.maze_list.append(row_list)

    def print_maze(self) -> None:
        for element in self.maze_list:
            print(element)
            print()


def generator(maze_info: MazeConfig) -> None:
    width: int = maze_info.width
    height: int = maze_info.height
    new_maze: MazeGen = MazeGen(width, height)
    new_maze.make_maze()
    new_maze.print_maze()

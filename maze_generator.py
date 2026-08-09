from validate_and_build import MazeConfig
import random


class MazeCell:
    def __init__(self, coordinates: tuple[int, int]) -> None:
        self.coordinates = coordinates
        self.visited: bool = False
        self.north_wall: int = 1
        self.east_wall: int = 2
        self.south_wall: int = 4
        self.west_wall: int = 8
        self.cell_value: int = (self.north_wall + self.east_wall
                                + self.south_wall + self.west_wall)
        self.north_neighbor: "MazeCell | None" = None
        self.east_neighbor: "MazeCell | None" = None
        self.south_neighbor: "MazeCell | None" = None
        self.west_neighbor: "MazeCell | None" = None

    def show_status(self) -> None:
        print(f"Coordination: {self.coordinates}")
        print(f"Visit status: {self.visited}")
        print(f"Value of this cell: {self.cell_value}")


class MazeGen:
    def __init__(self, width: int, height: int,
                 entry_point: tuple[int, int],
                 exit_point: tuple[int, int],
                 seed: int = 0) -> None:
        self.width = width
        self.height = height
        self.entry_point = entry_point
        self.exit_point = exit_point
        self.maze_list: list[list[MazeCell]] = []

    def gen_grid(self) -> None:
        for y in range(self.height):
            row_list: list[MazeCell] = []
            for x in range(self.width):
                coordinate: tuple = (x, y)
                row_list.append(MazeCell(coordinate))
            self.maze_list.append(row_list)

    def print_grid(self) -> None:
        for element in self.maze_list:
            for status in element:
                print(status.show_status())


def generator(maze_info: MazeConfig) -> None:
    width: int = maze_info.width
    height: int = maze_info.height
    entry_p: tuple[int, int] = maze_info.entry_point
    exit_p: tuple[int, int] = maze_info.exit_point
    new_maze: MazeGen = MazeGen(width, height, entry_p, exit_p)
    new_maze.gen_grid()
    new_maze.print_grid()

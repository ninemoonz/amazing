from validate_and_build import MazeConfig
from output_generator import output_gen
import random


class MazeCell:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, coordinates: tuple[int, int]) -> None:
        self.coordinates = coordinates
        self.visited: bool = False
        self.cell_value: int = (MazeCell.NORTH + MazeCell.EAST +
                                MazeCell.SOUTH + MazeCell.WEST)
        self.north_neighbor: "MazeCell | None" = None
        self.east_neighbor: "MazeCell | None" = None
        self.south_neighbor: "MazeCell | None" = None
        self.west_neighbor: "MazeCell | None" = None

    def show_status(self) -> None:
        print(f"Coordination: {self.coordinates}")
        print(f"Visit status: {self.visited}")
        print(f"Value of this cell: {self.cell_value}")


class MazeGen:
    OPPOSITE: dict = {
        MazeCell.NORTH: MazeCell.SOUTH,
        MazeCell.SOUTH: MazeCell.NORTH,
        MazeCell.EAST: MazeCell.WEST,
        MazeCell.WEST: MazeCell.EAST
    }

    def __init__(self, width: int, height: int,
                 entry_point: tuple[int, int],
                 exit_point: tuple[int, int],
                 seed_value: int = 0) -> None:
        self.width = width
        self.height = height
        self.entry_point = entry_point
        self.exit_point = exit_point
        self.maze_list: list[list[MazeCell]] = []
        self.seed_value = seed_value

    def gen_grid(self) -> None:
        for y in range(self.height):
            row_list: list[MazeCell] = []
            for x in range(self.width):
                coordinate: tuple = (x, y)
                row_list.append(MazeCell(coordinate))
            self.maze_list.append(row_list)

    def link_cells(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze_list[y][x]
                if y > 0:
                    cell.north_neighbor = self.maze_list[y - 1][x]
                if y < self.height - 1:
                    cell.south_neighbor = self.maze_list[y + 1][x]
                if x > 0:
                    cell.west_neighbor = self.maze_list[y][x - 1]
                if x < self.width - 1:
                    cell.east_neighbor = self.maze_list[y][x + 1]

    def carve_maze(self) -> None:
        rng = random.Random(self.seed_value)
        start = self.maze_list[self.entry_point[1]][self.entry_point[0]]
        start.visited = True
        visit_stack: list[MazeCell] = [start]

        while visit_stack:
            current = visit_stack[-1]  # last element stored in this lits.
            neighbors: list[tuple[int, MazeCell]] = []
            if (current.north_neighbor is not None and
                    not current.north_neighbor.visited):
                neighbors.append((MazeCell.NORTH, current.north_neighbor))
            if (current.south_neighbor is not None and
                    not current.south_neighbor.visited):
                neighbors.append((MazeCell.SOUTH, current.south_neighbor))
            if (current.east_neighbor is not None and
                    not current.east_neighbor.visited):
                neighbors.append((MazeCell.EAST, current.east_neighbor))
            if (current.west_neighbor is not None and
                    not current.west_neighbor.visited):
                neighbors.append((MazeCell.WEST, current.west_neighbor))
            if not neighbors:
                visit_stack.pop()
                continue
            direction, next_cell = rng.choice(neighbors)
            current.cell_value &= ~direction
            next_cell.cell_value &= ~self.OPPOSITE[direction]
            next_cell.visited = True
            visit_stack.append(next_cell)

    # def braid_maze(self) -> None:
    #     rng = random.Random(self.seed_value)
    #     for row in self.maze_list:
    #         for cell in row:
    #             if bin(cell.cell_value).count("1") == 3:
    #                 if cell.coordinates[0] > 0 and cell.coordinates[0] < self.width - 1:


def generator(maze_info: MazeConfig) -> None:
    width: int = maze_info.width
    height: int = maze_info.height
    entry_p: tuple[int, int] = maze_info.entry_point
    exit_p: tuple[int, int] = maze_info.exit_point
    new_maze: MazeGen = MazeGen(width, height, entry_p, exit_p, maze_info.seed)
    new_maze.gen_grid()
    new_maze.link_cells()
    new_maze.carve_maze()
    new_maze.braid_maze()
    output_gen(new_maze.maze_list, maze_info)

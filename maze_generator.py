from validate_and_build import MazeConfig
import error_class
import random


class MazeCell:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, coordinates: tuple[int, int]) -> None:
        self.coordinates = coordinates
        self.is_sign: bool = False
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
    """
    MazeGen class is constructed and designed to store
    1. attributes to make maze (data from config values)
    2. methods to generate maze
    3. hard coded data to reach for opposite direction
    4. hard coded data to put 42 sign in the center of the maze.
    """
    OPPOSITE: dict = {
        MazeCell.NORTH: MazeCell.SOUTH,
        MazeCell.SOUTH: MazeCell.NORTH,
        MazeCell.EAST: MazeCell.WEST,
        MazeCell.WEST: MazeCell.EAST
    }

    FORTY_TWO: list[list[int]] = [[1, 0, 0, 0, 1, 1, 1],
                                  [1, 0, 0, 0, 0, 0, 1],
                                  [1, 1, 1, 0, 1, 1, 1],
                                  [0, 0, 1, 0, 1, 0, 0],
                                  [0, 0, 1, 0, 1, 1, 1]]

    """
    width: width of the maze (number of elements in a row)
    height: height of the maze (number of rows)
    """
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

    def forty_two(self, sign: list[list[int]]) -> None:
        if self.width < len(sign[0]) or self.height < len(sign):
            raise error_class.OffsetError("Grid too small to put sign")
        ox = (self.width - len(sign[0])) // 2
        oy = (self.height - len(sign)) // 2
        for ry, row in enumerate(self.FORTY_TWO):
            for rx, value in enumerate(row):
                if value == 1:
                    self.maze_list[oy + ry][ox + rx].visited = True
                    self.maze_list[oy + ry][ox + rx].is_sign = True

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

    def braid_maze(self) -> None:
        rng = random.Random(self.seed_value)
        for row in self.maze_list:
            for cell in row:
                if bin(cell.cell_value).count("1") == 3:
                    candidates: list[tuple[int, MazeCell]] = []
                    if (cell.north_neighbor is not None and
                            cell.cell_value & MazeCell.NORTH and not
                            cell.north_neighbor.is_sign):
                        candidates.append((MazeCell.NORTH,
                                           cell.north_neighbor))
                    if (cell.east_neighbor is not None and
                            cell.cell_value & MazeCell.EAST and not
                            cell.east_neighbor.is_sign):
                        candidates.append((MazeCell.EAST,
                                           cell.east_neighbor))
                    if (cell.south_neighbor is not None and
                            cell.cell_value & MazeCell.SOUTH and not
                            cell.south_neighbor.is_sign):
                        candidates.append((MazeCell.SOUTH,
                                           cell.south_neighbor))
                    if (cell.west_neighbor is not None and
                            cell.cell_value & MazeCell.WEST and not
                            cell.west_neighbor.is_sign):
                        candidates.append((MazeCell.WEST,
                                           cell.west_neighbor))
                    if not candidates:
                        continue
                    if not cell.is_sign:
                        direction, next_cell = rng.choice(candidates)
                        cell.cell_value &= ~direction
                        next_cell.cell_value &= ~self.OPPOSITE[direction]

    def open_corridor_check(self, cx: int, cy: int) -> bool:
        for dy in range(3):
            for dx in range(3):
                cell = self.maze_list[cy + dy][cx + dx]
                if dx < 2 and cell.cell_value & MazeCell.EAST:
                    return False
                if dy < 2 and cell.cell_value & MazeCell.SOUTH:
                    return False
        return True


def generator(maze_info: MazeConfig) -> list[list[MazeCell]]:
    width: int = maze_info.width
    height: int = maze_info.height
    entry_p: tuple[int, int] = maze_info.entry_point
    exit_p: tuple[int, int] = maze_info.exit_point
    new_maze: MazeGen = MazeGen(width, height, entry_p, exit_p, maze_info.seed)
    new_maze.gen_grid()
    new_maze.link_cells()
    new_maze.forty_two(MazeGen.FORTY_TWO)
    new_maze.carve_maze()
    if not maze_info.perfect:
        new_maze.braid_maze()
    return new_maze.maze_list

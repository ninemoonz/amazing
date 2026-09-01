"""Maze generation and path-finding engine.

Provides a standalone maze generator using depth-first search with
optional loop braiding, plus integrated BFS shortest-path solver.
No external dependencies beyond Python standard library.
"""

import random
from collections import deque


class OffsetError(Exception):
    """Raised when maze dimensions are too small for required patterns."""

    pass


class MazeCell:
    """Represents a single cell in the maze grid.

    Each cell stores its coordinate, wall bitmask, neighbor references,
    and metadata for generation and rendering.

    Attributes:
        NORTH: Bitmask value 1 for north wall.
        EAST: Bitmask value 2 for east wall.
        SOUTH: Bitmask value 4 for south wall.
        WEST: Bitmask value 8 for west wall.
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, coordinates: tuple[int, int]) -> None:
        """Initialize a maze cell.

        Args:
            coordinates: (x, y) tuple position in maze grid.
        """
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
        """Print debug information about this cell."""
        print(f"Coordination: {self.coordinates}")
        print(f"Visit status: {self.visited}")
        print(f"Value of this cell: {self.cell_value}")


class MazeGen:
    """A maze generator and solver, usable standalone with no external
    dependencies beyond the Python standard library.

    Basic usage:

        from maze_generator import MazeGen

        maze = MazeGen(width=10, height=10,
                        entry_point=(0, 0), exit_point=(9, 9),
                        seed_value=42)
        maze.gen_grid()
        maze.link_cells()
        maze.forty_two(MazeGen.FORTY_TWO)
        maze.carve_maze()

    Custom parameters (passed to __init__):
        width, height  -- size of the maze grid
        entry_point    -- (x, y) tuple, where the maze starts
        exit_point     -- (x, y) tuple, where the maze ends
        seed_value     -- controls randomness; same seed -> same maze

    Accessing the generated structure:
        maze.maze_list is a list[list[MazeCell]] grid. Each MazeCell
        has a cell_value (0-15) whose bits mark which walls are
        closed: 1=North, 2=East, 4=South, 8=West.

            cell = maze.maze_list[y][x]
            print(cell.cell_value)

    Accessing a solution:
        route = maze.find_path()
        # A string of moves (e.g. "EESSWW") from entry_point to
        # exit_point, or "" if no path exists.
    """

    OPPOSITE: dict[int, int] = {
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

    def __init__(self, width: int, height: int,
                 entry_point: tuple[int, int],
                 exit_point: tuple[int, int],
                 seed_value: int = 0) -> None:
        """Initialize maze generator with dimensions and entry/exit.

        Args:
            width: Maze grid width in cells.
            height: Maze grid height in cells.
            entry_point: (x, y) coordinate for maze start.
            exit_point: (x, y) coordinate for maze end.
            seed_value: Random seed for reproducible generation.
        """
        self.width = width
        self.height = height
        self.entry_point = entry_point
        self.exit_point = exit_point
        self.maze_list: list[list[MazeCell]] = []
        self.seed_value = seed_value

    def gen_grid(self) -> None:
        """Generate initial maze grid with all walls present."""
        for y in range(self.height):
            row_list: list[MazeCell] = []
            for x in range(self.width):
                coordinate: tuple[int, int] = (x, y)
                row_list.append(MazeCell(coordinate))
            self.maze_list.append(row_list)

    def forty_two(self, sign: list[list[int]]) -> None:
        """Mark cells to form the 42 school logo pattern.

        Args:
            sign: 2D pattern array where 1 marks cells to fill.

        Raises:
            OffsetError: If maze is too small for the sign pattern.
        """
        if self.width < len(sign[0]) or self.height < len(sign):
            raise OffsetError("Grid too small to put sign")
        ox = (self.width - len(sign[0])) // 2
        oy = (self.height - len(sign)) // 2
        for ry, row in enumerate(self.FORTY_TWO):
            for rx, value in enumerate(row):
                if value == 1:
                    self.maze_list[oy + ry][ox + rx].visited = True
                    self.maze_list[oy + ry][ox + rx].is_sign = True

    def link_cells(self) -> None:
        """Establish neighbor relationships between adjacent cells."""
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
        """Generate maze passages using depth-first search algorithm.

        Starts from entry point and recursively carves passages through
        unvisited cells, creating a spanning tree of the grid.
        """
        rng = random.Random(self.seed_value)
        start = self.maze_list[self.entry_point[1]][self.entry_point[0]]
        start.visited = True
        visit_stack: list[MazeCell] = [start]

        while visit_stack:
            current = visit_stack[-1]
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
        """Remove dead ends to create loops (non-perfect maze).

        Adds optional passages to cells with only one exit,
        creating multiple paths between points.
        """
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

    def corridor_check(self, cx: int, cy: int) -> bool:
        """Check if a 3x3 region contains an open corridor.

        Args:
            cx: Top-left x coordinate of region.
            cy: Top-left y coordinate of region.

        Returns:
            bool: True if region is a valid corridor.
        """
        for dy in range(3):
            for dx in range(3):
                cell = self.maze_list[cy + dy][cx + dx]
                if dx < 2 and cell.cell_value & MazeCell.EAST:
                    return False
                if dy < 2 and cell.cell_value & MazeCell.SOUTH:
                    return False
        return True

    def corridor_fix(self) -> None:
        """Ensure no 3x3 regions form complete corridors.

        Prevents unintended long straight passages in the maze.
        """
        rng = random.Random(self.seed_value)
        for cy in range(self.height - 2):
            for cx in range(self.width - 2):
                if not self.corridor_check(cx, cy):
                    continue
                walls: list[tuple[MazeCell, MazeCell, int]] = []
                for dy in range(3):
                    for dx in range(3):
                        cell = self.maze_list[cy + dy][cx + dx]
                        if dx < 2:
                            east_cell = self.maze_list[cy + dy][cx + dx + 1]
                            walls.append((cell, east_cell, MazeCell.EAST))
                        if dy < 2:
                            south_cell = self.maze_list[cy + dy + 1][cx + dx]
                            walls.append((cell, south_cell, MazeCell.SOUTH))
                cell, neighbor, direction = rng.choice(walls)
                cell.cell_value |= direction
                neighbor.cell_value |= self.OPPOSITE[direction]

    def find_path(self) -> str:
        """Find shortest path from entry to exit using BFS.

        Returns:
            str: Route as moves ('N', 'E', 'S', 'W') or empty string if
                 no path exists.
        """
        height = len(self.maze_list)
        width = len(self.maze_list[0]) if height else 0

        queue = deque([self.entry_point])
        visited = {self.entry_point}
        came_from: dict[tuple[int, int],
                        tuple[int, int] | None] = {self.entry_point: None}
        move_taken: dict[tuple[int, int], str] = {}

        while queue:
            x, y = queue.popleft()

            if (x, y) == self.exit_point:
                break

            for direction, dx, dy, current_bit, neighbor_bit in (
                ("N", 0, -1, MazeCell.NORTH, MazeCell.SOUTH),
                ("E", 1, 0, MazeCell.EAST, MazeCell.WEST),
                ("S", 0, 1, MazeCell.SOUTH, MazeCell.NORTH),
                ("W", -1, 0, MazeCell.WEST, MazeCell.EAST),
            ):
                nx = x + dx
                ny = y + dy

                if not (0 <= nx < width and 0 <= ny < height):
                    continue
                if (nx, ny) in visited:
                    continue

                current = self.maze_list[y][x]
                neighbor = self.maze_list[ny][nx]

                if current.cell_value & current_bit:
                    continue
                if neighbor.cell_value & neighbor_bit:
                    continue

                visited.add((nx, ny))
                came_from[(nx, ny)] = (x, y)
                move_taken[(nx, ny)] = direction
                queue.append((nx, ny))

        if self.exit_point not in came_from:
            return ""

        route: list[str] = []
        node = self.exit_point
        while came_from[node] is not None:
            route.append(move_taken[node])
            next_node = came_from[node]
            assert next_node is not None
            node = next_node
        route.reverse()
        return "".join(route)

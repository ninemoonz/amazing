from collections import deque

from maze_generator import MazeCell


def find_path(maze: list[list[MazeCell]], start: tuple[int, int], goal: tuple[int, int]) -> str:
    height = len(maze)
    width = len(maze[0]) if height else 0

    queue = deque([start])
    visited = {start}
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    move_taken: dict[tuple[int, int], str] = {}

    while queue:
        x, y = queue.popleft()

        if (x, y) == goal:
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

            current = maze[y][x]
            neighbor = maze[ny][nx]

            if current.cell_value & current_bit:
                continue
            if neighbor.cell_value & neighbor_bit:
                continue

            visited.add((nx, ny))
            came_from[(nx, ny)] = (x, y)
            move_taken[(nx, ny)] = direction
            queue.append((nx, ny))

    if goal not in came_from:
        return ""

    route: list[str] = []
    current = goal
    while came_from[current] is not None:
        route.append(move_taken[current])
        current = came_from[current]
    route.reverse()
    return "".join(route)

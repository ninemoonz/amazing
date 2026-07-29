from validate_and_build import MazeConfig


class MazeGen:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.row_list: list[str] = []
        self.maze_list: list[list[str]] = []

    def make_maze(self):
        for _ in range(self.width):
            self.row_list.append("F")
        for _ in range(self.height):
            self.maze_list.append(self.row_list)

    def print_maze(self):
        for element in self.maze_list:
            print(element)
            print()


def generator(maze_info: MazeConfig) -> list[list[str]]:
    width: int = maze_info.width
    height: int = maze_info.height
    new_maze: MazeGen = MazeGen(width, height)
    new_maze.make_maze()
    new_maze.print_maze()

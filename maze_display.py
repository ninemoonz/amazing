def read_maze(filename: str) -> list[list[int]]:
    converted_list: list[list[int]] = []
    with open(filename) as f:
        for line in f:
            converted_row: list[int] = []
            stripped = line.strip()
            if stripped == "":
                break
            for ch in stripped:
                converted_row.append(int(ch, 16))
            converted_list.append(converted_row)
    return converted_list


if __name__ == "__main__":
    con_list = read_maze("maze.txt")
    print(con_list)

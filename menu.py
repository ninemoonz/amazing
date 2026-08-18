


while True:
    print("=== A-Maze-Ing ===")
    print("[1] Re-generate a new maze\n"
          "[2] Show/Hide Path from entry to exit\n"
          "[3] Roate maze colors\n"
          "[4] Quit Program\n")
    choice = input("Choice: ")
    if choice == "1":
        print("Re-generate a new maze")
    elif choice == "2":
        print("Show path")
    elif choice == "3":
        print("How to change the colors?")
    elif choice == "4":
        break
    else:
        print(f"{MazeColor.WALL}THIS IS COLOR OF THE WALL")

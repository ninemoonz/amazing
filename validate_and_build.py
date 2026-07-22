REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


class ImplementationError(Exception):
    pass


def key_check(raw: dict[str, str]) -> bool:
    for raw_key in raw:
        for key in REQUIRED_KEYS:
            if raw_key == key:
                return True
    return False


def width_height_check(raw: dict[str, str]) -> None:
    width: int = int(raw["WIDTH"])
    height: int = int(raw["HEIGHT"])
    if width < 0 or height < 0:
        raise ImplementationError("WIDTH and HEIGHT should be positive")


def coordinates_check(raw: dict[str, str]):
    raw_entry: str = raw["ENTRY"].strip()
    raw_exit: str = raw["EXIT"].strip()
    width: int = int(raw["WIDTH"])
    height: int = int(raw["HEIGHT"])
    print(f"raw entry: {raw_entry}")
    print(f"raw exit: {raw_exit}")
    entry_x, entry_y = raw_entry.split(',')
    exit_x, exit_y = raw_exit.split(',')
    entry_x = int(entry_x)
    entry_y = int(entry_y)
    exit_x = int(exit_x)
    exit_y = int(exit_y)
    if entry_x == exit_x and entry_y == exit_y:
        raise ImplementationError("ENTRY and EXIT SHOULD NOT "
                                  "HAVE SAME COORDINATION")
    if entry_x < 0 or entry_x >= width:
        raise ImplementationError("Invalide coordinates")
    if entry_y < 0 or entry_y >= height:
        raise ImplementationError("Invalide coordinates")


def validate_and_build(raw: dict[str, str]) -> dict:
    try:
        key_check(raw)
        width_height_check(raw)
        coordinates_check(raw)
    except ImplementationError as e:
        print(e)

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
    print(f"raw entry: {raw_entry}")
    entry_x, entry_y = raw_entry.split(',')
    entry_x = int(entry_x)
    entry_y = int(entry_y)


def validate_and_build(raw: dict[str, str]) -> dict:
    try:
        key_check(raw)
        width_height_check(raw)
        coordinates_check(raw)
    except ImplementationError as e:
        print(e)

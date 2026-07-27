REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


def key_check(raw: dict[str, str]) -> bool:
    for raw_key in raw:
        for key in REQUIRED_KEYS:
            if raw_key == key:
                return True
    return False


def width_height_check(width: int, height: int) -> None:
    if width < 0 or height < 0:
        raise NotImplementedError


def extract_size(raw: dict[str, str]):
    try:
        width: int = int(raw["WIDTH"])
        height: int = int(raw["HEIGHT"])
    except ValueError as e:
        print(e)
    width_height_check(width, height)
    return width, height


def validate_and_build(raw: dict[str, str]) -> dict:
    try:
        key_check(raw)
        width_height_check(raw)
    except NotImplementedError as e:
        print(e)

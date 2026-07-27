REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


def key_check(raw: dict[str, str]) -> list[str]:
    missing: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in raw:
            missing.append(key)
    return missing


def parse_dimension(raw: dict[str, str], key: str) -> int:
    value_str = raw[key]
    if not value_str.isdigit():
        raise ValueError(f"{key} must be a positive integer, got '{value_str}'")
    value = int(value_str)
    if value <= 0:
        raise ValueError(f"{key} must be greater than 0, got {value}")
    return value


def perfect_check(raw: dict[str, str], key: str) -> bool:
    value_str = raw[key].strip().upper()
    if value_str not in ("TRUE", "FALSE"):
        raise ValueError(f"{key} must be either 'TRUE' or 'FALSE', "
                         f"got {value_str}")
    return value_str == "TRUE"


def dimension_check(raw: dict[str, str], key: str) -> bool:
    ...
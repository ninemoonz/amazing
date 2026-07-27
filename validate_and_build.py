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

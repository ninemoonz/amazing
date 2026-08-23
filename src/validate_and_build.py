from dataclasses import dataclass
from src.error_class import ConfigError

REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


@dataclass(frozen=True)
class MazeConfig:
    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None


def key_check(raw: dict[str, str]) -> list[str]:
    missing: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in raw:
            missing.append(key)
    return missing


def parse_dimension(raw: dict[str, str], key: str) -> int:
    value_str = raw[key]
    if not value_str.isdigit():
        raise ValueError(f"{key} must be a positive integer, "
                         f"got '{value_str}'")
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


def parse_point(raw: dict[str, str],
                key: str, width: str, height: str) -> tuple[int, int]:
    value = raw[key].strip()
    w = parse_dimension(raw, width)
    h = parse_dimension(raw, height)
    parts = value.split(',', 1)
    if len(parts) != 2:
        raise ConfigError(f"{key} must be 'x,y', got '{value}'")
    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError:
        raise ConfigError(f"{key} coordinates must be integers, got '{value}'")
    if not 0 <= x < w or not 0 <= y < h:
        raise ConfigError(f"{key} ({x},{y}) is out of maze bounds "
                          f"({width},{height})")
    return (x, y)


def validate_entry_exit(entry_point: tuple[int, int],
                        exit_point: tuple[int, int]) -> None:
    if entry_point == exit_point:
        raise ConfigError("ENTRY and EXIT must not be the same cell")


def validate_output_file(raw: dict[str, str], key: str) -> str:
    value = raw.get(key, "").strip()
    if value == "":
        raise ConfigError(f"{key} must not be empty")
    return value


def parse_optional_seed(raw: dict[str, str], key: str = "SEED") -> int | None:
    value = raw.get(key, "").strip()
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"SEED must be an integer, got '{value}'")


def build_config(raw: dict[str, str]) -> MazeConfig:
    missing = key_check(raw)
    if missing:
        raise ConfigError(f"Missing required keys: {', '.join(missing)}")
    width: int = parse_dimension(raw, "WIDTH")
    height: int = parse_dimension(raw, "HEIGHT")
    entry_point: tuple[int, int] = parse_point(raw, "ENTRY", "WIDTH", "HEIGHT")
    exit_point: tuple[int, int] = parse_point(raw, "EXIT", "WIDTH", "HEIGHT")
    validate_entry_exit(entry_point, exit_point)
    output_file: str = validate_output_file(raw, "OUTPUT_FILE")
    perfect: bool = perfect_check(raw, "PERFECT")
    seed: int | None = parse_optional_seed(raw)
    return MazeConfig(width, height, entry_point,
                      exit_point, output_file, perfect, seed)

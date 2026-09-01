"""Configuration validation and MazeConfig object construction.

Provides utilities to validate maze configuration parameters from raw
key-value pairs and construct a validated MazeConfig dataclass object.
"""

from dataclasses import dataclass
from src.error_class import ConfigError

REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


@dataclass(frozen=True)
class MazeConfig:
    """Immutable configuration object for maze generation.

    Attributes:
        width: Maze grid width in cells.
        height: Maze grid height in cells.
        entry_point: (x, y) tuple for maze start location.
        exit_point: (x, y) tuple for maze end location.
        output_file: Path to write generated maze to.
        perfect: If True, generate a perfect maze (no loops).
        seed: Random seed for reproducible generation (None for random).
    """

    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None


def key_check(raw: dict[str, str]) -> list[str]:
    """Check for missing required configuration keys.

    Args:
        raw: Raw configuration dictionary.

    Returns:
        list[str]: List of missing required keys, empty if all present.
    """
    missing: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in raw:
            missing.append(key)
    return missing


def parse_dimension(raw: dict[str, str], key: str) -> int:
    """Parse and validate a positive integer dimension.

    Args:
        raw: Configuration dictionary.
        key: Key to extract dimension from.

    Returns:
        int: Validated positive integer value.

    Raises:
        ValueError: If value is not a positive integer.
    """
    value_str = raw[key]
    if not value_str.isdigit():
        raise ValueError(f"{key} must be a positive integer, "
                         f"got '{value_str}'")
    value = int(value_str)
    if value <= 0:
        raise ValueError(f"{key} must be greater than 0, got {value}")
    return value


def perfect_check(raw: dict[str, str], key: str) -> bool:
    """Parse and validate a boolean configuration value.

    Args:
        raw: Configuration dictionary.
        key: Key to extract boolean from.

    Returns:
        bool: True if value is 'TRUE', False if 'FALSE'.

    Raises:
        ValueError: If value is neither 'TRUE' nor 'FALSE'.
    """
    value_str = raw[key].strip().upper()
    if value_str not in ("TRUE", "FALSE"):
        raise ValueError(f"{key} must be either 'TRUE' or 'FALSE', "
                         f"got {value_str}")
    return value_str == "TRUE"


def parse_point(raw: dict[str, str],
                key: str, width: str, height: str) -> tuple[int, int]:
    """Parse and validate a coordinate point.

    Args:
        raw: Configuration dictionary.
        key: Key to extract point from.
        width: Key for maze width (used for bounds checking).
        height: Key for maze height (used for bounds checking).

    Returns:
        tuple[int, int]: (x, y) coordinate within maze bounds.

    Raises:
        ConfigError: If format is invalid or point is out of bounds.
    """
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
    """Validate that entry and exit are different cells.

    Args:
        entry_point: Maze entry coordinate.
        exit_point: Maze exit coordinate.

    Raises:
        ConfigError: If entry and exit are the same location.
    """
    if entry_point == exit_point:
        raise ConfigError("ENTRY and EXIT must not be the same cell")


def validate_output_file(raw: dict[str, str], key: str) -> str:
    """Validate output file path is not empty.

    Args:
        raw: Configuration dictionary.
        key: Key to extract output file from.

    Returns:
        str: Non-empty output file path.

    Raises:
        ConfigError: If output file path is empty.
    """
    value = raw.get(key, "").strip()
    if value == "":
        raise ConfigError(f"{key} must not be empty")
    return value


def parse_optional_seed(raw: dict[str, str], key: str = "SEED") -> int | None:
    """Parse optional random seed value.

    Args:
        raw: Configuration dictionary.
        key: Key to extract seed from (default 'SEED').

    Returns:
        int | None: Seed value if present, None if absent or empty.

    Raises:
        ConfigError: If seed value is not a valid integer.
    """
    value = raw.get(key, "").strip()
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"SEED must be an integer, got '{value}'")


def build_config(raw: dict[str, str]) -> MazeConfig:
    """Build and validate a complete MazeConfig object.

    Args:
        raw: Raw configuration dictionary from file parsing.

    Returns:
        MazeConfig: Fully validated configuration object.

    Raises:
        ConfigError: If any required key is missing or value is invalid.
    """
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

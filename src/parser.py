"""Configuration file parser for maze settings.

This module provides utilities to parse key-value configuration files
with support for comments and whitespace handling.
"""

from src.error_class import ConfigError


def parse_config(file_name: str) -> dict[str, str]:
    """Parse key-value configuration file.

    Reads a configuration file with KEY=VALUE format, ignoring empty
    lines and lines starting with '#'. Raises ConfigError if any line
    does not follow the expected format.

    Args:
        file_name: Path to configuration file to parse.

    Returns:
        dict[str, str]: Parsed configuration as key-value pairs.

    Raises:
        ConfigError: If a line has incorrect syntax (missing '=').
    """
    config: dict[str, str] = {}
    with open(file_name) as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if line == "" or line.startswith("#"):
                continue
            if "=" not in line:
                raise ConfigError(f"Bad syntax on line {line_number}: {line}")
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config

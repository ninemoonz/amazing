"""Maze application package.

Exports public API for configuration parsing, validation, and
menu-driven user interface.
"""

from src.parser import parse_config
from src.validate_and_build import build_config, MazeConfig
from src.error_class import ConfigError
from src.menu import menu_func


__all__ = ["parse_config", "build_config",
           "MazeConfig", "ConfigError", "menu_func"]

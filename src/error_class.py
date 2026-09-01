"""Custom exception classes for the maze application.

Defines specialized exception types for configuration, path-finding,
and offset errors specific to maze generation and solving.
"""


class ConfigError(Exception):
    """Raised when configuration parsing or validation fails."""

    pass


class OffsetError(Exception):
    """Raised when maze dimensions are too small for required patterns."""

    pass


class PathFindingError(Exception):
    """Raised when path-finding encounters invalid maze state."""

    pass

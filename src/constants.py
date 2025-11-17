"""
Simulation Constants

CARLA simulation infrastructure constants.
Only enum-like type identifiers and protocol constants are kept here.
All configurable values have been moved to config.yaml (common or module-specific).

Use ConfigManager.load() to access configuration values.
"""


class MessageTopics:
    """ZMQ message topic identifiers (protocol constants)."""

    FRAME = b'frame'
    DETECTION = b'detection'
    STATE = b'state'
    ACTION = b'action'


class ActionTypes:
    """Action type identifiers for event system."""

    RESPAWN = "respawn"
    PAUSE = "pause"
    RESUME = "resume"
    QUIT = "quit"


# Convenience exports
__all__ = [
    'MessageTopics',
    'ActionTypes',
]

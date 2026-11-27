"""Game configuration: loading from a JSON file and validation."""

import json
import sys
from typing import Any


class ConfigParser:
    """Validated game configuration with safe defaults."""

    lives: int
    pacgum: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: int
    level_max_time: int
    highscore_filename: str
    levels: list[dict[str, int]]

    MIN_LEVELS: int = 10
    DEFAULT_HIGHSCORE: str = "highscores.json"

    # key: (default, min, max)
    INT_RULES: dict[str, tuple[int, int, int]] = {
        "lives": (3, 1, 99),
        "pacgum": (42, 1, 10000),
        "points_per_pacgum": (10, 0, 100000),
        "points_per_super_pacgum": (50, 0, 100000),
        "points_per_ghost": (200, 0, 100000),
        "seed": (42, 0, 2**32 - 1),
        "level_max_time": (90, 10, 3600),
    }

    LEVEL_RULES: dict[str, tuple[int, int, int]] = {
        "width": (15, 5, 51),
        "height": (15, 5, 51),
    }

    def __init__(self, data: Any = None) -> None:
        """Initialize the configuration with validated values."""
        if not isinstance(data, dict):
            self._warn("Config root must be an object, using defaults")
            data = {}

        filename = data.get("highscore_filename")

        if isinstance(filename, str) and filename.strip():
            self.highscore_filename = filename.strip()
        else:
            self._warn(
                "Invalid 'highscore_filename', "
                f"using '{self.DEFAULT_HIGHSCORE}'"
            )
            self.highscore_filename = self.DEFAULT_HIGHSCORE

        for key, limits in self.INT_RULES.items():
            value = self._validate_int(data.get(key), key, limits)
            setattr(self, key, value)

        self.levels = self._validate_levels(data.get("levels"))

    @classmethod
    def from_file(cls, path: str) -> "ConfigParser":
        """Load a JSON configuration file and handle loading errors."""
        if not path.lower().endswith(".json"):
            raise ValueError("Expected a JSON file.")
        try:
            with open(path, encoding="utf-8") as file:
                cleaned = "".join(
                    "\n" if line.lstrip().startswith(("#", "//"))
                    else line
                    for line in file)

            data = json.loads(cleaned)

        except OSError as error:
            raise ValueError(f"Cannot open configuration file: {error}"
                             ) from error

        except (ValueError, RecursionError) as error:
            cls._warn(f"Invalid configuration content ({error}), "
                      f"using defaults")
            data = {}

        return cls(data)

    @staticmethod
    def _warn(message: str) -> None:
        """Write a configuration warning to standard error."""
        print(f"Warning: {message}", file=sys.stderr)

    @classmethod
    def _validate_int(
        cls,
        value: Any,
        name: str,
        limits: tuple[int, int, int]
    ) -> int:
        """Validate an integer and clamp it to safe bounds."""
        default, low, high = limits

        if isinstance(value, bool) or not isinstance(value, int):
            cls._warn(
                f"'{name}' missing or not an int, using {default}")
            return default

        if not low <= value <= high:
            clamped = max(low, min(high, value))

            cls._warn(
                f"'{name}' out of bounds [{low}, {high}], "
                f"clamped to {clamped}")
            return clamped

        return value

    @classmethod
    def _default_level(cls) -> dict[str, int]:
        """Create a level using the default dimensions."""
        return {
            key: limits[0]
            for key, limits in cls.LEVEL_RULES.items()
        }

    @classmethod
    def _validate_levels(cls, raw: Any) -> list[dict[str, int]]:
        """Validate level dimensions and ensure a minimum of ten levels."""
        if not isinstance(raw, list):
            cls._warn("'levels' missing or invalid, using defaults")
            raw = []

        levels: list[dict[str, int]] = []

        for i, item in enumerate(raw):
            if not isinstance(item, dict):
                cls._warn(
                    f"Level[{i}] invalid, using default dimensions")
                levels.append(cls._default_level())
                continue

            levels.append({
                key: cls._validate_int(
                    item.get(key),
                    f"levels[{i}].{key}",
                    limits)
                for key, limits in cls.LEVEL_RULES.items()})

        if len(levels) < cls.MIN_LEVELS:
            missing = cls.MIN_LEVELS - len(levels)

            cls._warn(
                f"At least {cls.MIN_LEVELS} levels required, "
                f"adding {missing} default levels")

            for _ in range(missing):
                levels.append(cls._default_level())

        return levels

"""Configuration utility functions for loading, saving, and merging configs.

Supports JSON config files with type-safe operations, atomic writes,
schema validation, and flexible deep-merge strategies.
"""

from __future__ import annotations

import json
import os
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any, Union

ConfigDict = dict[str, Any]
PathLike = Union[str, Path]


class ConfigError(Exception):
    """Base exception for configuration errors."""


class ConfigLoadError(ConfigError):
    """Raised when a config file cannot be loaded."""


class ConfigValidationError(ConfigError):
    """Raised when a config fails schema validation."""


# ── Loading ──────────────────────────────────────────────────────────────


def load_config(path: PathLike, *, default: ConfigDict | None = None) -> ConfigDict:
    """Load a JSON configuration file and return it as a dictionary.

    Args:
        path: Path to the JSON config file.
        default: If provided, return this dict instead of raising when the
                 file does not exist.

    Returns:
        The parsed configuration dictionary.

    Raises:
        ConfigLoadError: If the file cannot be read or parsed (and no
                         *default* was given for missing files).

    >>> import tempfile, os
    >>> p = tempfile.mktemp(suffix=".json")
    >>> save_config(p, {"key": "value"})
    >>> load_config(p)
    {'key': 'value'}
    >>> os.unlink(p)
    """
    path = Path(path)
    if not path.exists():
        if default is not None:
            return deepcopy(default)
        raise ConfigLoadError(f"Config file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ConfigLoadError(f"Invalid JSON in {path}: {exc}") from exc
    except OSError as exc:
        raise ConfigLoadError(f"Cannot read {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigLoadError(
            f"Expected a JSON object at root, got {type(data).__name__}"
        )
    return data


# ── Saving ───────────────────────────────────────────────────────────────


def save_config(
    path: PathLike,
    data: ConfigDict,
    *,
    atomic: bool = True,
    indent: int = 2,
) -> None:
    """Save a dictionary as a JSON configuration file.

    Uses atomic write by default (temp file + rename) to prevent
    corruption on crash.

    Args:
        path: Destination file path.
        data: Dictionary to serialize.
        atomic: Write atomically via temp file + rename (default True).
        indent: JSON indentation level.

    Raises:
        TypeError: If *data* is not a dictionary.
    """
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict, got {type(data).__name__}")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    content = json.dumps(data, indent=indent, ensure_ascii=False) + "\n"

    if atomic:
        fd, tmp_path = tempfile.mkstemp(
            dir=path.parent, prefix=".cfg_", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(content)
            os.replace(tmp_path, path)
        except BaseException:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


# ── Merging ──────────────────────────────────────────────────────────────


def merge_configs(
    base: ConfigDict,
    override: ConfigDict,
    *,
    list_strategy: str = "replace",
) -> ConfigDict:
    """Deep-merge two configuration dictionaries.

    Values from *override* take precedence. Nested dicts are merged
    recursively; list handling is controlled by *list_strategy*.

    Args:
        base: Base configuration dict.
        override: Override configuration dict.
        list_strategy: How to handle list values —
            ``"replace"`` (default): override replaces base.
            ``"append"``: concatenate base + override lists.
            ``"unique"``: concatenate and deduplicate (order-preserving).

    Returns:
        A new merged dictionary (inputs are never mutated).

    Raises:
        ValueError: If *list_strategy* is not recognized.

    >>> merge_configs({"a": 1, "b": {"x": 1}}, {"b": {"y": 2}, "c": 3})
    {'a': 1, 'b': {'x': 1, 'y': 2}, 'c': 3}
    >>> merge_configs({"t": [1, 2]}, {"t": [2, 3]}, list_strategy="unique")
    {'t': [1, 2, 3]}
    """
    valid_strategies = ("replace", "append", "unique")
    if list_strategy not in valid_strategies:
        raise ValueError(
            f"Unknown list_strategy {list_strategy!r}, expected one of {valid_strategies}"
        )

    merged = deepcopy(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_configs(
                merged[key], value, list_strategy=list_strategy
            )
        elif (
            key in merged
            and isinstance(merged[key], list)
            and isinstance(value, list)
            and list_strategy != "replace"
        ):
            if list_strategy == "append":
                merged[key] = merged[key] + deepcopy(value)
            else:  # unique
                seen: set[Any] = set()
                result: list[Any] = []
                for item in merged[key] + value:
                    h = _make_hashable(item)
                    if h not in seen:
                        seen.add(h)
                        result.append(item)
                merged[key] = result
        else:
            merged[key] = deepcopy(value)
    return merged


# ── Validation ───────────────────────────────────────────────────────────


def validate_config(
    data: ConfigDict,
    required_keys: list[str] | None = None,
    schema: ConfigDict | None = None,
) -> list[str]:
    """Validate a config dict and return a list of error messages.

    Args:
        data: The configuration to validate.
        required_keys: Top-level keys that must be present.
        schema: A simple type-schema dict, e.g.
                ``{"port": int, "name": str}``.

    Returns:
        A list of human-readable error strings (empty means valid).

    Raises:
        ConfigValidationError: When called via ``validate_config_strict``.

    >>> validate_config({"port": "bad"}, schema={"port": int})
    ["Key 'port': expected int, got str"]
    """
    errors: list[str] = []
    for key in required_keys or []:
        if key not in data:
            errors.append(f"Missing required key: '{key}'")
    for key, expected_type in (schema or {}).items():
        if key in data and not isinstance(data[key], expected_type):
            actual = type(data[key]).__name__
            errors.append(
                f"Key '{key}': expected {expected_type.__name__}, got {actual}"
            )
    return errors


def validate_config_strict(
    data: ConfigDict,
    required_keys: list[str] | None = None,
    schema: ConfigDict | None = None,
) -> None:
    """Like :func:`validate_config` but raises on first error."""
    errors = validate_config(data, required_keys=required_keys, schema=schema)
    if errors:
        raise ConfigValidationError("; ".join(errors))


# ── Internal helpers ─────────────────────────────────────────────────────


def _make_hashable(obj: Any) -> Any:
    """Best-effort conversion to a hashable representation for dedup."""
    if isinstance(obj, dict):
        return tuple(sorted((k, _make_hashable(v)) for k, v in obj.items()))
    if isinstance(obj, (list, tuple)):
        return tuple(_make_hashable(i) for i in obj)
    return obj


# ── CLI demo ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    base: ConfigDict = {
        "app": {"name": "MyApp", "debug": False, "tags": ["v1"]},
        "version": 1,
    }
    override: ConfigDict = {
        "app": {"debug": True, "port": 8080, "tags": ["v2"]},
        "author": "vlbeau",
    }

    print("── merge (replace lists) ──")
    print(json.dumps(merge_configs(base, override), indent=2))

    print("\n── merge (unique lists) ──")
    print(json.dumps(merge_configs(base, override, list_strategy="unique"), indent=2))

    print("\n── validation ──")
    errors = validate_config(
        {"port": "bad", "name": "App"},
        required_keys=["port", "name", "secret"],
        schema={"port": int, "name": str},
    )
    for e in errors:
        print(f"  ⚠ {e}")

    print("\n── atomic save / load round-trip ──")
    demo_path = Path("/tmp/_config_demo.json")
    save_config(demo_path, base)
    loaded = load_config(demo_path)
    print(f"  Round-trip OK: {loaded == base}")
    demo_path.unlink()

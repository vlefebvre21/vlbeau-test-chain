"""Configuration utility functions for loading, saving, and merging configs."""

import json
import os


def load_config(path):
    """Load a JSON configuration file and return it as a dictionary.

    Args:
        path: Path to the JSON config file.

    Returns:
        dict: The parsed configuration.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(path, data):
    """Save a dictionary as a JSON configuration file.

    Args:
        path: Destination file path.
        data: Dictionary to serialize.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def merge_configs(base, override):
    """Deep-merge two configuration dictionaries.

    Values from *override* take precedence. Nested dicts are merged
    recursively; all other types are replaced.

    Args:
        base: Base configuration dict.
        override: Override configuration dict.

    Returns:
        dict: A new merged dictionary.
    """
    merged = base.copy()
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    return merged


if __name__ == "__main__":
    import tempfile

    base = {"app": {"name": "MyApp", "debug": False}, "version": 1}
    override = {"app": {"debug": True, "port": 8080}, "author": "vlbeau"}

    print("Base config:", json.dumps(base, indent=2))
    print("Override:", json.dumps(override, indent=2))
    print("Merged:", json.dumps(merge_configs(base, override), indent=2))

    # Round-trip demo
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as tmp:
        tmp_path = tmp.name
    save_config(tmp_path, base)
    loaded = load_config(tmp_path)
    print(f"Save/Load round-trip OK: {loaded == base}")
    os.unlink(tmp_path)

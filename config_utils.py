import json
import os

def load_config(path):
    """
    Load configuration from a JSON file.
    Returns empty dict if file doesn't exist.
    """
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return json.load(f)

def save_config(path, data):
    """
    Save configuration dict to a JSON file.
    Creates parent directories if needed.
    """
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

def merge_configs(base, override):
    """
    Deep merge two dictionaries.
    Override takes precedence, recursively merges nested dicts.
    """
    merged = base.copy()
    for key, value in override.items():
        if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    return merged

if __name__ == "__main__":
    # Demo
    config1 = {"a": 1, "b": {"x": 10, "z": 30}}
    config2 = {"b": {"y": 20}, "c": 3}
    
    merged = merge_configs(config1, config2)
    print("Merged config:", merged)
    
    # Test save and load
    demo_path = "demo_config.json"
    save_config(demo_path, merged)
    loaded = load_config(demo_path)
    print("Loaded config:", loaded)
    
    # Clean up demo file
    os.remove(demo_path)

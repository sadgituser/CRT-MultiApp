import json
import os
import sys
from pathlib import Path
from datetime import datetime

def get_config_directory():
    """Return application configuration directory based on the operating system."""

    if sys.platform == "win32":
        base_directory = os.environ.get("APPDATA")

        if base_directory:
            return Path(base_directory) / "CRT-MultiApp"

        return Path.home() / "AppData" / "Roaming" / "CRT-MultiApp"

    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "CRT-MultiApp"

    else:
        base_directory = os.environ.get("XDG_CONFIG_HOME")

        if base_directory: 
            return Path(base_directory) / "CRT-MultiApp"

        return Path.home() / ".config" / "CRT-MultiApp"

CONFIG_FILE = get_config_directory() / "config.json" 

DEFAULT_CONFIG = {
    "api_key": "",
    "ai_model": "gpt-4o",
    "ai_provider": "openai",
    "password": "",
    "locked": False,
    "command_history_1": "",
    "command_history_2": "",
    "command_history_3": "",
    "command_history_4": "",
    "command_history_5": "",
    "command_history_6": "",
    "command_history_7": "",
}

def save_config(config, config_file=CONFIG_FILE):
    """Saves the config file to the PATH"""

    config_file = Path(config_file)

    config_file.parent.mkdir(parents=True, exist_ok=True)

    temporary_file = config_file.with_suffix(".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)

        if os.name != "nt":
            temporary_file.chmod(0o600)

        temporary_file.replace(config_file)

        return True

    except (OSError, TypeError, ValueError) as error:
        print(f"File not saved: {error}")

    if temporary_file.exists():
        temporary_file.unlink()

    return False


def load_config(config_file=CONFIG_FILE):
    """Loads configuration with the defaults"""

    config_file = Path(config_file)

    if not config_file.exists():
        config = DEFAULT_CONFIG.copy()
        save_config(config, config_file)
        return config 

    try:
        with config_file.open("r", encoding="utf-8") as file:
            loaded_config = json.load(file)

        if not isinstance(loaded_config, dict):
            raise ValueError("Config must contain a Json Object")

        # add new defaults without removing existing ones
        config = DEFAULT_CONFIG.copy()
        config.update(loaded_config)

        # validate config setttings
        for key, default_value in DEFAULT_CONFIG.items():
            if not isinstance(config.get(key), type(default_value)):
                config[key] = default_value

        if not config["ai_model"].strip():
            config["ai_model"] = DEFAULT_CONFIG["ai_model"]

        if not config["ai_provider"].strip():
            config["ai_provider"] = DEFAULT_CONFIG["ai_provider"] 

        if config != loaded_config:
            save_config(config, config_file) 

        return config
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Config could not be loaded: {error}")

        config = DEFAULT_CONFIG.copy()
        save_config(config, config_file)
        
        return config

def update_config(config, **updates):
    """updates selected values and saves them"""

    for key, value in updates.items():
        if key not in DEFAULT_CONFIG:
            raise ValueError(f"unknown config setting '{key}' ")
        
        expected_type = type(DEFAULT_CONFIG[key])

        if not isinstance(value, expected_type):
            raise TypeError(f"config setting '{key}' must be " 
            f"{expected_type.__name__}"
            )

    updated_config = config.copy()
    updated_config.update(updates)

    if save_config(updated_config):
        config.clear()
        config.update(updated_config)
        return True 

    return False

def save_command_history(config, commands):
    """Saves the last 7 commands to the config file"""

    history = [
        command.strip()
        for command in commands
        if isinstance(command, str) and command.strip()
    ][-7:]

    updates = {
        f"command_history_{index + 1}": (
            history[index] if index < len(history) else ""
        )
        for index in range(7)   

    }

    return update_config(config, **updates)

def load_command_history(config):
    """loads saved commands in order"""

    return [
        config.get(f"command_history_{index + 1}", "")
        for index in range(7)
        if config.get(f"command_history_{index + 1}", "").strip()

    ]
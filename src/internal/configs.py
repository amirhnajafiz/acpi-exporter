import yaml



def load_configs(config_path="config.yaml") -> dict:
    """Load configuration from a YAML file.

    Args:
        config_path (str, optional): path to the config file. Defaults to "config.yaml".

    Raises:
        FileNotFoundError: config_path not found.

    Returns:
        _type_: dict
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

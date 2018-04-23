import configparser

from clerkbot.paths import CONF_DIR


def read():
    """Read the application configuration."""
    config_file = CONF_DIR / 'config.ini'
    config = configparser.ConfigParser()
    with config_file.open() as f:
        config.read_file(f)
    return config

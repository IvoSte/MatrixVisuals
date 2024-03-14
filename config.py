from dynaconf import Dynaconf
import os

config = None


def load_config(config_filepath: str = None):
    if not os.path.exists(config_filepath):
        raise Exception("Config file not found")
    config = Dynaconf(settings_files=[config_filepath])
    return config

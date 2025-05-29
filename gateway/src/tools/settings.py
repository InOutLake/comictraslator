from typing import Self
from configparser import ConfigParser
from os import PathLike


class Settings:
    def __init__(self: Self):
        self.config = None


class ConfigSettings(Settings):
    def __init__(self: Self, config_path: PathLike):
        configparser = ConfigParser()
        self.config = configparser.read(config_path)


class EnvSettings(Settings): ...


def get_settings() -> Settings:
    return ConfigSettings(".cfg")

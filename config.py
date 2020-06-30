import configparser

config_handler = configparser.ConfigParser()
config_handler.read("application.ini")


def get_property(key: str) -> str:
    return config_handler.get("DEFAULT", key, fallback=None)

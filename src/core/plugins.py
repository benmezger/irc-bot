import os
import importlib
from abc import ABC, abstractmethod

PLUGINS = {}


class Plugin(ABC):
    @abstractmethod
    def __call__(self, input: str) -> str:
        pass


class NameConflictError(Exception):
    def __init__(self, message):
        self.message = message


def register_plugin(name: str, description: str, arguments: str):
    def wrapper(plugin_class):
        if name in PLUGINS:
            raise NameConflictError(
                f"Plugin name conflict: '{name}'. Double check"
                " that all plugins have unique names."
            )
        plugin = plugin_class()
        PLUGINS[name] = {
            "name": name,
            "description": description,
            "arguments": arguments,
            "func": plugin,
        }
        return plugin

    return wrapper


def get_plugins():
    return PLUGINS


def import_modules(dirname):
    direc = dirname
    for f in os.listdir(direc):
        path = os.path.join(direc, f)
        if (
            not f.startswith("_")
            and not f.startswith(".")
            and not f == __file__
            and f.endswith(".py")
        ):
            file_name = f[: f.find(".py")]
            module = importlib.import_module(f"{dirname}.{file_name}")

"Some random utils"

from rich import print as rprint

# Settings

_settings = {
    "debug": False,
}


def setting(name, value):
    "Change a setting"
    _settings[name] = value

# Log


def debug(*args, **kwargs):
    "Shortcut for rich.print but depends on 'debug' setting"
    if _settings['debug']:
        rprint(*args, **kwargs)


def log(*args, **kwargs):
    "Shortcut for rich.print"
    rprint(*args, **kwargs)

# Random stuff


def countin(iterable, searchedobj):
    "How many times does an object appear in an iterable?"
    count = 0
    for obj in iterable:
        if obj == searchedobj:
            count += 1
    return count

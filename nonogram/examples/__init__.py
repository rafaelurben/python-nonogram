"Example nonogram games for testing"

from .easy1 import gamedata as easy1
from .easy2 import gamedata as easy2

from .medium1 import gamedata as medium1

from .hard1 import gamedata as hard1

from .expert1 import gamedata as expert1

all_examples = {
    "easy1": ("Easy", 1, easy1),
    "easy2": ("Easy", 2, easy2),

    "medium1": ("Medium", 1, medium1),

    "hard1": ("Hard", 1, hard1),

    "expert1": ("Expert", 1, expert1),
}

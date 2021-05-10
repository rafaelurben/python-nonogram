"A nonogram bot in Python"

from nonogram.game import NonogramGame
from nonogram.utils import setting
from nonogram import examples

data = examples.expert1

game = NonogramGame(**data)
gamecopy = NonogramGame(**data)

setting('debug', True)

game.solve()
gamecopy.print()
game.print()

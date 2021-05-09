"A nonogram bot in Python"

from nonogram.game import NonogramGame
from nonogram import examples

data = examples.hard1

game = NonogramGame(**data)
gamecopy = NonogramGame(**data)

game.solve()
gamecopy.print()
game.print()

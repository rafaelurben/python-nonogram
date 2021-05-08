"A nonogram bot in Python"

from nonogram.game import NonogramGame
from nonogram import examples

game = NonogramGame(**examples.medium1)
gamecopy = NonogramGame(**examples.medium1)

game.solve()
gamecopy.print()
game.print()

"A nonogram bot in Python"

from nonogram.game import NonogramGame
from nonogram import examples

game = NonogramGame(**examples.easy2)
gamecopy = NonogramGame(**examples.easy2)

game.solve()
gamecopy.print()
game.print()

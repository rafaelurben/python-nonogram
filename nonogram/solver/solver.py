"Solver for Nonogram games"

from rich import print
from rich.rule import Rule

from nonogram.solver.lines import NonogramLine

def solve(game):
    "Solve the board"

    oldhash = hash(str(game.rows))

    # Step 1: individual lines
    columns = game.cols
    yinfo = game.yinfo
    for i in range(game.width):
        print(Rule(f"Solve column #{i}"))
        game.replacecol(
            i, NonogramLine.solve(columns[i], yinfo[i]))

    rows = game.rows
    xinfo = game.xinfo
    for i in range(game.height):
        print(Rule(f"Solve row #{i}"))
        game.replacerow(
            i, NonogramLine.solve(rows[i], xinfo[i]))

    newhash = hash(str(game.rows))

    if oldhash != newhash:
        print(Rule(title="Next solving cycle"))
        #solve(game)

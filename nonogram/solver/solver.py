"Solver for Nonogram games"

from nonogram.solver.lines import NonogramLine

def solve(game):
    "Solve the board"

    # Step 1: individual lines
    columns = game.cols
    yinfo = game.yinfo
    for i in range(game.width):
        game.replacecol(
            i, NonogramLine.solve(columns[i], yinfo[i]))
    rows = game.rows
    xinfo = game.xinfo
    for i in range(game.height):
        game.replacerow(
            i, NonogramLine.solve(rows[i], xinfo[i]))

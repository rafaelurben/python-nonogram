"Solver for Nonogram boards"

from rich.rule import Rule

from nonogram.solver.lines import NonogramLineSolver
from nonogram.utils import debug


class NonogramBoardSolver:
    "Class for solving nonogram boards"

    @classmethod
    def issolved(cls, game):
        "Check if a board is solved"

        for i, row in enumerate(game.rows):
            if not NonogramLineSolver.iscompleted(row, game.xinfo[i]):
                return False
        for i, col in enumerate(game.cols):
            if not NonogramLineSolver.iscompleted(col, game.yinfo[i]):
                return False
        return True

    @classmethod
    def solve(cls, game):
        "Solve the board"

        oldhash = hash(str(game.rows))

        # Step 1: individual lines
        columns = game.cols
        yinfo = game.yinfo
        for i in range(game.width):
            debug(Rule(f"Solve column #{i}"))
            game.replacecol(
                i, NonogramLineSolver.solve(columns[i], yinfo[i]))

        rows = game.rows
        xinfo = game.xinfo
        for i in range(game.height):
            debug(Rule(f"Solve row #{i}"))
            game.replacerow(
                i, NonogramLineSolver.solve(rows[i], xinfo[i]))

        if cls.issolved(game):
            debug(game)
            debug(Rule(title="Solving completed"))
            return True

        newhash = hash(str(game.rows))

        if oldhash != newhash:
            debug(game)
            debug(Rule(title="Next solving cycle"))
            return cls.solve(game)

        debug(Rule(title="Solving failed"))
        return False

"A nonogram bot in Python"

from rich import print
from rich.table import Table, Column
from rich.rule import Rule

X = False
O = True
N = None

def _cell(value):
    "Helper function to represent values of a cell"
    if value is True:
        return '⬛'
    if value is False:
        return '❌'
    return None

class NonogramGame():
    "A nonogram game"

    def __init__(self, xinfo, yinfo, board):
        if len(xinfo) != len(board) or len(yinfo) != len(board[0]):
            raise ValueError("Invalid board!")

        self.__xinfo = xinfo
        self.__yinfo = yinfo
        self.__board = board

    # Properties

    @property
    def xinfo(self):
        "Get the requirements for all columns"
        return self.__xinfo

    @property
    def yinfo(self):
        "Get the requirements for all columns"
        return self.__yinfo

    @property
    def width(self):
        "Get the width (column count)"
        return len(self.yinfo)

    @property
    def height(self):
        "Get the height (row count)"
        return len(self.xinfo)

    def __getitem__(self, pos):
        "Get the element at (col, row)"
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise IndexError('Index must be a tuple of length 2')
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.__board[x][y]
        raise IndexError('Grid index out of range')

    def __setitem__(self, pos, value):
        "Set the element at (col, row)"
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise IndexError('Index must be a tuple of length 2')
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError('Grid index out of range')
        self.__board[x][y] = value

    @property
    def cols(self):
        "Get a list of all columns"
        return [
            [self[x, y] for x in range(self.width)]
            for y in range(self.height)
        ]

    @property
    def rows(self):
        "Get a list of all rows"
        return [
            [self[x, y] for y in range(self.height)]
            for x in range(self.width)
        ]

    # Methods

    def export(self):
        "Get the data of this board to copy and create a new one later with `NonogramGame(**data)`"
        return {
            'xinfo': self.__xinfo,
            'yinfo': self.__yinfo,
            'board': self.__board,
        }

    def print(self):
        "Print this gameboard"

        tab = Table(
            Column(justify='right', no_wrap=True),
            title="Nonogram game",
            caption="python-nonogram by rafaelurben",
        )
        for col in range(self.width):
            tab.add_column(
                "\n".join(map(str, self.xinfo[col])),
                justify='center'
            )
        for row in range(self.height):
            tab.add_row(
                " ".join(map(str, self.yinfo[row])),
                *map(_cell, self.rows[row])
            )
        print(Rule(end='\n'), tab, Rule(end='\n'))

    def solve(self):
        pass

game = NonogramGame(
    xinfo=[
        [1],
        [2, 3],
        [4],
    ],
    yinfo=[
        [1],
        [2],
        [2, 3],
    ],
    board=[
        [X, O, X],
        [X, N, X],
        [N, N, X],
    ]
)
game.print()
game[0, 0] = True
game.print()

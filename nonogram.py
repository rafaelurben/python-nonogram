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


class _NonogramLines():
    "Class with helper methods for solving of individual lines"

    @classmethod
    def getfullwidth(cls, requirements):
        "Helper function to get the full required space for a row or column"
        width = -1
        for count in requirements:
            width += count+1
        return width

    @classmethod
    def getsideoffset(cls, values):
        "Get blocked fields on the start and end of a line"
        offsetstart = 0
        for x in values:
            if x is not False:
                break
            offsetstart += 1
        offsetend = 0
        for x in values[::-1]:
            if x is not False:
                break
            offsetend += 1
        return (offsetstart+offsetend, offsetstart, offsetend)

    @classmethod
    def isfull(cls, values):
        "Check if a line is full"
        return None not in values

    @classmethod
    def solve_fullline(cls, values, requirements):
        "Solve a line if it uses up the full (remaining) line"
        offset = cls.getsideoffset(values)
        fullwidth = cls.getfullwidth(requirements)
        print(fullwidth, offset)
        if fullwidth - offset[0] == len(values):
            index = offset[1]
            for i, req in enumerate(requirements):
                for _ in range(req):
                    values[index] = True
                    index += 1
                # add False inbetween
                if i+1 < len(requirements):
                    values[index] = False
                    index += 1
        return values

    @classmethod
    def solve(cls, values, requirements):
        "Try to solve a standalone line"
        print("start solve", values, requirements)
        if not cls.isfull(values):
            values = cls.solve_fullline(values, requirements)
        print("end solve", values, requirements)
        return values


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
            return self.__board[y][x]
        raise IndexError('Grid index out of range')

    def __setitem__(self, pos, value):
        "Set the element at (col, row)"
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise IndexError('Index must be a tuple of length 2')
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError('Grid index out of range')
        self.__board[y][x] = value

    @property
    def rows(self):
        "Get a list of all rows"
        return [
            [self[x, y] for x in range(self.width)]
            for y in range(self.height)
        ]

    @property
    def cols(self):
        "Get a list of all columns"
        return [
            [self[x, y] for y in range(self.height)]
            for x in range(self.width)
        ]

    def replacerow(self, index, values):
        "Replace a row"
        for col, content in enumerate(values):
            self[col, index] = content

    def replacecol(self, index, values):
        "Replace a column"
        for row, content in enumerate(values):
            self[index, row] = content

    # Utils

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
                "\n".join(map(str, self.yinfo[col])),
                justify='center'
            )
        for row in range(self.height):
            tab.add_row(
                " ".join(map(str, self.xinfo[row])),
                *map(_cell, self.rows[row])
            )
        print(Rule(end='\n'), tab, Rule(end='\n'))

    # Solving

    def solve(self):
        "Solve the board"
        
        # Step 1: individual lines
        columns = self.cols
        yinfo = self.yinfo
        for i in range(self.width):
            self.replacecol(
                i, _NonogramLines.solve(columns[i], yinfo[i]))
        rows = self.rows
        xinfo = self.xinfo
        for i in range(self.height):
            self.replacerow(
                i, _NonogramLines.solve(rows[i], xinfo[i]))


game = NonogramGame(
    xinfo=[
        [5],
        [1, 4],
        [2, 1, 1],
        [2, 1, 1],
        [3, 1],
        [3, 3, 1],
        [1, 5, 2],
        [10],
        [1, 1, 4],
        [3, 4],
    ],
    yinfo=[
        [5],
        [1, 1, 1],
        [4, 1],
        [1, 3],
        [7],
        [1, 2, 3],
        [2, 5],
        [4, 3],
        [2, 4],
        [10],
    ],
    board=[
        [N, N, N, N, X, N, N, N, N, N],
        [N, N, X, X, N, N, N, N, N, N],
        [N, X, N, N, N, N, X, N, X, N],
        [N, N, X, X, N, N, N, N, X, N],
        [X, X, N, N, N, N, N, X, X, N],
        [N, N, N, N, N, N, N, N, X, N],
        [N, X, N, N, N, N, N, N, N, N],
        [N, N, N, N, N, N, N, N, N, N],
        [N, N, X, N, X, X, N, N, N, N],
        [N, N, N, X, N, X, N, N, N, N],
    ]
)
game.print()
game.solve()
game.print()

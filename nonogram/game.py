"A Nonogram game"

import copy

from rich import print
from rich.table import Table, Column
from rich.rule import Rule

from nonogram.solver import solve


def _cell(value):
    "Helper function to represent values of a cell"
    if value is True:
        return '⬛'
    if value is False:
        return '❌'
    return None


class NonogramGame():
    "A Nonogram game"

    def __init__(self, xinfo, yinfo, board):
        if len(xinfo) != len(board) or len(yinfo) != len(board[0]):
            raise ValueError("Invalid board!")

        self.__xinfo = copy.deepcopy(xinfo)
        self.__yinfo = copy.deepcopy(yinfo)
        self.__board = copy.deepcopy(board)

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
        "Get a copy of this board's data to create a new one later with `NonogramGame(**data)`"
        return {
            'xinfo': copy.deepcopy(self.__xinfo),
            'yinfo': copy.deepcopy(self.__yinfo),
            'board': copy.deepcopy(self.__board),
        }

    def print(self):
        "Print this gameboard"

        tab = Table(
            Column(justify='right', no_wrap=True),
            title="Nonogram game",
            caption="[link=https://github.com/rafaelurben/python-nonogram]python-nonogram[/link] by "
                    "[link=https://github.com/rafaelurben]rafaelurben[/link]",
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

    solve = solve

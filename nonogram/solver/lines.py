"Utils for solving lines in Nonogram"

from rich import print

class NonogramLine():
    "Class with helper methods for solving individual lines"

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
    def fillline(cls, values):
        "Replace all empty fields with False"
        for i, val in enumerate(values):
            if val is None:
                values[i] = False
        return values

    @classmethod
    def solve_longest(cls, values, requirements):
        "Solving method 2"

    @classmethod
    def solve_fullline(cls, values, requirements):
        "Solving method 1"
        offset = cls.getsideoffset(values)
        fullwidth = cls.getfullwidth(requirements)
        print(fullwidth, offset)
        if fullwidth - offset[0] == len(values):
            index = offset[1]
            for req in requirements:
                for _ in range(req):
                    values[index] = True
                    index += 1
            return cls.fillline(values)
        return values

    @classmethod
    def solve(cls, values, requirements):
        "Try to solve a standalone line"
        print("line solve", values, requirements)
        if not cls.isfull(values):
            values = cls.solve_fullline(values, requirements)
        print(values, "end line solve")
        return values

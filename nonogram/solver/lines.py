"Utils for solving lines in Nonogram"

from rich import print
from rich.rule import Rule

from nonogram.solver.exceptions import UnsolvableLine

class NonogramLine():
    "Class with helper methods for solving individual lines"

    # Get helpers

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
    def getfreeranges(cls, values):
        """Get a list of free ranges in a line
        Return format: [(len, pos, values), ...]"""
        ranges = []
        curr = 0
        currstart = None
        for i, val in enumerate(values+[0]):
            if (val is None) or (val is True):
                curr += 1
                if currstart is None:
                    currstart = i
            elif currstart is not None:
                fullcurr = values[currstart:i]
                ranges.append(
                    (curr, (currstart, i-1), fullcurr)
                )
                curr = 0
                currstart = None
        return ranges

    # Check helpers

    @classmethod
    def isfull(cls, values):
        "Check if a line is full"
        return None not in values

    @classmethod
    def iscompleted(cls, values, requirements):
        "Check if a line meets its requirements"
        meets = []
        curr = 0
        for val in values+[0]:
            if val is True:
                curr += 1
            elif curr > 0:
                meets.append(curr)
                curr = 0
        return meets == requirements

    # Modify helpers

    @classmethod
    def fillline(cls, values):
        "Replace all empty fields with False"
        for i, val in enumerate(values):
            if val is None:
                values[i] = False
        return values

    # Solving methods

    @classmethod
    def solve_fullline(cls, values, requirements):
        "Solving method"
        offset = cls.getsideoffset(values)
        fullwidth = cls.getfullwidth(requirements)
        print("- solve fullline", {"fullwidth": fullwidth, "offset": offset})
        if len(values) - offset[0] == fullwidth:
            index = offset[1]
            for req in requirements:
                values[index:index+req] = [True]*req
                index += req+1
            values = cls.fillline(values)
            print(values, "- end solve fullline")
            return values
        print("- unable to solve fullline")
        return values

    @classmethod
    def solve_ranges(cls, values, requirements):
        "Solving method"
        ranges = cls.getfreeranges(values)
        print("- solve ranges", {"ranges": ranges})

        # Remove all ranges which are too small
        smallestreq = min(requirements)
        for ran in ranges:
            if ran[0] < smallestreq:
                values[ran[1][0]:ran[1][1]+1] = [False]*ran[0]

        # Modify ranges at the end and start
        for ran in ranges:
            if ran[0] < requirements[0]:
                values[ran[1][0]:ran[1][1]+1] = [False]*ran[0]
                continue
            if ran[2][0] is True:
                values[ran[1][0]:ran[1][0]+requirements[0]] = [True]*requirements[0]
                if ran[1][0]+requirements[0] < len(values):
                    values[ran[1][0]+requirements[0]] = False
            break
        for ran in ranges[::-1]:
            if ran[0] < requirements[-1]:
                values[ran[1][0]:ran[1][1]+1] = [False]*ran[0]
                continue
            if ran[2][-1] is True:
                values[ran[1][1]-requirements[-1]+1:ran[1][1]+1] = [True]*requirements[-1]
                if ran[1][1]-requirements[-1] >= 0:
                    values[ran[1][1]-requirements[-1]] = False
            break

        # Check if requirements are met
        isfull = cls.isfull(values)
        iscompleted = cls.iscompleted(values, requirements)

        if iscompleted and not isfull:
            values = cls.fillline(values)
        elif isfull and not iscompleted:
            raise UnsolvableLine("This line seems impossible to solve!")

        print(values, "- end solve ranges")
        return values

    # Main solving

    @classmethod
    def solve(cls, values, requirements):
        "Try to solve a standalone line"

        oldhash = hash(str(values))

        # TODO: Trim offset at start / Also trim fullfilled requirements

        print({"values": values, "requirements": requirements})

        if not cls.isfull(values):
            values = cls.solve_fullline(values, requirements)
        if not cls.isfull(values):
            values = cls.solve_ranges(values, requirements)

        newhash = hash(str(values))

        if not cls.isfull(values) and oldhash != newhash:
            print("solve line again")
            values = cls.solve(values, requirements)

        return values

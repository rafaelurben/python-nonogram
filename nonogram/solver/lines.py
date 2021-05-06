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
    def getfreeranges(cls, values):
        """Get a list of free ranges in a line
        Return format: [(len, pos, values, contains True?), ...]"""
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
                    (curr, (currstart, i-1), fullcurr, True in fullcurr)
                )
                curr = 0
                currstart = None
        return ranges

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
    def solve_fullline(cls, values, requirements):
        "Solving method 1"
        offset = cls.getsideoffset(values)
        fullwidth = cls.getfullwidth(requirements)
        if fullwidth - offset[0] == len(values):
            print("- solve fullline", fullwidth, "offset", offset)
            index = offset[1]
            for req in requirements:
                values[index:index+req] = [True]*req
                index += req+1
            print(values, "- end solve fulline")
            return cls.fillline(values)
        return values

    @classmethod
    def solve_ranges(cls, values, requirements):
        "Solving method 2"
        print("- solve ranges")
        ranges = cls.getfreeranges(values)

        if len(ranges) == len(requirements):
            for i, ran in enumerate(ranges):
                rlen = requirements[i]
                if ran[0] == rlen:
                    values[ran[1][0]:ran[1][1]+1] = [True]*rlen
        elif len(ranges) < len(requirements):
            ...
        elif len(ranges) > len(requirements):
            ...
        print(values, "- end solve ranges")
        return values

    @classmethod
    def solve(cls, values, requirements):
        "Try to solve a standalone line"
        print("line solve", values, requirements)
        if not cls.isfull(values):
            values = cls.solve_fullline(values, requirements)
        if not cls.isfull(values):
            values = cls.solve_ranges(values, requirements)
        print(values, "end line solve")
        return values

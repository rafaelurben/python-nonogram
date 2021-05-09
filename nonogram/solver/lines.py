"Utils for solving lines in Nonogram"

from rich import print as log

from nonogram.solver.exceptions import UnsolvableLine
from nonogram.utils import countin


class NonogramLine():
    "Class with helper methods for solving individual lines"

    # Get helpers

    @classmethod
    def getfullwidth(cls, requirements):
        "Helper function: Get the full required space for requirements"
        return sum(requirements)+len(requirements)-1

    @classmethod
    def getoffset(cls, values):
        """Get blocked fields on the start and end of a line
        Output format: (fullofset, leftoffset, rightoffset)"""
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
        Output format: [(len, pos, values), ...]"""
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
        completed = meets == requirements

        # Check for potential errors
        if not completed and cls.isfull(values):
            raise UnsolvableLine("Requirements are not met but line is full!")

        return completed

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
        "Solving method: Requirements use full space"
        reqwidth = cls.getfullwidth(requirements)
        valwidth = len(values)
        log("[yellow][Solving fullline] Start[/]")
        log({"reqwidth": reqwidth, "valwidth": valwidth})
        if valwidth == reqwidth:
            index = 0
            for req in requirements:
                values[index:index+req] = [True]*req
                index += req+1
            log("[yellow][Solving fullline] Succeeded[/]")
            return values
        log("[yellow][Solving fullline] Failed[/]")
        return values

    @classmethod
    def solve_ranges(cls, values, requirements):
        "Solving method: Use free ranges"
        ranges = cls.getfreeranges(values)
        log("[yellow][Solving ranges] Start[/]")
        log({"ranges": ranges})

        # Remove all ranges which are too small
        smallestreq = min(requirements)
        for ran in ranges:
            if ran[0] < smallestreq:
                values[ran[1][0]:ran[1][1]+1] = [False]*ran[0]

        # Update ranges var
        ranges = cls.getfreeranges(values)

        # Modify ranges at the end and start

        for ran in ranges:
            if ran[0] < requirements[0]:
                values[ran[1][0]:ran[1][1]+1] = [False]*ran[0]
                continue
            if ran[2][0] is True or (ran[0] == requirements[0] and True in ran[2]):
                values[ran[1][0]:ran[1][0]+requirements[0]
                       ] = [True]*requirements[0]
                if ran[1][0]+requirements[0] < len(values):
                    values[ran[1][0]+requirements[0]] = False
            break
        for ran in ranges[::-1]:
            if ran[0] < requirements[-1]:
                values[ran[1][0]:ran[1][1]+1] = [False]*ran[0]
                continue
            if ran[2][-1] is True or (ran[0] == requirements[-1] and True in ran[2]):
                values[ran[1][1]-requirements[-1]+1:ran[1]
                       [1]+1] = [True]*requirements[-1]
                if ran[1][1]-requirements[-1] >= 0:
                    values[ran[1][1]-requirements[-1]] = False
            break

        # Update ranges var
        ranges = cls.getfreeranges(values)

        # Case "Exact match"
        if list(map(lambda x: x[0], ranges)) == requirements:
            for ran in ranges:
                values[ran[1][0]:ran[1][1]+1] = [True]*ran[0]
            log("[yellow][Solving ranges] Succeeded with exact match[/]")
            return values


        log("[yellow][Solving ranges] Ended[/]")
        return values

    # Main solving

    @classmethod
    def solve(cls, values, requirements):
        "Try to solve a line"

        oldhash = hash(str(values))
        log({"values": values, "requirements": requirements})

        # START) Skip if line is already full
        if cls.iscompleted(values, requirements):
            values = cls.fillline(values)
            return values

        # 1a) Trim from ends
        offset = cls.getoffset(values)

        trim_start = 0
        i_first = offset[1]
        if values[i_first] is True:
            i_end = i_first+requirements[0]
            values[i_first:i_end] = [True]*requirements[0]
            if not i_end < len(values):
                cls.fillline(values)
                log("[cyan][Return] Solved in 1a) start:[/]", values)
                return values
            values[i_end] = False
            trim_start = i_end+1

        trim_end = 0
        i_last = -1-offset[2]
        if values[i_last] is True:
            i_start = i_last-requirements[-1]
            values[i_start:i_last] = [True]*requirements[-1]
            if not (len(values) + i_start) >= 0:
                values = cls.fillline(values)
                log("[cyan][Return] Solved in 1a) end:[/]", values)
                return values
            values[i_start] = False
            trim_end = i_start

        # 1b) End if requirements are met

        if cls.iscompleted(values, requirements):
            values = cls.fillline(values)
            log("[cyan][Return] Solved in 1a):[/]", values)
            return values

        # 1c) Run for sublist if ends can be trimmed
        if trim_start or trim_end or offset[0]:
            log("[blue][Recursive] Trimming line[/]",
                {"t_start": trim_start, "t_end": trim_end, "offset": offset})
            if trim_start and trim_end:
                values[trim_start:trim_end] = cls.solve(
                    values[trim_start:trim_end], requirements[1:-1])
            elif trim_start:
                values[trim_start:-offset[2] or None] = cls.solve(
                    values[trim_start:-offset[2] or None], requirements[1:]
                )
            elif trim_end:
                values[offset[1]:trim_end] = cls.solve(
                    values[offset[1]:trim_end], requirements[:-1]
                )
            else:
                values[offset[1]:-offset[2] or None] = cls.solve(
                    values[offset[1]:-offset[2] or None], requirements
                )
            log(values)
            return values

        # 2a) Solve fullline

        values = cls.solve_fullline(values, requirements)

        # 2b) End if requirements are met

        if cls.iscompleted(values, requirements):
            values = cls.fillline(values)
            log("[cyan][Return] Solved in 2) Fullline:[/]", values)
            return values

        # 3a) Solve ranges

        values = cls.solve_ranges(values, requirements)

        # 3b) End if requirements are met

        if cls.iscompleted(values, requirements):
            values = cls.fillline(values)
            log("[cyan][Return] Solved in 3) Ranges:[/]", values)
            return values

        # END) Solve again if something has changed
        newhash = hash(str(values))
        if oldhash != newhash:
            log("[blue][Recursive] Line changed - solve again[/]")
            return cls.solve(values, requirements)
        log("[cyan][Return] Line still unsolved:[/]", values)
        return values

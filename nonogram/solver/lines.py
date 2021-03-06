"Utils for solving lines in Nonogram"

from nonogram.solver.exceptions import UnsolvableLine
from nonogram.utils import countin, debug


class NonogramLineSolver():
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
            raise UnsolvableLine("Requirements are not met but line is full! "
                                 f"{values} {requirements}")

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
        debug("[yellow][Solving fullline] Start[/]")
        debug({"reqwidth": reqwidth, "valwidth": valwidth})
        if reqwidth > valwidth:
            raise UnsolvableLine("Requirements use more space than possible!")
        if valwidth == reqwidth:
            index = 0
            for req in requirements:
                values[index:index+req] = [True]*req
                index += req+1
            debug("[yellow][Solving fullline] Succeeded[/]")
            return values
        debug("[yellow][Solving fullline] Failed[/]")
        return values

    @classmethod
    def solve_singlerangesinglereq(cls, values, req):
        "Solving method: 1 Requirement in 1 range"

        length = len(values)
        half = length/2

        i_start = None
        i_end = None

        # Set start and end index to distance starting from the middle
        if req > half:
            diff = req - half
            i_start = int(half-diff)
            i_end = int(half+diff)

        # Change start/end if already present and not between
        for i, value in enumerate(values):
            if value is True:
                if i_start is None or i < i_start:
                    i_start = i
                if i_end is None or i > i_end:
                    i_end = i+1

        # Move start/end left/right and replace values
        if i_start is not None and i_end is not None:
            missing = req-(i_end-i_start)

            if i_start < missing:
                i_end += (missing-i_start)
            if length-i_end < missing:
                i_start -= (missing-(length-i_end))

            values[i_start:i_end] = [True]*(i_end-i_start)
        return values

    @classmethod
    def solve_singlerangemultireq(cls, values, requirements):
        "Solving method: More than 1 requirement in 1 range"
        debug("[red][Solving singlerange] Start[/]")
        debug({"values": values, "requirements": requirements})

        debug("[red][Solving singlerange] End[/]")
        return values

    @classmethod
    def solve_multirange(cls, values, requirements):
        "Solving method: Multirange"
        ranges = cls.getfreeranges(values)
        debug("[red][Solving multirange] Start[/]")
        debug({"values": values, "ranges": ranges, "requirements": requirements})

        debug("[red][Solving multirange] End[/]")
        return values

    @classmethod
    def solve_ranges(cls, values, requirements):
        "Solving method: Use free ranges"
        ranges = cls.getfreeranges(values)
        debug("[yellow][Solving ranges] Start[/]")
        debug({"ranges": ranges})

        # Remove all ranges which aren't usable
        smallestreq = min(requirements)

        fillempty = len(ranges) > 1 and countin(
            map(lambda x: True in x[2], ranges), True) == len(requirements)

        for ran in ranges:
            if ran[0] < smallestreq or (fillempty and not True in ran[2]):
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
            debug("[yellow][Solving ranges] Succeeded with exact match[/]")
            return values

        elif countin(map(lambda x: True in x[2], ranges), True) == len(requirements):
            for i, ran in enumerate(ranges):
                req = requirements[i]
                values[ran[1][0]:ran[1][1]+1] = cls.solve_singlerangesinglereq(ran[2], req)
            return values

        # Case "Only one requirement in one range"
        if len(requirements) == 1 and len(ranges) == 1:
            req = requirements[0]
            ran = ranges[0]

            values[ran[1][0]:ran[1][1] +
                   1] = cls.solve_singlerangesinglereq(ran[2], req)

        # Case "More than one requirement in one range"
        elif len(ranges) == 1:
            ran = ranges[0]
            values[ran[1][0]:ran[1][1] +
                   1] = cls.solve_singlerangemultireq(ran[2], requirements)

        # Case "More than one requirement in more than one range"
        elif len(ranges) > 1 and len(requirements) > 1:
            s = slice(ranges[0][1][0], ranges[-1][1][1]+1)
            values[s] = cls.solve_multirange(values[s], requirements)

        debug("[yellow][Solving ranges] Ended[/]")
        return values

    # Main solving

    @classmethod
    def solve(cls, values, requirements):
        "Try to solve a line"

        oldhash = hash(str(values))
        debug({"values": values, "requirements": requirements})

        # START) Skip if line is already full
        if cls.iscompleted(values, requirements):
            if not cls.isfull(values):
                values = cls.fillline(values)
                debug(values)
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
                debug("[cyan][Return] Solved in 1a) start:[/]", values)
                return values
            values[i_end] = False
            trim_start = i_end+1

        offset = cls.getoffset(values)

        trim_end = 0
        i_last = -1-offset[2]
        if values[i_last] is True:
            i_start = i_last-requirements[-1]+1
            values[i_start:i_last+1 or None] = [True]*requirements[-1]
            if not (len(values) + i_start) > 0:
                values = cls.fillline(values)
                debug("[cyan][Return] Solved in 1a) end:[/]", values)
                return values
            values[i_start-1] = False
            trim_end = i_start-1

        # 1b) End if requirements are met

        if cls.iscompleted(values, requirements):
            values = cls.fillline(values)
            debug("[cyan][Return] Solved in 1a):[/]", values)
            return values

        # 1c) Run for sublist if ends can be trimmed
        if trim_start or trim_end or offset[0]:
            debug("[blue][Recursive] Trimming line[/]",
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
            debug(values)
            return values

        # 2a) Solve fullline

        values = cls.solve_fullline(values, requirements)

        # 2b) End if requirements are met

        if cls.iscompleted(values, requirements):
            values = cls.fillline(values)
            debug("[cyan][Return] Solved in 2) Fullline:[/]", values)
            return values

        # 3a) Solve ranges

        values = cls.solve_ranges(values, requirements)

        # 3b) End if requirements are met

        if cls.iscompleted(values, requirements):
            values = cls.fillline(values)
            debug("[cyan][Return] Solved in 3) Ranges:[/]", values)
            return values

        # END) Solve again if something has changed
        newhash = hash(str(values))
        if oldhash != newhash:
            debug("[blue][Recursive] Line changed - solve again[/]")
            return cls.solve(values, requirements)
        debug("[cyan][Return] Line still unsolved:[/]", values)
        return values

from typing import List, Tuple
from levels import *


def delta(x: int, y: int, dir: str) -> List[int]:
    """
    Returns the position adjacent to position [x, y], in the direction dir.
    :param x: x coordinate
    :param y: y coordinate
    :param dir: the direction
    :return: The list [x1, y1] with the coordinates adjacent to [x, y], in the given direction.
    """
    deltas = { EAST: (+1, 0), WEST: (-1, 0), NORTH: (0, +1), SOUTH: (0, -1) }
    return [x + deltas[dir][0], y + deltas[dir][1]]


def iswin(state: List[List[str or int]]) -> bool:
    """
    Checks whether a state is a final state (all squares over their corresponding goals).
    :param state: the state to check.
    :return: True if the state is final.
    """
    fixed = [e for e in state if e[TYPE] != SQUARE]
    sqrs = {e[COLOR]: e[XY] + [e[DIR]] for e in state if e[TYPE] == SQUARE}

    for sq in sqrs:
        goal = [e[XY] for e in fixed if e[TYPE] == GOAL and e[COLOR] == sq]
        if goal and sqrs[sq][XY] != goal[0]:
            return False
    return True

def p(state, small: bool = False) -> str:
    """
    Renders the state as a printable string.
    :param state: A state in GAS game
    :param small: If True, a more compact version is rendered.
    :return: A printable string that represents the state.
    """
    space, multx, multy = 7, 5, 3
    spacer = ' ' * multx
    sep = '-' * 2 * space * multx

    v = check_state(state)
    if v: return v + "\n" + sep

    minx = min([s[X] for s in state])
    maxx = max([s[X] for s in state])
    miny = min([s[Y] for s in state])
    maxy = max([s[Y] for s in state])

    s = ""

    elements = {}
    for iy in range(miny, maxy + 1):
        elements[iy] = {}
        for ix in range(minx, maxx + 1):
            elements[iy][ix] = [e for e in state if e[X] == ix and e[Y] == iy]

    if small:
        for iy in range(maxy, miny - 1, -1):
            for ix in range(minx, maxx + 1):
                es = elements[iy][ix]
                squares = [e for e in es if e[TYPE] == SQUARE]
                if not es:
                    s += " ."
                elif squares:
                    s += squares[0][DIR] + squares[0][COLOR][0]
                else:
                    s += " *" if es[0][TYPE] == GOAL else es[0][DIR] * 2
                s += " "
            s += "\n"
        return s

    s += "  "
    for ix in range(-space, space):
        s += ' ' * (multx - 4) + str(ix).zfill(2) + "  "
    s += "\n"

    for iy in range(space, -space, -1):
        for line in range(multy):
            s += str(iy).zfill(2) if line == 1 else "  "
            for ix in range(-space, space):
                es = elements[iy][ix] if minx <= ix <= maxx and miny <= iy <= maxy else []
                squares = [e for e in es if e[TYPE] == SQUARE]
                square = squares[0] if squares else None
                notsquares = [e for e in es if e[TYPE] != SQUARE]
                e = notsquares[0] if notsquares else None

                if (square):
                    s += {
                        0: " ___ ",
                        1: "|" + square[COLOR][0] + (e[DIR] if e and e[TYPE] == CHANGER else " ") + square[DIR] + "|",
                        2: "|_" + ("*" + e[COLOR][0] + ")" if e and e[TYPE] == GOAL else "__|"),
                    }.get(line)
                elif e and e[TYPE] == CHANGER and line == 1:
                    s += " [" + e[DIR] + "] "
                elif e and e[TYPE] == GOAL and line == 2:
                    s += " (*" + e[COLOR][0] + ")"
                else:
                    s += "  .  " if line == 1 and not es else spacer
            s += "\n"
    s += sep
    return s

def prints(*strings : [str]) -> str:
    """
    Print multiple multi-line strings on next to the other.
    :param strings: several single- or multi-line strings
    :return; a multi-line concatenation of the strings, top-aligned.
    """
    out = ""
    rows = []
    maxheight = 0
    cwidth = 0
    for i, s in enumerate(strings):
        lines = s.split("\n")
#         height[i] = len(lines)
        if maxheight < len(lines):
            rows += (len(lines) - maxheight) * [cwidth * " "]
            maxheight = len(lines)
        width = max([len(line) for line in lines])
        cwidth += width
#         print(len(rows), len(lines))
        for j, line in enumerate(lines):
            rows[j] += line.rjust(width)
        for j in range(len(lines), maxheight): rows[j] += width * " "
    out = "\n".join(rows)
    print(out)


def check_state(state) -> str or None:
    """
    Verify the validity of a state in GAS game
    :param state: a state in GAS game
    :return: None if the state is valid, an error string if the state is invalid
    """
    if not isinstance(state, list): return "Invalid state (not list): " + str(state)
    for e in state:
        if not isinstance(e, list): return "Invalid element (not list): " + str(e)
        if len(e) == 0: return "Invalid element (empty list)"
        if e[TYPE] not in types: return "Invalid element type: " + str(e)
        if len(e) != (4 if e[TYPE] == GOAL else 5): return "Invalid element list length: " + str(e)
        if e[TYPE] != CHANGER and e[COLOR] not in colors: return "Invalid element color: " + str(e)
        if not (isinstance(e[X], int) and isinstance(e[Y], int)): return "Invalid element coords: " + str(e)
        if e[TYPE] != GOAL and e[DIR] not in dirs: return "Invalid element direction: " + str(e)
    return None


def state_eq(state1, state2) -> bool:
    """
    Verify the equality of two states
    :param state1: A state in GAS game
    :param state2: A state in GAS game
    :return: True if the states are equal, False otherwise
    """
    res1 = check_state(state1)
    res2 = check_state(state2)
    if res1 is not None:
        raise ValueError(res1)
    elif res2 is not None:
        raise ValueError(res2)
    else:
        if len(state1) != len(state2):
            return False

        changers1 = {(e[X], e[Y]): e[DIR] for e in state1 if e[TYPE] == CHANGER}
        goals1 = [(e[X], e[Y]) for e in state1 if e[TYPE] == GOAL]

        changers2 = {(e[X], e[Y]): e[DIR] for e in state2 if e[TYPE] == CHANGER}
        goals2 = [(e[X], e[Y]) for e in state2 if e[TYPE] == GOAL]

        state1_squares = [e for e in state1 if e[TYPE] == SQUARE]
        state2_squares = [e for e in state2 if e[TYPE] == SQUARE]

        # check static state elements
        if len(goals1) != len(goals2):
            return False
        if len(changers1) != len(changers2):
            return False
        for goal in goals1:
            if goal not in goals2:
                return False

        for changer in changers1:
            if changer not in changers2 or changers1[changer] != changers2[changer]:
                return False

        # check dynamic state elements (the squares)
        for s1 in state1_squares:
            if s1 not in state2_squares:
                return False

        return True


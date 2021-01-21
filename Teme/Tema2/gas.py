from copy import deepcopy
from heapq import heappop, heappush
from math import inf, sqrt
from typing import Callable, List, Tuple

from levels import *
from util import check_state, delta, state_eq, p, prints, iswin

"""
#######################################
################ TODOs ################
#######################################
"""


MINX = 0
MINY = 1
MAXX = 2
MAXY = 3


def _get_square(state: List[List[str or int]], colour: str) -> List[str or int]:
    for elem in state:
        if elem[TYPE] == SQUARE and elem[COLOR] == colour:
            return elem


def _get_type(state: List[List[str or int]], pos: Tuple[int, int], type: str):
    for elem in state:
        if elem[TYPE] == type and elem[X] == pos[X] and elem[Y] == pos[Y]:
            return elem


def between_dir(
    direction: str,
    x1: int, y1: int,
    x2: int, y2: int,
    x3: int, y3: int
):
    return (
        (y2 == y3 and y1 == y2
        and (
            (direction == EAST and x1 < x2 and x2 < x3)
            or (direction == WEST and x1 > x2 and x2 > x3)
        ))
        or (
            (x2 == x3 and x1 == x2
            and (
                (direction == NORTH and y1 < y2 and y2 < y3)
                or (direction == SOUTH and y1 > y2 and y2 > y3)
            ))
        )
    )


def _check_continuous_squares(
    start_sq: List[str or int],
    sq: List[str or int],
    squares: List[List[str or int]],
    direction: str
) -> bool:
    rev = False

    if direction == EAST or direction == WEST:
        sq_line = list(filter(lambda s: s[Y] == sq[Y], squares))
        pos = X

        if direction == EAST:
            sq_line.sort(key=lambda s: s[X])
        else:
            rev = True
            sq_line.sort(key=lambda s: s[X], reverse=True)

    else:
        sq_line = list(filter(lambda s: s[X] == sq[X], squares))
        pos = Y

        if direction == NORTH:
            sq_line.sort(key=lambda s: s[Y])
        else:
            rev = True
            sq_line.sort(key=lambda s: s[Y], reverse=True)

    if start_sq not in sq_line:
        return False

    start = sq_line.index(start_sq)
    end = sq_line.index(sq)
    if start > end:
        return False

    for i in range(start, end):
        if rev and sq_line[i][pos] != sq_line[i + 1][pos] + 1:
            return False
        if not rev and sq_line[i][pos] != sq_line[i + 1][pos] - 1:
            return False

    return True


def move_square(state: List[List[str or int]], square: List[str or int]):
    all_squares = _get_squares(state)
    for sq in all_squares:
        if (sq[COLOR] == square[COLOR]
            or not _check_continuous_squares(
                square,
                sq,
                all_squares,
                square[DIR]
            )
        ):
            continue

        state.remove(sq)

        new_x, new_y = delta(sq[X], sq[Y], square[DIR])
        changer = _get_type(state, (new_x, new_y), CHANGER)
        if changer:
            sq[DIR] = changer[DIR]

        state.append([new_x, new_y, sq[TYPE], sq[COLOR], sq[DIR]])

    state.remove(square)

    new_x, new_y = delta(square[X], square[Y], square[DIR])
    changer = _get_type(state, (new_x, new_y), CHANGER)
    if changer:
        square[DIR] = changer[DIR]

    state.append([new_x, new_y, square[TYPE], square[COLOR], square[DIR]])

    return state


def move_square_rec(
    state: List[List[str or int]],
    x: int,
    y: int,
    direction: str
) -> List[List[str or int]]:
    """
    Implementare recursiva a lui move_square. E pusa aici doar ca sa se vada cat
    de frumos se poate face urmand o logica naturala in comparatie cu
    implementarea fortata de mai sus.
    """
    square = _get_type(state, (x, y), SQUARE)
    if square is None:
        return state

    state.remove(square)
    new_x, new_y = delta(square[X], square[Y], direction)
    state = move_square_rec(state, new_x, new_y, direction)

    changer = _get_type(state, (new_x, new_y), CHANGER)
    if changer:
        square[DIR] = changer[DIR]

    state.append([new_x, new_y, square[TYPE], square[COLOR], square[DIR]])

    return state


def press(color: str, state: List[List[str or int]]) -> List[List[str or int]]:
    square = _get_square(state, color)
    # return move_square_rec(deepcopy(state), square[X], square[Y], square[DIR])
    return move_square(deepcopy(state), deepcopy(square))


def _get_squares(state: List[List[str or int]]) -> List[List[str or int]]:
    return [elem for elem in state if elem[TYPE] == SQUARE]


def _get_goal_for_colour(state: List[List[str or int]], colour: str):
    for elem in state:
        if elem[TYPE] == GOAL and elem[COLOR] == colour:
            return elem[X], elem[Y]

    return None, None


def _check_halfplane(
    state: List[List[str or int]],
    square: List[str or int],
    p: Callable[[List[str or int]], int]
) -> bool:
    return any(elem for elem in state
        if (
            p(elem) and
            (
                (elem[TYPE] == SQUARE and elem[COLOR] != square[COLOR])
                or (elem[TYPE] == CHANGER and elem[DIR] != square[DIR])
            )
        )
    )


def _is_halfplane_consistent(state: List[List[str or int]]) -> bool:
    for sq in _get_squares(state):
        x, y = _get_goal_for_colour(state, sq[COLOR])
        if x is not None and y is not None:
            if sq[DIR] == SOUTH and y > sq[Y]:
                if not _check_halfplane(state, sq, lambda el: el[Y] <= sq[Y]):
                    return False
            if sq[DIR] == NORTH and y < sq[Y]:
                if not _check_halfplane(state, sq, lambda el: el[Y] >= sq[Y]):
                    return False
            if sq[DIR] == EAST and x < sq[X]:
                if not _check_halfplane(state, sq, lambda el: el[X] >= sq[X]):
                    return False
            if sq[DIR] == WEST and x > sq[X]:
                if not _check_halfplane(state, sq, lambda el: el[X] <= sq[X]):
                    return False

    return True


def _squares_within_bbox(
    state: List[List[str or int]],
    bbox: List[int]
) -> bool:
    for square in _get_squares(state):
        if (
            square[X] < bbox[MINX] or square[Y] < bbox[MINY]
            or square[X] > bbox[MAXX] or square[Y] > bbox[MAXY]
        ):
            return False

    return True


def _get_bbox(state: List[List[str or int]]) -> List[int]:
    bbox = [inf, inf, -inf, -inf]

    for elem in state:
        bbox[MINX] = min(bbox[MINX], elem[X])
        bbox[MINY] = min(bbox[MINY], elem[Y])
        bbox[MAXX] = max(bbox[MAXX], elem[X])
        bbox[MAXY] = max(bbox[MAXY], elem[Y])

    bbox[MINY] -= 1
    bbox[MAXY] += 1

    return bbox


def hash(state: List[List[str or int]]) -> str:
    squares = [(elem[X], elem[Y], elem[COLOR], elem[DIR])
        for elem in state if elem[TYPE] == SQUARE]
    squares.sort(key=lambda el: el[2])

    return str(squares)


def euclid(state: List[List[str or int]]) -> int:
    dist_euclid = 0

    for square in _get_squares(state):
        x, y = _get_goal_for_colour(state, square[COLOR])
        if x is not None and y is not None:
            dist_euclid += sqrt((square[X] - x)**2 + (square[Y] - y)**2)

    return int(dist_euclid)


def solve(
    initial_state: List[List[str or int]]
) -> Tuple[List[str], List[List[List[str or int]]], int]:
    frontier = [(euclid(initial_state), initial_state)]
    discovered = {hash(initial_state): []}
    colours = [elem[COLOR] for elem in initial_state if elem[TYPE] == SQUARE]

    num_explored = 1
    bbox = _get_bbox(initial_state)

    while frontier:
        crt_state = heappop(frontier)[1]
        cmds = discovered[hash(crt_state)]

        if iswin(crt_state):
            break

        for colour in colours:
            next_s = press(colour, crt_state)
            if (
                not _is_halfplane_consistent(next_s)
                or not _squares_within_bbox(next_s, bbox)
            ):
                continue

            next_s_h = hash(next_s)
            if next_s_h not in discovered:
                discovered[next_s_h] = cmds + [colour]
                heappush(frontier, (euclid(next_s), next_s))
                num_explored += 1

    explored = [initial_state]
    for cmd in cmds:
        initial_state = press(cmd, initial_state)
        explored.append(initial_state)

    return cmds, explored, num_explored

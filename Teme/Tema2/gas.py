from copy import deepcopy
from typing import List, Tuple

from levels import *
from util import check_state, state_eq, p, prints

"""
#######################################
################ TODOs ################
#######################################
"""


def pos(square: List[str or int], x: int, y: int) -> bool:
    return square[X] == x and square[Y] == y and square[TYPE] == SQUARE


def dir(square: List[str or int], direction: str) -> bool:
    return square[TYPE] == SQUARE and square[DIR] == direction


def delta(direction: str, x: int, y: int, x1: int, y1: int) -> bool:
    return (
        x == x1 and y == y1 - 1 and direction == EAST
        or x == x1 + 1 and y == y1 and direction == NORTH
        or x == x1 and y == y1 + 1 and direction == WEST
        or x == x1 -1 and y == y1 and direction == SOUTH
    )


def empty(state: List[List[str or int]], x: int, y: int) -> bool:
    return not any(map(lambda l: pos(l, x, y), state))


def changer(
    state: List[List[str or int]],
    x: int,
    y: int,
    direction: str
) -> bool:
    return any(map(
        lambda l:
            l[X] == x
            and l[Y] == y
            and l[TYPE] == CHANGER
            and l[DIR] == direction,
        state
    ))


def no_changer(state: List[List[str or int]], x: int, y: int) -> bool:
    return not any(map(
        lambda l: l[X] == x and l[Y] == y and l[TYPE] == CHANGER,
        state
    ))


def between(down: int, x: int, up: int) -> bool:
    return down <= x and x <= up


def _get_colour_pos(state: List[List[str or int]], colour: str) -> Tuple[int, int]:
    for elem in state:
        if elem[TYPE] == SQUARE and elem[COLOR] == colour:
            return elem[X], elem[Y]


def _get_elems_by_pos(
    state: List[List[str or int]],
    pos: Tuple[int, int]
) -> List[List[str or int]]:
    return [elem for elem in state if elem[X] == pos[X] and elem[Y] == pos[Y]]


def _get_type(state: List[List[str or int]], pos: Tuple[int, int], type: str):
    for elem in state:
        if elem[TYPE] == type and elem[X] == pos[X] and elem[Y] == pos[Y]:
            return elem


def _move_square(
    state: List[List[str or int]],
    pos: Tuple[int, int],
    direction: str
) -> List[List[str or int]]:
    square = _get_type(state, pos, SQUARE)
    if square is None:
        return state

    if direction is None:
        direction = square[DIR]

    if direction == EAST:
        new_x, new_y = square[X] + 1, square[Y]
    elif direction == NORTH:
        new_x, new_y = square[X], square[Y] + 1
    elif direction == WEST:
        new_x, new_y = square[X] - 1, square[Y]
    else:
        new_x, new_y = square[X], square[Y] - 1

    state.remove(square)
    state = _move_square(state, (new_x, new_y), direction)

    square[X] = new_x
    square[Y] = new_y

    changer = _get_type(state, (new_x, new_y), CHANGER)
    if changer:
        square[DIR] = changer[DIR]

    state.append(square)

    return state


def press(color: str, state: List[List[str or int]]) -> List[List[str or int]]:
    return _move_square(deepcopy(state), _get_colour_pos(state, color), None)


def solve(initial_state: List[List[str or int]]) -> Tuple[List[str], List[List[List[str or int]]], int]:
    return ["", [initial_state], 0]


def play(initstate: List[List[str or int]], plan: List[str], small: bool=False):
    state = initstate
    print(p(state, small))
    for action in plan:
        state = press(action, state)
        print(p(state, small))


# play(levels['level10'], [RED, RED, RED, DARK, DARK, BLUE, BLUE, BLUE])

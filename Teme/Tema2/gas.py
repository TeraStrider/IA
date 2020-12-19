from copy import deepcopy
from heapq import heappop, heappush
from math import inf
from typing import Callable, List, Tuple

from levels import *
from util import check_state, state_eq, p, prints, iswin

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


def _find_colours(state: List[List[str or int]]):
    return [elem[COLOR] for elem in state if elem[TYPE] == SQUARE]


def _get_squares(state: List[List[str or int]]) -> List[List[str or int]]:
    return [elem for elem in state if elem[TYPE] == SQUARE]


def _get_goal_for_colour(state: List[List[str or int]], colour: str):
    for elem in state:
        if elem[TYPE] == GOAL and elem[COLOR] == colour:
            return elem[X], elem[Y]

    return None, None


def _check_if(state, square, p):
    return any(elem for elem in state
        if (
            p(elem) and
            (
                (elem[TYPE] == SQUARE and elem[COLOR] != square[COLOR])
                or (elem[TYPE] == CHANGER and elem[DIR] != square[DIR])
            )
        )
    )


def _should_keep_state(state: List[List[str or int]]) -> bool:
    for square in _get_squares(state):
        x, y = _get_goal_for_colour(state, square[COLOR])
        if x is not None and y is not None:
            if square[DIR] == SOUTH and y > square[Y]:
                if not _check_if(state, square, lambda el: el[Y] <= square[Y]):
                    return False
            if square[DIR] == NORTH and y < square[Y]:
                if not _check_if(state, square, lambda el: el[Y] >= square[Y]):
                    return False
            if square[DIR] == EAST and x < square[X]:
                if not _check_if(state, square, lambda el: el[X] >= square[X]):
                    return False
            if square[DIR] == WEST and x > square[X]:
                if not _check_if(state, square, lambda el: el[X] <= square[X]):
                    return False

    return True


def _should_keep_state2(state: List[List[str or int]], bbox: List[int]) -> bool:
    for square in _get_squares(state):
        if (
            square[X] < bbox[0] or square[Y] < bbox[1]
            or square[X] > bbox[2] or square[Y] > bbox[3]
        ):
            return False

    return True


def _get_bbox(state: List[List[str or int]]) -> List[int]:
    bbox = [inf, inf, -inf, -inf]

    for elem in state:
        bbox[0] = min(bbox[0], elem[X])
        bbox[1] = min(bbox[1], elem[Y])
        bbox[2] = max(bbox[2], elem[X])
        bbox[3] = max(bbox[3], elem[Y])

    bbox[0] -= 1
    bbox[1] -= 1
    bbox[2] += 1
    bbox[3] += 1

    return bbox


def hash(state: List[List[str or int]]) -> str:
    squares = [(elem[X], elem[Y], elem[COLOR], elem[DIR])
        for elem in state if elem[TYPE] == SQUARE]
    squares.sort(key=lambda el: el[2])

    return str(squares)


def manhattan(state: List[List[str or int]]) -> int:
    dist = 0

    for square in _get_squares(state):
        x, y = _get_goal_for_colour(state, square[COLOR])
        if x is not None and y is not None:
            dist += abs(square[X] - x) + abs(square[Y] - y)

    return dist


def _solve_astar(
    initial_state: List[List[str or int]],
    h
) -> Tuple[List[str], List[List[List[str or int]]], int]:
    frontier = []
    heappush(frontier, (0 + h(initial_state), initial_state))

    discovered = {hash(initial_state): (0, [])}
    colours = _find_colours(initial_state)

    num_explored = 1
    bbox = _get_bbox(initial_state)
    found = iswin(initial_state)

    while not found and frontier:
        crt_state = heappop(frontier)[1]
        crt_g, cmds = discovered[hash(crt_state)]

        for colour in colours:
            next_g = crt_g + 1
            next_s = press(colour, crt_state)

            if iswin(next_s):
                cmds.append(colour)
                found = True
                break

            if (
                not _should_keep_state(next_s)
                or not _should_keep_state2(next_s, bbox)
            ):
                continue

            next_s_h = hash(next_s)

            if next_s_h not in discovered or next_g < discovered[next_s_h][0]:
                discovered[next_s_h] = (next_g, cmds + [colour])
                heappush(frontier, (next_g + h(next_s), next_s))
                num_explored += 1

    explored = [initial_state]
    for cmd in cmds:
        initial_state = press(cmd, initial_state)
        explored.append(initial_state)

    return cmds, explored, num_explored


def solve(
    initial_state: List[List[str or int]]
) -> Tuple[List[str], List[List[List[str or int]]], int]:
    return _solve_astar(initial_state, manhattan)


def play(initstate: List[List[str or int]], plan: List[str], small: bool=False):
    state = initstate
    print(p(state, small))
    for action in plan:
        state = press(action, state)
        print(p(state, small))

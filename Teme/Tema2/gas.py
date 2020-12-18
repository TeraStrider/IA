from typing import List, Tuple
from levels import *
from util import check_state, state_eq, p, prints

"""
#######################################
################ TODOs ################
#######################################
"""


def press(color: str, state: List[List[str or int]]) -> List[List[str or int]]:
    raise NotImplementedError("Not implemented by student")


def solve(initial_state: List[List[str or int]]) -> Tuple[List[str], List[List[List[str or int]]], int]:
    raise NotImplementedError("Not implemented by student")


def play(initstate: List[List[str or int]], plan: List[str], small: bool=False):
    state = initstate
    print(p(state, small))
    for action in plan:
        state = press(action, state)
        print(p(state, small))


# play(levels['level10'], [RED, RED, RED, DARK, DARK, BLUE, BLUE, BLUE])
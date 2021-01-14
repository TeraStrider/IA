#!/usr/bin/python

from gas import press, solve
from util import p, iswin, state_eq, prints
from levels import *
from typing import Callable, List, Tuple
from argparse import ArgumentParser
import sys, traceback
from statistics import median


"""
#######################################
################ TESTS ################
#######################################
"""

APPLY_OP_TESTS = [
    {
        'start_state': [[0, 0, 'GOAL', 'ORANGE'], [0, 1, 'GOAL', 'DARK'], [0, 2, 'CHANGER', None, 'v'],
                        [2, 1, 'CHANGER', None, '<'], [1, -1, 'SQUARE', 'DARK', '^'], [1, 0, 'SQUARE', 'ORANGE', '>']],
        'end_state': [[0, 0, 'GOAL', 'ORANGE'], [0, 1, 'GOAL', 'DARK'], [0, 2, 'CHANGER', None, 'v'],
                      [2, 1, 'CHANGER', None, '<'], [1, 1, 'SQUARE', 'ORANGE', '<'], [0, 2, 'SQUARE', 'DARK', 'v']],
        'ops': ['DARK', 'ORANGE', 'DARK', 'ORANGE', 'DARK']},

    {
        'start_state': [[0, 2, 'CHANGER', None, 'v'], [0, 1, 'CHANGER', None, '>'], [3, 2, 'CHANGER', None, '<'],
                        [1, 0, 'GOAL', 'BLUE'], [1, 1, 'GOAL', 'RED'], [2, 0, 'SQUARE', 'BLUE', '^'],
                        [0, 1, 'SQUARE', 'RED', '>']],
        'end_state': [[0, 2, 'CHANGER', None, 'v'], [0, 1, 'CHANGER', None, '>'], [3, 2, 'CHANGER', None, '<'],
                      [1, 0, 'GOAL', 'BLUE'], [1, 1, 'GOAL', 'RED'], [0, 1, 'SQUARE', 'BLUE', '>'],
                      [0, 2, 'SQUARE', 'RED', 'v']],
        'ops': ['RED', 'RED', 'BLUE', 'RED', 'BLUE', 'RED', 'RED', 'BLUE', 'RED']},

    {
        'start_state': [[-2, 1, 'CHANGER', None, 'v'], [-1, 0, 'CHANGER', None, 'v'], [0, -1, 'CHANGER', None, '^'],
                        [-2, -2, 'CHANGER', None, '>'], [-1, -1, 'CHANGER', None, '>'], [1, -2, 'CHANGER', None, '^'],
                        [1, 0, 'CHANGER', None, '<'], [0, 0, 'GOAL', 'DARK'], [0, 2, 'GOAL', 'BLUE'],
                        [0, 4, 'GOAL', 'RED'],
                        [-1, 1, 'SQUARE', 'DARK', '<'], [-2, 1, 'SQUARE', 'BLUE', 'v'], [0, 3, 'SQUARE', 'RED', '^']],
        'end_state': [[-2, 1, 'CHANGER', None, 'v'], [-1, 0, 'CHANGER', None, 'v'], [0, -1, 'CHANGER', None, '^'],
                      [-2, -2, 'CHANGER', None, '>'], [-1, -1, 'CHANGER', None, '>'], [1, -2, 'CHANGER', None, '^'],
                      [1, 0, 'CHANGER', None, '<'], [0, 0, 'GOAL', 'DARK'], [0, 2, 'GOAL', 'BLUE'],
                      [0, 4, 'GOAL', 'RED'],
                      [-1, 1, 'SQUARE', 'DARK', '<'], [0, 4, 'SQUARE', 'RED', '^'], [0, -1, 'SQUARE', 'BLUE', '^']],
        'ops': ['RED', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE']},

    {
        'start_state': [[0, 0, 'GOAL', 'RED'], [-2, 0, 'GOAL', 'BLUE'], [2, 0, 'GOAL', 'DARK'],
                        [-1, 1, 'CHANGER', None, '>'],
                        [0, 2, 'CHANGER', None, 'v'], [1, 0, 'CHANGER', None, '<'], [0, -2, 'CHANGER', None, '^'],
                        [-1, 0, 'SQUARE', 'DARK', '>'], [0, 0, 'SQUARE', 'RED', '^'], [0, 1, 'SQUARE', 'BLUE', '<']],

        'end_state': [[0, 0, 'GOAL', 'RED'], [-2, 0, 'GOAL', 'BLUE'], [2, 0, 'GOAL', 'DARK'],
                      [-1, 1, 'CHANGER', None, '>'],
                      [0, 2, 'CHANGER', None, 'v'], [1, 0, 'CHANGER', None, '<'], [0, -2, 'CHANGER', None, '^'],
                      [0, 1, 'SQUARE', 'RED', 'v'], [2, 0, 'SQUARE', 'DARK', '<'], [-2, 0, 'SQUARE', 'BLUE', '<']],
        'ops': ['BLUE', 'RED', 'DARK', 'DARK', 'RED', 'BLUE', 'RED', 'BLUE', 'BLUE', 'BLUE', 'BLUE']},

    {
        'start_state': [[0, 0, 'GOAL', 'ORANGE'], [0, 1, 'GOAL', 'DARK'], [0, 2, 'CHANGER', None, 'v'],
                     [2, 1, 'CHANGER', None, '<'], [1, -1, 'SQUARE', 'DARK', '^'], [1, 0, 'SQUARE', 'ORANGE', '>']],
        'end_state': [[0, 0, 'GOAL', 'ORANGE'], [0, 1, 'GOAL', 'DARK'], [0, 2, 'CHANGER', None, 'v'],
                   [2, 1, 'CHANGER', None, '<'], [0, 2, 'SQUARE', 'DARK', 'v'], [0, 1, 'SQUARE', 'ORANGE', '<']],
        'ops': ['DARK', 'ORANGE', 'DARK', 'ORANGE', 'DARK', 'ORANGE']},

    {
        'start_state': [[0, 2, 'SQUARE', 'RED', 'v'], [0, 2, 'CHANGER', None, 'v'], [0, 1, 'CHANGER', None, '>'],
                        [3, 2, 'CHANGER', None, '<'], [1, 0, 'GOAL', 'BLUE'], [1, 1, 'GOAL', 'RED'],
                        [2, 0, 'SQUARE', 'BLUE', '^']],
        'end_state': [[0, 2, 'CHANGER', None, 'v'], [0, 1, 'CHANGER', None, '>'], [3, 2, 'CHANGER', None, '<'],
                      [1, 0, 'GOAL', 'BLUE'], [1, 1, 'GOAL', 'RED'], [1, 2, 'SQUARE', 'RED', '<'],
                      [0, 2, 'SQUARE', 'BLUE', 'v']],
        'ops': ['RED', 'RED', 'RED', 'BLUE', 'RED', 'BLUE', 'RED', 'RED']},

    {
        'start_state': [[-2, 1, 'SQUARE', 'RED', 'v'], [-2, 1, 'CHANGER', None, 'v'], [-1, 0, 'CHANGER', None, 'v'],
                        [0, -1, 'CHANGER', None, '^'], [-2, -2, 'CHANGER', None, '>'], [-1, -1, 'CHANGER', None, '>'],
                        [1, -2, 'CHANGER', None, '^'], [1, 0, 'CHANGER', None, '<'], [0, 0, 'GOAL', 'DARK'],
                        [0, 2, 'GOAL', 'BLUE'], [0, 4, 'GOAL', 'RED'], [0, 1, 'SQUARE', 'BLUE', '^'],
                        [1, 0, 'SQUARE', 'DARK', '<']],
        'end_state': [[-2, 1, 'CHANGER', None, 'v'], [-1, 0, 'CHANGER', None, 'v'], [0, -1, 'CHANGER', None, '^'],
                      [-2, -2, 'CHANGER', None, '>'], [-1, -1, 'CHANGER', None, '>'], [1, -2, 'CHANGER', None, '^'],
                      [1, 0, 'CHANGER', None, '<'], [0, 0, 'GOAL', 'DARK'], [0, 2, 'GOAL', 'BLUE'],
                      [0, 4, 'GOAL', 'RED'], [-1, 1, 'SQUARE', 'DARK', '<'], [0, 4, 'SQUARE', 'RED', '^'],
                      [0, 0, 'SQUARE', 'BLUE', '^']],
        'ops': ['RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'DARK',
                'DARK', 'RED', 'RED', 'RED', 'RED', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE',
                'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE']
    },

    {
        'start_state': [[0, 0, 'GOAL', 'RED'], [-2, 0, 'GOAL', 'BLUE'], [2, 0, 'GOAL', 'DARK'],
                        [-1, 1, 'CHANGER', None, '>'], [0, 2, 'CHANGER', None, 'v'], [1, 0, 'CHANGER', None, '<'],
                        [0, -2, 'CHANGER', None, '^'], [0, 2, 'SQUARE', 'BLUE', 'v'], [1, 0, 'SQUARE', 'RED', '<'],
                        [0, 1, 'SQUARE', 'DARK', '>']],
        'end_state': [[0, 0, 'GOAL', 'RED'], [-2, 0, 'GOAL', 'BLUE'], [2, 0, 'GOAL', 'DARK'],
                      [-1, 1, 'CHANGER', None, '>'], [0, 2, 'CHANGER', None, 'v'], [1, 0, 'CHANGER', None, '<'],
                      [0, -2, 'CHANGER', None, '^'], [0, 1, 'SQUARE', 'RED', 'v'], [2, 0, 'SQUARE', 'DARK', '<'],
                      [0, 0, 'SQUARE', 'BLUE', '<']],
        'ops': ['BLUE', 'RED', 'BLUE', 'BLUE', 'RED', 'DARK', 'BLUE', 'RED', 'BLUE', 'RED', 'DARK', 'DARK', 'RED',
                'BLUE', 'RED', 'BLUE', 'BLUE']
    },

    {
        'start_state': [[0, 0, 'GOAL', 'ORANGE'], [0, 1, 'GOAL', 'DARK'], [0, 2, 'CHANGER', None, 'v'],
                        [2, 1, 'CHANGER', None, '<'], [-1, 0, 'SQUARE', 'ORANGE', '>'], [1, -1, 'SQUARE', 'DARK', '^']],
        'end_state': [[0, 0, 'GOAL', 'ORANGE'], [0, 1, 'GOAL', 'DARK'], [0, 2, 'CHANGER', None, 'v'],
                      [2, 1, 'CHANGER', None, '<'], [1, 1, 'SQUARE', 'ORANGE', '<'], [0, 2, 'SQUARE', 'DARK', 'v']],
        'ops': ['ORANGE', 'ORANGE', 'DARK', 'ORANGE', 'DARK', 'ORANGE', 'DARK']},

    {
        'start_state': [[0, 2, 'CHANGER', None, 'v'], [0, 1, 'CHANGER', None, '>'], [3, 2, 'CHANGER', None, '<'],
                        [1, 0, 'GOAL', 'BLUE'], [1, 1, 'GOAL', 'RED'], [2, 0, 'SQUARE', 'BLUE', '^'],
                        [0, 1, 'SQUARE', 'RED', '>']],
        'end_state': [[0, 2, 'CHANGER', None, 'v'], [0, 1, 'CHANGER', None, '>'], [3, 2, 'CHANGER', None, '<'],
                      [1, 0, 'GOAL', 'BLUE'], [1, 1, 'GOAL', 'RED'], [1, 2, 'SQUARE', 'RED', '<'],
                      [0, 1, 'SQUARE', 'BLUE', '>']],
        'ops': ['RED', 'RED', 'BLUE', 'RED', 'BLUE', 'RED', 'RED', 'BLUE']},

    {
        'start_state': [[-2, 1, 'CHANGER', None, 'v'], [-1, 0, 'CHANGER', None, 'v'], [0, -1, 'CHANGER', None, '^'],
                        [-2, -2, 'CHANGER', None, '>'], [-1, -1, 'CHANGER', None, '>'], [1, -2, 'CHANGER', None, '^'],
                        [1, 0, 'CHANGER', None, '<'], [0, 0, 'GOAL', 'DARK'], [0, 2, 'GOAL', 'BLUE'],
                        [0, 4, 'GOAL', 'RED'], [0, 1, 'SQUARE', 'BLUE', '^'], [1, 1, 'SQUARE', 'DARK', '<'],
                        [-1, 0, 'SQUARE', 'RED', 'v']],
        'end_state': [[-2, 1, 'CHANGER', None, 'v'], [-1, 0, 'CHANGER', None, 'v'], [0, -1, 'CHANGER', None, '^'],
                      [-2, -2, 'CHANGER', None, '>'], [-1, -1, 'CHANGER', None, '>'], [1, -2, 'CHANGER', None, '^'],
                      [1, 0, 'CHANGER', None, '<'], [0, 0, 'GOAL', 'DARK'], [0, 2, 'GOAL', 'BLUE'],
                      [0, 4, 'GOAL', 'RED'], [-1, 1, 'SQUARE', 'DARK', '<'], [0, 4, 'SQUARE', 'RED', '^'],
                      [-1, -1, 'SQUARE', 'BLUE', '>']],
        'ops': ['RED', 'RED', 'RED', 'DARK', 'DARK', 'RED', 'RED', 'RED', 'RED', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE',
                'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE']},

    {
        'start_state': [[0, 0, 'GOAL', 'RED'], [-2, 0, 'GOAL', 'BLUE'], [2, 0, 'GOAL', 'DARK'],
                        [-1, 1, 'CHANGER', None, '>'], [0, 2, 'CHANGER', None, 'v'], [1, 0, 'CHANGER', None, '<'],
                        [0, -2, 'CHANGER', None, '^'], [0, -1, 'SQUARE', 'RED', '^'], [0, 0, 'SQUARE', 'DARK', '>'],
                        [1, 0, 'SQUARE', 'BLUE', '<']],
        'end_state': [[0, 0, 'GOAL', 'RED'], [-2, 0, 'GOAL', 'BLUE'], [2, 0, 'GOAL', 'DARK'],
                      [-1, 1, 'CHANGER', None, '>'], [0, 2, 'CHANGER', None, 'v'], [1, 0, 'CHANGER', None, '<'],
                      [0, -2, 'CHANGER', None, '^'], [1, 0, 'SQUARE', 'DARK', '<'], [0, 1, 'SQUARE', 'RED', 'v'],
                      [0, 0, 'SQUARE', 'BLUE', '>']],
        'ops': ['BLUE', 'RED', 'BLUE', 'RED', 'DARK', 'DARK', 'RED', 'BLUE', 'RED']},

    {
        'start_state': [[0, 0, 'GOAL', 'ORANGE'], [0, 1, 'GOAL', 'DARK'], [0, 2, 'CHANGER', None, 'v'],
                        [2, 1, 'CHANGER', None, '<'], [1, 0, 'SQUARE', 'DARK', '^'], [2, 1, 'SQUARE', 'ORANGE', '<']],
        'end_state': [[0, 0, 'GOAL', 'ORANGE'], [0, 1, 'GOAL', 'DARK'], [0, 2, 'CHANGER', None, 'v'],
                      [2, 1, 'CHANGER', None, '<'], [0, 1, 'SQUARE', 'DARK', 'v'], [0, 0, 'SQUARE', 'ORANGE', '<']],
        'ops': ['DARK', 'ORANGE', 'DARK', 'ORANGE', 'DARK']},

    {
        'start_state': [[0, 2, 'CHANGER', None, 'v'], [0, 1, 'CHANGER', None, '>'], [3, 2, 'CHANGER', None, '<'],
                        [1, 0, 'GOAL', 'BLUE'], [1, 1, 'GOAL', 'RED'], [2, 0, 'SQUARE', 'BLUE', '^'],
                        [2, 1, 'SQUARE', 'RED', '>']],
        'end_state': [[0, 2, 'CHANGER', None, 'v'], [0, 1, 'CHANGER', None, '>'], [3, 2, 'CHANGER', None, '<'],
                      [1, 0, 'GOAL', 'BLUE'], [1, 1, 'GOAL', 'RED'], [1, 2, 'SQUARE', 'RED', '<'],
                      [0, 2, 'SQUARE', 'BLUE', 'v']], 'ops': ['BLUE', 'RED', 'BLUE', 'RED', 'RED']},

    {
        'start_state': [[-2, 1, 'SQUARE', 'RED', 'v'], [-2, 1, 'CHANGER', None, 'v'], [-1, 0, 'CHANGER', None, 'v'],
                        [0, -1, 'CHANGER', None, '^'], [-2, -2, 'CHANGER', None, '>'], [-1, -1, 'CHANGER', None, '>'],
                        [1, -2, 'CHANGER', None, '^'], [1, 0, 'CHANGER', None, '<'], [0, 0, 'GOAL', 'DARK'],
                        [0, 2, 'GOAL', 'BLUE'], [0, 4, 'GOAL', 'RED'], [1, -1, 'SQUARE', 'DARK', '^'],
                        [0, 1, 'SQUARE', 'BLUE', '^']],
        'end_state': [[-2, 1, 'CHANGER', None, 'v'], [-1, 0, 'CHANGER', None, 'v'], [0, -1, 'CHANGER', None, '^'],
                      [-2, -2, 'CHANGER', None, '>'], [-1, -1, 'CHANGER', None, '>'], [1, -2, 'CHANGER', None, '^'],
                      [1, 0, 'CHANGER', None, '<'], [0, 0, 'GOAL', 'DARK'], [0, 2, 'GOAL', 'BLUE'],
                      [0, 4, 'GOAL', 'RED'], [-1, 1, 'SQUARE', 'DARK', '<'], [0, 4, 'SQUARE', 'RED', '^'],
                      [0, 0, 'SQUARE', 'BLUE', '^']],
        'ops': ['DARK', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED', 'RED',
                'DARK', 'DARK', 'RED', 'RED', 'RED', 'RED', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE',
                'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE', 'BLUE']},

    {
        'start_state': [[0, 0, 'GOAL', 'RED'], [-2, 0, 'GOAL', 'BLUE'], [2, 0, 'GOAL', 'DARK'],
                        [-1, 1, 'CHANGER', None, '>'], [0, 2, 'CHANGER', None, 'v'], [1, 0, 'CHANGER', None, '<'],
                        [0, -2, 'CHANGER', None, '^'], [-1, 0, 'SQUARE', 'DARK', '>'], [0, 0, 'SQUARE', 'RED', '^'],
                        [0, 1, 'SQUARE', 'BLUE', '<']],
        'end_state': [[0, 0, 'GOAL', 'RED'], [-2, 0, 'GOAL', 'BLUE'], [2, 0, 'GOAL', 'DARK'],
                      [-1, 1, 'CHANGER', None, '>'], [0, 2, 'CHANGER', None, 'v'], [1, 0, 'CHANGER', None, '<'],
                      [0, -2, 'CHANGER', None, '^'], [-1, 1, 'SQUARE', 'BLUE', '>'], [0, 1, 'SQUARE', 'RED', '^'],
                      [1, 0, 'SQUARE', 'DARK', '<']], 'ops': ['BLUE', 'RED', 'DARK', 'DARK']
    }]


APPLY_OP_TESTS_SINGLE = {
    "Test 1": {
        "start_state": [
            [0, 2, GOAL, RED],
            [2, 2, GOAL, ORANGE],
            [1, 1, GOAL, BLUE],
            [2, 0, GOAL, DARK],
            [1, 2, SQUARE, DARK, SOUTH],
            [0, 1, SQUARE, ORANGE, EAST],
            [1, 0, SQUARE, BLUE, NORTH],
            [2, 1, SQUARE, RED, WEST]],
        "end_state": [
            [0, 2, GOAL, RED],
            [2, 2, GOAL, ORANGE],
            [1, 1, GOAL, BLUE],
            [2, 0, GOAL, DARK],
            [1, 2, SQUARE, DARK, SOUTH],
            [0, 1, SQUARE, ORANGE, EAST],
            [1, 0, SQUARE, BLUE, NORTH],
            [1, 1, SQUARE, RED, WEST]],
        "ops": ['RED']
    },
    "Test 2": {
        "start_state": [
            [0, 2, GOAL, RED],
            [2, 2, GOAL, ORANGE],
            [1, 1, GOAL, BLUE],
            [2, 0, GOAL, DARK],
            [1, 2, SQUARE, DARK, SOUTH],
            [0, 1, SQUARE, ORANGE, EAST],
            [1, 0, SQUARE, BLUE, NORTH],
            [1, 1, SQUARE, RED, WEST]
        ],
        "end_state": [
            [0, 2, GOAL, RED],
            [2, 2, GOAL, ORANGE],
            [1, 1, GOAL, BLUE],
            [2, 0, GOAL, DARK],
            [1, 1, SQUARE, DARK, SOUTH],
            [0, 1, SQUARE, ORANGE, EAST],
            [1, -1, SQUARE, BLUE, NORTH],
            [1, 0, SQUARE, RED, WEST],
        ],
        "ops": ['DARK']
    },
    "Test 3": {
        "start_state": [
            [2, 3, GOAL, RED],
            [2, 2, GOAL, GREEN],
            [2, 1, GOAL, ORANGE],
            [0, 3, GOAL, DARK],
            [0, 0, CHANGER, None, EAST],
            [2, 0, CHANGER, None, NORTH],
            [2, 4, CHANGER, None, WEST],
            [0, 1, CHANGER, None, SOUTH],
            [0, 2, CHANGER, None, NORTH],
            [0, 4, CHANGER, None, SOUTH],
            [0, 2, SQUARE, ORANGE, NORTH],
            [0, 1, SQUARE, DARK, SOUTH],
            [0, 3, SQUARE, GREEN, SOUTH],
            [1, 4, SQUARE, RED, WEST],
        ],
        "end_state": [
            [2, 3, GOAL, RED],
            [2, 2, GOAL, GREEN],
            [2, 1, GOAL, ORANGE],
            [0, 3, GOAL, DARK],
            [0, 0, CHANGER, None, EAST],
            [2, 0, CHANGER, None, NORTH],
            [2, 4, CHANGER, None, WEST],
            [0, 1, CHANGER, None, SOUTH],
            [0, 2, CHANGER, None, NORTH],
            [0, 4, CHANGER, None, SOUTH],
            [0, 2, SQUARE, ORANGE, NORTH],
            [0, 1, SQUARE, DARK, SOUTH],
            [0, 3, SQUARE, GREEN, SOUTH],
            [0, 4, SQUARE, RED, SOUTH],
        ],
        "ops": ['RED']
    },
    "Test 4": {
        "start_state": [
            [2, 3, GOAL, RED],
            [2, 2, GOAL, GREEN],
            [2, 1, GOAL, ORANGE],
            [0, 3, GOAL, DARK],
            [0, 0, CHANGER, None, EAST],
            [2, 0, CHANGER, None, NORTH],
            [2, 4, CHANGER, None, WEST],
            [0, 1, CHANGER, None, SOUTH],
            [0, 2, CHANGER, None, NORTH],
            [0, 4, CHANGER, None, SOUTH],
            [0, 2, SQUARE, ORANGE, NORTH],
            [0, 1, SQUARE, DARK, SOUTH],
            [0, 3, SQUARE, GREEN, SOUTH],
            [0, 4, SQUARE, RED, SOUTH],
        ],
        "end_state": [
            [2, 3, GOAL, RED],
            [2, 2, GOAL, GREEN],
            [2, 1, GOAL, ORANGE],
            [0, 3, GOAL, DARK],
            [0, 0, CHANGER, None, EAST],
            [2, 0, CHANGER, None, NORTH],
            [2, 4, CHANGER, None, WEST],
            [0, 1, CHANGER, None, SOUTH],
            [0, 2, CHANGER, None, NORTH],
            [0, 4, CHANGER, None, SOUTH],
            [0, 0, SQUARE, ORANGE, EAST],
            [0, -1, SQUARE, DARK, EAST],
            [0, 2, SQUARE, GREEN, NORTH],
            [0, 3, SQUARE, RED, SOUTH],
        ],
        "ops": ['RED', 'ORANGE']
    },
    "Test 5": {
        "start_state": [
            [0, 3, GOAL, DARK],
            [0, 0, CHANGER, None, NORTH],
            [0, 2, CHANGER, None, EAST],
            [0, 4, CHANGER, None, SOUTH],
            [2, 2, CHANGER, None, NORTH],
            [0, 1, SQUARE, GREEN, EAST],
            [0, 2, SQUARE, DARK, EAST],
            [0, 3, SQUARE, BLUE, SOUTH],
            [0, 4, SQUARE, RED, SOUTH],
        ],
        "end_state": [
            [0, 3, GOAL, DARK],
            [0, 0, CHANGER, None, NORTH],
            [0, 2, CHANGER, None, EAST],
            [0, 4, CHANGER, None, SOUTH],
            [2, 2, CHANGER, None, NORTH],
            [0, 0, SQUARE, GREEN, NORTH],
            [0, 1, SQUARE, DARK, EAST],
            [0, 2, SQUARE, BLUE, EAST],
            [0, 3, SQUARE, RED, SOUTH],
        ],
        "ops": ['RED']
    },
    "Test 6": {
        "start_state": [
            [0, 3, GOAL, DARK],
            [0, 0, CHANGER, None, NORTH],
            [0, 2, CHANGER, None, EAST],
            [0, 4, CHANGER, None, SOUTH],
            [2, 2, CHANGER, None, NORTH],
            [0, 1, SQUARE, GREEN, EAST],
            [0, 2, SQUARE, DARK, EAST],
            [0, 3, SQUARE, BLUE, SOUTH],
            [0, 4, SQUARE, RED, SOUTH],
        ],
        "end_state": [
            [0, 3, GOAL, DARK],
            [0, 0, CHANGER, None, NORTH],
            [0, 2, CHANGER, None, EAST],
            [0, 4, CHANGER, None, SOUTH],
            [2, 2, CHANGER, None, NORTH],
            [0, 2, SQUARE, GREEN, EAST],
            [0, 3, SQUARE, DARK, EAST],
            [0, 4, SQUARE, BLUE, SOUTH],
            [2, 2, SQUARE, RED, NORTH],
        ],
        "ops": ['RED', 'RED', 'RED', 'RED', 'GREEN', 'GREEN', 'GREEN']
    },

}



"""
########################################
############### AUXILIARY ##############
########################################
"""


def get_aligned_squares(state_squares, op):
    deltas = {EAST: (+1, 0), WEST: (-1, 0), NORTH: (0, +1), SOUTH: (0, -1)}

    op_x = state_squares[op][0]
    op_y = state_squares[op][1]
    op_dir = state_squares[op][2]

    aligned_squares = []
    visited_squares = [op]
    x, y = (op_x + deltas[op_dir][0], op_y + deltas[op_dir][1])

    for i in range(len(state_squares) - 1):
        for sq in state_squares:
            if sq not in visited_squares:
                if state_squares[sq][0] == x and state_squares[sq][1] == y:
                    aligned_squares.append(sq)
                    x, y = (x + deltas[op_dir][0], y + deltas[op_dir][1])
                    visited_squares.append(sq)
                    break

    return aligned_squares


def check_adjacent_states(state1: List[List[str or int]], op: str, state2: List[List[str or int]]) -> bool:
    """
    Verify if two states are "adjacent", i.e. `state2' can be obtained from `state1', when applying `op'
    :param state1: A state in GAS
    :param op: The name of the square which is pressed
    :param state2: A state in GAS
    :return: True if state2 follows from state1 by executing op, False otherwise
    """
    state1_squares = {e[COLOR]: e[XY]+[e[DIR]] for e in state1 if e[TYPE] == SQUARE}
    state2_squares = {e[COLOR]: e[XY]+[e[DIR]] for e in state2 if e[TYPE] == SQUARE}

    changers = {(e[X], e[Y]) : e[DIR] for e in state1 if e[TYPE] == CHANGER}

    deltas = {EAST: (+1, 0), WEST: (-1, 0), NORTH: (0, +1), SOUTH: (0, -1)}

    op_x = state1_squares[op][0]
    op_y = state1_squares[op][1]
    op_dir = state1_squares[op][2]
    next_x, next_y = (op_x + deltas[op_dir][0], op_y + deltas[op_dir][1])

    aligned_squares = get_aligned_squares(state1_squares, op)

    # check if operator square is on the right position
    if state2_squares[op][0] != next_x or state2_squares[op][1] != next_y:
        return False

    # check if it has the right orientation
    changer_dir = changers.get((next_x, next_y), None)
    if changer_dir and state2_squares[op][2] != changer_dir:
        return False

    # check squares which are not aligned with op to see that they remain in place
    unaligend_squares = [sq for sq in state1_squares if sq != op and sq not in aligned_squares]
    for sq in unaligend_squares:
        if state1_squares[sq][0] != state2_squares[sq][0] or state1_squares[sq][1] != state2_squares[sq][1]:
            return False

    # check the positions and orientations of the aligned_squares
    for sq in aligned_squares:
        next_x, next_y = (state1_squares[sq][0] + deltas[op_dir][0], state1_squares[sq][1] + deltas[op_dir][1])
        if state2_squares[sq][0] != next_x or state2_squares[sq][1] != next_y:
            return False

        changer_dir = changers.get((next_x, next_y), None)
        if changer_dir and state2_squares[sq][2] != changer_dir:
            return False

    return True


"""
########################################
################# TESTS ################
########################################
"""

def check_apply_ops(apply_op_func: Callable[[str, List[List[str or int]]], List[List[str or int]]] = press, verbose: bool = False, test: str or int = None, single: bool = False):
    """
    Test that applies your action implementation.
    :param apply_op_func: The function that applies an action in a state. It will take in two parameters:
    an action (the name of a square to press) and a state (a situation of the board). The function is expected
    to return the next state.

    The default value is your implementation of the `apply' method from the support code.
    :param verbose: True for a verbose output.
    :param test: a single test to run, or the test to begin with.
    :param single: run a single test or continue from the given start test.
    :return: successfull tests and total tests.
    """
    S = True
    ct = 0
    total = len(APPLY_OP_TESTS_SINGLE) + len(APPLY_OP_TESTS)
    for test_name, test_case in list(APPLY_OP_TESTS_SINGLE.items()) + list(enumerate(APPLY_OP_TESTS)):
        if test:
            if test == test_name: test = None
            else: continue

        if isinstance(test_name, int): test_name = "Test ops " + str(test_name)
        state = test_case["start_state"]
        print(">>> ", test_name, end = "")
        if verbose: print(":",  ", ".join(test_case["ops"])); prints(p(state, S), " -> ", p(test_case["end_state"], S))
        print("... ", end="", flush=True)
        for op in test_case["ops"]:
            state = apply_op_func(op, state)

        if state_eq(state, test_case["end_state"]):
            print("successful!")
            ct += 1
            if verbose: print("\n----------------\n\n")
        else:
            print("failed:")
            print("End state is:\n%s" % p(state, small=True))
            print("Should be:\n%s" % p(test_case["end_state"], small=True))
            if not verbose: print("Test was:",  ", ".join(test_case["ops"])); prints(p(test_case["start_state"], S), " -> ", p(test_case["end_state"], S))
        if single: break
#         print("----------------")
    print(ct, "/", total, "operations tests successful")
    return ct, total


def check_plan(level: List[List[str or int]], plan: List[str], states: List[List[List[str or int]]]) -> Tuple[bool, str]:
    """
    Check if the provided plan is correct by verifying that the end state is a "win" for the specified level
    :param level: start state characterizing a level of the GAS game
    :param plan: a list of operators (names of squares to press in order)
    :param states: the list of states produced by the execution of the plan starting from the initial state
    :return: A tuple (valid, obs) where `valid' is True if the plan is valid, False otherwise, and `obs' is an
    observation string containing reason for rejection if the plan is invalid.
    """
    if not state_eq(level, states[0]):
        return False, "Starting states do not match! Level is\n%s\nFirst state is%s" % (p(level, small=True),
                                                                                        p(states[0], small=True))
    if not iswin(states[-1]):
        return False, "End state is not a win state!\n%s" % p(states[-1], small=True)

    if len(plan) != len(states) - 1:
        return False, "Mismatch in length of plan and explored states. Plan length: %i, States length: %i" \
               % (len(plan), len(states))

    state1 = states[0]
    for idx, op in enumerate(plan):
        state2 = states[idx + 1]
        if not check_adjacent_states(state1, op, state2):
            return False, "States not in sequence!\nState\n%s\ndoes not follow from state\n%s\nby pressing %s" \
                % (p(state2, small=True), p(state1, small=True), op)
        state1 = state2

    return True, "Plan OK"


def check_plans(verbose: bool = False, test: str = None, single: bool = False):
    """
    :param verbose: True for a verbose output.
    :param test: a single test to run, or the test to begin with.
    :param single: run a single test or continue from the given start test.
    :return: successfull tests and total tests, indications of going over bounds.
    """
    ct = inbounds = inbounds_ext = 0
    overs = []
    for level in levels:
        if test:
            if test == level: test = None
            else: continue

        print(">>> Checking plan for level", level, "... ", end="", flush = True)
        initial_state = levels[level]

        try:
            plan, states, nr_discovered = solve(initial_state)
        except:
            print("plan generation raised exception:", sys.exc_info())
            traceback.print_exc()
            print("----------------")
            continue

        if verbose:
            limit = 80
            print(" got plan:", )
            printer = []
            cw = 0
            for i, s in enumerate(states):
                w = len(p(s, True).split("\n")[0]) + (len(plan[i]) if i < len(plan) else 0)  + 2
                if cw + w > limit:
                    prints(*printer)
                    print()
                    printer = ["   "]
                    cw = 3
                cw += w
                printer.append(p(s, True))
                if i < len(plan): printer.append(" " + plan[i] + " ")
            prints(*printer)
            print(nr_discovered, "states discovered,", len(plan), "operations in the plan.")

        valid, obs = check_plan(initial_state, plan, states)

        if valid:
            ct += 1
            print(obs, " ", end="")
            bound = DISCOVERED_STATE_LIMITS.get(level, 100)
            if nr_discovered < bound:
                print("Number of discovered states within bounds:", nr_discovered, "/", bound)
                inbounds += 1
            elif nr_discovered < bound * 3:
                overs.append(round((nr_discovered-bound)/bound*100))
                print("Number of discovered states within extended bounds:", nr_discovered, "/", bound, "+" + str(overs[-1])+"%")
                inbounds_ext += 1
            else:
                print("Number of discovered states not within extended bound", nr_discovered, "/", bound*3)
        else:
            print(obs)
        if verbose: print("----------------")
        if single: break

    print("Passed %i out of %i levels." % (ct, len(levels)))
    return ct, inbounds, inbounds_ext, len(levels), overs


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-t", "--test",
                            type=str,
                            choices=["plan", "apply_op", "all"],
                            required=False,
                            dest="test_type",
                            help="Test type")
    arg_parser.add_argument("-v", "--verbose",
                            action='store_true',
#                             action='store_false',
                            required=False,
                            dest="verbose",
                            help="Verbose")
    tests = [t[len("Test "):] for t in APPLY_OP_TESTS_SINGLE.keys()] + ["ops_"+str(i) for i in range(len(APPLY_OP_TESTS))] + list(levels.keys())
    arg_parser.add_argument("-single",
                            type=str,
                            choices=tests,
                            required=False,
                            dest="single",
                            help="Run the designated test.")
    arg_parser.add_argument("-from",
                            type=str,
                            choices=tests,
                            required=False,
                            dest="fromtest",
                            help="Run all tests in the category, starting with the designated test.")
    args = arg_parser.parse_args()
    print("======================= TESTING START ====================")
    verbose = args.verbose
    if verbose == None: verbose = False
    if args.single or args.fromtest:
        testfrom = args.single or args.fromtest
        singletest = args.single is not None
        if singletest: verbose = True
        if testfrom.startswith("level"):
            check_plans(verbose = verbose, single = singletest, test = testfrom)
        else:
            if len(testfrom) > 2: testfrom = int(testfrom[-2:].replace("_", " "))
            else: testfrom = "Test " + testfrom
            check_apply_ops(verbose = verbose, single = singletest, test = testfrom)
    elif not args.test_type or args.test_type == "all":
        ops_good, n_tests = check_apply_ops(verbose = verbose)
        plans_ok, inbounds, inbounds_ext, n_levels, overs = check_plans(verbose = verbose)
        print("===================================\nSummary")
        print(ops_good, "/", n_tests, "operation tests successful")
        print(plans_ok, "/", n_levels, "correct plans")
        print(inbounds, "/", n_levels, "efficient searches,")
        print(inbounds_ext, "/", n_levels, "less efficient searches", (" / ".join([str(o) + "%" for o in overs]) + " over the limit, median " + str(median(overs))+"%" if overs else ""))
        print(plans_ok - inbounds - inbounds_ext, "/", n_levels, "out of bounds searches")
    elif args.test_type == "apply_op":
        check_apply_ops(verbose = verbose)
    elif args.test_type == "plan":
        check_plans(verbose = verbose)

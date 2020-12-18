
types = SQUARE, GOAL, CHANGER = "SQUARE,GOAL,CHANGER".split(",")
dirs = NORTH, SOUTH, EAST, WEST = "^,v,>,<".split(",")
colors = RED, BLUE, DARK, ORANGE, GREEN = "RED,BLUE,DARK,ORANGE,GREEN".split(",")
indexes = X, Y, TYPE, COLOR, DIR = range(5)
XY = slice(X, Y+1)

# level = [[x, y, type, color, direction], ...]
levels = {}

levels['level1'] = [
    [0, 1, GOAL, BLUE],
    [0, 0, GOAL, RED],
    [0, 2, SQUARE, BLUE, SOUTH],
    [0, -1, SQUARE, RED, NORTH],
]

levels['level3'] = [
    [0, -2, GOAL, BLUE],
    [-2, 0, GOAL, RED],
    [0, 3, SQUARE, BLUE, SOUTH],
    [3, 1, SQUARE, RED, WEST],
]

levels['level4'] = [
    [0, 1, SQUARE, RED, SOUTH],
    [-1, 0, SQUARE, BLUE, EAST],
    [1, 0, SQUARE, DARK, SOUTH],
    [0, 0, GOAL, RED],
    [1, -1, GOAL, DARK],
    [2, -2, GOAL, BLUE],
]

levels['level5'] = [
    [0, 1, SQUARE, RED, SOUTH],
    [-1, 0, SQUARE, BLUE, EAST],
    [1, 0, SQUARE, DARK, SOUTH],
    [0, 0, GOAL, RED],
    [1, -1, GOAL, BLUE],
    [2, -2, GOAL, DARK],
]

levels['level7'] = [
    [0, 2, SQUARE, BLUE, SOUTH],
    [0, 0, CHANGER, None, EAST],
    [2, 0, CHANGER, None, NORTH],
    [2, 2, GOAL, BLUE],
]

levels['level9'] = [
    [0, 0, SQUARE, ORANGE, EAST],
    [2, 0, SQUARE, BLUE, NORTH],
    [1, 1, GOAL, ORANGE],
    [2, 1, GOAL, BLUE],
    [0, 0, CHANGER, None, EAST],
    [2, 0, CHANGER, None, NORTH],
    [3, 0, CHANGER, None, WEST],
]

levels['level10'] = [
    [0, 0, CHANGER, None, EAST],
    [-2, 0, GOAL, DARK],
    [-1, 0, GOAL, RED],
    [1, 0, GOAL, BLUE],
    [0, 2, SQUARE, RED, SOUTH],
    [0, -2, SQUARE, DARK, NORTH],
    [2, 0, SQUARE, BLUE, WEST],
]

levels['level12'] = [
    [0, 0, GOAL, ORANGE],
    [0, 1, GOAL, DARK],
    [0, 2, CHANGER, None, SOUTH],
    [2, 1, CHANGER, None, WEST],
    [-1, 0, SQUARE, ORANGE, EAST],
    [1, -1, SQUARE, DARK, NORTH],
]

levels['level13'] = [
    [0, 1, GOAL, BLUE],
    [0, 2, SQUARE, DARK, SOUTH],
    [0, 2, CHANGER, None, SOUTH],
    [0, 3, GOAL, DARK],
    [2, 0, SQUARE, ORANGE, WEST],
    [-1, -1, GOAL, ORANGE],
    [1, -2, SQUARE, BLUE, NORTH],
]

levels['level14'] = [
    [0, 2, GOAL, RED],
    [2, 2, GOAL, ORANGE],
    [1, 1, GOAL, BLUE],
    [2, 0, GOAL, DARK],
    [1, 2, SQUARE, DARK, SOUTH],
    [0, 1, SQUARE, ORANGE, EAST],
    [1, 0, SQUARE, BLUE, NORTH],
    [2, 1, SQUARE, RED, WEST],
]

levels['level15'] = [
    [0, 2, SQUARE, RED, SOUTH],
    [0, 2, CHANGER, None, SOUTH],
    [0, 1, CHANGER, None, EAST],
    [3, 2, CHANGER, None, WEST],
    [1, 0, GOAL, BLUE],
    [1, 1, GOAL, RED],
    [2, 0, SQUARE, BLUE, NORTH],
]

levels['level16'] = [
    [0, 2, CHANGER, None, EAST],
    [1, 0, CHANGER, None, NORTH],
    [2, 2, CHANGER, None, SOUTH],
    [2, 1, CHANGER, None, WEST],
    [3, 1, GOAL, BLUE],
    [0, 1, GOAL, RED],
    [0, 2, SQUARE, RED, EAST],
    [2, 1, SQUARE, BLUE, WEST],
]

levels['level17'] = [
    [0, 2, SQUARE, RED, SOUTH],
    [0, 1, SQUARE, DARK, EAST],
    [3, 2, SQUARE, BLUE, WEST],
    [0, 2, CHANGER, None, SOUTH],
    [0, 1, CHANGER, None, EAST],
    [3, 2, CHANGER, None, WEST],
    [2, 0, CHANGER, None, NORTH],
    [1, 1, GOAL, RED],
    [2, 1, GOAL, DARK],
    [3, 1, GOAL, BLUE],
]

levels['level18'] = [
    [0, 2, SQUARE, DARK, SOUTH],
    [0, 1, SQUARE, RED, EAST],
    [3, 2, SQUARE, BLUE, WEST],
    [0, 2, CHANGER, None, SOUTH],
    [0, 1, CHANGER, None, EAST],
    [3, 2, CHANGER, None, WEST],
    [2, 0, CHANGER, None, NORTH],
    [1, 1, GOAL, RED],
    [2, 1, GOAL, DARK],
    [3, 1, GOAL, BLUE],
]

levels['level19'] = [
    [-2, 1, SQUARE, RED, SOUTH],
    [-1, 0, SQUARE, BLUE, SOUTH],
    [0, -1, SQUARE, DARK, NORTH],
    [-2, 1, CHANGER, None, SOUTH],
    [-1, 0, CHANGER, None, SOUTH],
    [0, -1, CHANGER, None, NORTH],
    [-2, -2, CHANGER, None, EAST],
    [-1, -1, CHANGER, None, EAST],
    [1, -2, CHANGER, None, NORTH],
    [1, 0, CHANGER, None, WEST],
    [0, 0, GOAL, DARK],
    [0, 2, GOAL, BLUE],
    [0, 4, GOAL, RED],
]

levels['level31'] = [
    [0, 0, GOAL, RED],
    [-2, 0, GOAL, BLUE],
    [2, 0, GOAL, DARK],
    [-1, 1, CHANGER, None, EAST],
    [0, 2, CHANGER, None, SOUTH],
    [1, 0, CHANGER, None, WEST],
    [0, -2, CHANGER, None, NORTH],
    [-1, 1, SQUARE, DARK, EAST],
    [0, 2, SQUARE, BLUE, SOUTH],
    [1, 0, SQUARE, RED, WEST],
]

levels['level32'] = [
    [0, 0, CHANGER, None, NORTH],
    [0, 4, CHANGER, None, SOUTH],
    [-1, 2, CHANGER, None, EAST],
    [3, 1, CHANGER, None, WEST],
    [-1, 3, GOAL, BLUE],
    [1, 4, GOAL, RED],
    [0, 4, SQUARE, BLUE, SOUTH],
    [-1, 2, SQUARE, RED, EAST],
    [3, 3, SQUARE, DARK, SOUTH],
]

levels['level33'] = [
    [3, 0, CHANGER, None, NORTH],
    [1, 2, CHANGER, None, SOUTH],
    [1, 0, CHANGER, None, EAST],
    [4, 2, CHANGER, None, WEST],
    [0, 3, GOAL, BLUE],
    [1, 3, GOAL, RED],
    [2, 3, GOAL, DARK],
    [1, 2, SQUARE, BLUE, SOUTH],
    [1, 0, SQUARE, DARK, EAST],
    [3, 0, SQUARE, RED, NORTH],
]

levels['level34'] = [
    [0, 2, CHANGER, None, SOUTH],
    [0, 1, CHANGER, None, EAST],
    [2, 0, CHANGER, None, NORTH],
    [3, 2, CHANGER, None, WEST],
    [1, 0, GOAL, DARK],
    [2, 1, GOAL, RED],
    [3, 0, GOAL, BLUE],
    [0, 2, SQUARE, DARK, SOUTH],
    [0, 1, SQUARE, RED, EAST],
    [3, 2, SQUARE, BLUE, WEST],
]

levels['level35'] = [
    [0, 4, CHANGER, None, SOUTH],
    [0, 1, CHANGER, None, EAST],
    [3, 0, CHANGER, None, NORTH],
    [4, 3, CHANGER, None, WEST],
    [4, 4, GOAL, ORANGE],
    [3, 4, GOAL, RED],
    [2, 4, GOAL, DARK],
    [0, 0, SQUARE, ORANGE, EAST],
    [1, 0, SQUARE, RED, EAST],
    [2, 0, SQUARE, DARK, EAST],
]


DISCOVERED_STATE_LIMITS = {
 'level10': 150,
 'level12': 200,
 'level13': 600,
 'level14': 1200,
 'level15': 200,
 'level16': 100,
 'level17': 500,
 'level18': 500,
 'level19': 6000,
 'level31': 12000,
 'level32': 15000,
 'level33': 12000,
 'level34': 5000,
 'level35': 10000,
}
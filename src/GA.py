import random

moves = ["U", "U'", "R", "R'", "L", "L'", "D", "D'", "F", "F'", "B", "B'"]

cube_dev = {
    "U": [["U", "U", "U"], ["U", "U", "U"], ["U", "U", "U"]],
    "R": [["R", "Y", "R"], ["R", "R", "R"], ["R", "R", "Y"]],
    "L": [["Z", "L", "L"], ["L", "L", "L"], ["L", "L", "L"]],
    "D": [["D", "D", "D"], ["D", "D", "U"], ["D", "D", "D"]],
    "F": [["F", "F", "F"], ["F", "F", "F"], ["F", "F", "F"]],
    "B": [["B", "H", "B"], ["B", "B", "B"], ["B", "B", "N"]],
}


def random_sequence(length=25):
    return [random.choice(moves) for _ in range(length)]


def init_population(pop_size=2, sequence_length=25):
    return [random_sequence(sequence_length) for _ in range(pop_size)]


def fitness(cube):  # lower this is, the better - 0 means that it is solved
    misplaced_stickers = 0
    for face, stickers in cube.items():
        centre = stickers[1][1]
        for i in range(3):
            for j in range(3):
                if stickers[i][j] != centre:
                    misplaced_stickers += 1

    return misplaced_stickers


print(fitness(cube_dev))

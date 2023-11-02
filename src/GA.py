import random
import copy
import rubiks

moves = ["U", "U'", "R", "R'", "L", "L'", "D", "D'", "F", "F'", "B", "B'"]


cube_dev = {
    "U": [["U", "U", "U"], ["U", "U", "U"], ["U", "U", "U"]],
    "R": [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"]],
    "L": [["L", "L", "L"], ["L", "L", "L"], ["L", "L", "L"]],
    "D": [["D", "D", "D"], ["D", "D", "U"], ["D", "D", "D"]],
    "F": [["F", "F", "F"], ["F", "F", "F"], ["F", "F", "F"]],
    "B": [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"]],
}


def apply_moves(cube, moves_sequence):
    modified_cube = copy.deepcopy(cube)
    for move in moves_sequence:
        rubiks.make_move(modified_cube, move)
    return modified_cube


def random_sequence(length=25):
    return [random.choice(moves) for _ in range(length)]

# print(random_sequence())


def init_population(pop_size=100, sequence_length=25):
    return [random_sequence(sequence_length) for _ in range(pop_size)]


def fitness(cube, moves_sequence):  # lower this is, the better - 0 means that it is solved

    modified_cube = apply_moves(cube, moves_sequence)  # applying moves to cube first - new

    misplaced_stickers = 0
    for face, stickers in modified_cube.items():
        centre = stickers[1][1]
        for i in range(3):
            for j in range(3):
                if stickers[i][j] != centre:
                    misplaced_stickers += 1

    return misplaced_stickers


def tournament_selection(population, cube, tournament_size=3):
    # randomly select tournament_size individuals from population
    tournament_individuals = random.sample(population, tournament_size)
    print(f"tournament individuals: {tournament_individuals}")

    # evaluate fitness of each individual
    fitness_scores = []
    for sequence in tournament_individuals:
        fitness_score = fitness(cube, sequence)
        print(f"sequence: {sequence} \n score: {fitness_score} ")
        fitness_scores.append(fitness_score)

    # fitness_scores = [fitness(cube, sequence) for sequence in tournament_individuals]
    # print(f"fitness scores: {fitness_scores}")

    # get index of lowest fitness score individual
    winner_index = fitness_scores.index(min(fitness_scores))

    # return the tournament winner (lowest fitness score)
    return tournament_individuals[winner_index]


print(f"winner: {tournament_selection(init_population(), cube_dev)}")
# print(apply_moves(cube_dev,moves))
# print(fitness(cube_dev))

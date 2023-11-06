import random
import copy
import rubiks

moves = ["U", "U'", "R", "R'", "L", "L'", "D", "D'", "F", "F'", "B", "B'"]

permutations = [  # borrowed from https://github.com/rvaccarim/genetic_rubik
    # permutes two edges: U face, bottom edge and right edge
    "F' L' B' R' U' R U' B L F R U R' U".split(" "),
    # permutes two edges: U face, bottom edge and left edge
    "F R B L U L' U B' R' F' L' U' L U'".split(" "),
    # permutes two corners: U face, bottom left and bottom right
    "U U B U U B' R R F R' F' U U F' U U F R'".split(" "),
    # permutes three corners: U face, bottom left and top left
    "U U R U U R' F F L F' L' U U L' U U L F'".split(" "),
    # permutes three centers: F face, top, right, bottom
    "U' B B D D L' F F D D B B R' U'".split(" "),
    # permutes three centers: F face, top, right, left
    "U B B D D R F F D D B B L U".split(" "),
    # U face: bottom edge <-> right edge, bottom right corner <-> top right corner
    "D' R' D R R U' R B B L U' L' B B U R R".split(" "),
    # U face: bottom edge <-> right edge, bottom right corner <-> left right corner
    "D L D' L L U L' B B R' U R B B U' L L".split(" "),
    # U face: top edge <-> bottom edge, bottom left corner <-> top right corner
    "R' U L' U U R U' L R' U L' U U R U' L U'".split(" "),
    # U face: top edge <-> bottom edge, bottom right corner <-> top left corner
    "L U' R U U L' U R' L U' R U U L' U R' U".split(" "),
    # permutes three corners: U face, bottom right, bottom left and top left
    "F' U B U' F U B' U'".split(" "),
    # permutes three corners: U face, bottom left, bottom right and top right
    "F U' B' U F' U' B U".split(" "),
    # permutes three edges: F face bottom, F face top, B face top
    "L' U U L R' F F R".split(" "),
    # permutes three edges: F face top, B face top, B face bottom
    "R' U U R L' B B L".split(" "),
    # H permutation: U Face, swaps the edges horizontally and vertically
    "M2 U M2 U U M2 U M2".split(" ")
]


cube_dev = {
    "U": [["U", "U", "U"], ["U", "U", "U"], ["U", "U", "U"]],
    "R": [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"]],
    "L": [["L", "L", "L"], ["L", "L", "L"], ["L", "L", "L"]],
    "D": [["D", "D", "D"], ["D", "D", "U"], ["D", "D", "D"]],
    "F": [["F", "F", "F"], ["F", "F", "F"], ["F", "F", "F"]],
    "B": [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"]],
}


def scramble_cube(cube, _moves):
    modded_cube = copy.deepcopy(cube)
    shuffle_moves = copy.deepcopy(_moves)
    random.shuffle(shuffle_moves)
    for move in shuffle_moves:
        modded_cube = rubiks.make_move(modded_cube, move)
    return modded_cube


def apply_moves(cube, moves_sequence):
    modified_cube = copy.deepcopy(cube)
    for move in moves_sequence:
        rubiks.make_move(modified_cube, move)
    return modified_cube


# def random_sequence(length=25):
#     return [random.choice(moves) for _ in range(length)]
#
#
# def init_population(pop_size=100, sequence_length=25):
#     return [random_sequence(sequence_length) for _ in range(pop_size)]

def init_population(pop_size=100, sequence_length=25, moves=moves):
    population = [[random.choice(moves) for _ in range(sequence_length)] for _ in range(pop_size)]
    return population


def init_population_with_permutations(pop_size, sequence_length, permutations = permutations):
    population = []
    for _ in range(pop_size):
        individual = []
        while len(individual) < sequence_length:
            permutation = random.choice(permutations)
            individual.extend(permutation)
            # If the individual sequence exceeds the desired length, truncate it.
            individual = individual[:sequence_length]
        population.append(individual)
    return population


# print(f"initial population: {init_population()[0]}")


# fitness
def check_fitness(cube, moves_sequence):  # lower this is, the better - 0 means that it is solved

    modified_cube = apply_moves(cube, moves_sequence)  # applying moves to cube first - new

    misplaced_stickers = 0
    for face, stickers in modified_cube.items():
        centre = stickers[1][1]
        for i in range(3):
            for j in range(3):
                if stickers[i][j] != centre:
                    misplaced_stickers += 1

    return misplaced_stickers


# selection
def tournament_selection(population, cube, tournament_size=10):
    # randomly select tournament_size individuals from population
    tournament_individuals = random.sample(population, tournament_size)
    # print(f"tournament individuals: {tournament_individuals}")

    # evaluate fitness of each individual
    fitness_scores = []
    for sequence in tournament_individuals:
        fitness_score = check_fitness(cube, sequence)
        # print(f"sequence: {sequence} \n score: {fitness_score} ")
        fitness_scores.append(fitness_score)

    # fitness_scores = [fitness(cube, sequence) for sequence in tournament_individuals]
    # print(f"fitness scores: {fitness_scores}")

    # get index of lowest fitness score individual
    winner_index = fitness_scores.index(min(fitness_scores))

    # return the tournament winner (lowest fitness score)
    return tournament_individuals[winner_index]


# cross over
def lookahead_crossover(parent1, parent2, cube, lookahead_depth):
    child1_moves = []
    child2_moves = []
    intermediate_cube1 = copy.deepcopy(cube)
    intermediate_cube2 = copy.deepcopy(cube)

    for i in range(len(parent1)):
        # look ahead
        lookahead_moves1 = parent1[i:i + lookahead_depth]
        lookahead_moves2 = parent2[i:i + lookahead_depth]

        # apply lookahead moves to separate copies of the cube for each child
        future_cube1_for_child1 = apply_moves(copy.deepcopy(intermediate_cube1), lookahead_moves1)
        future_cube2_for_child1 = apply_moves(copy.deepcopy(intermediate_cube1), lookahead_moves2)
        future_cube1_for_child2 = apply_moves(copy.deepcopy(intermediate_cube2), lookahead_moves1)
        future_cube2_for_child2 = apply_moves(copy.deepcopy(intermediate_cube2), lookahead_moves2)

        # evaluate which future state is better for each child
        fitness1_for_child1 = check_fitness(future_cube1_for_child1, lookahead_moves1)
        fitness2_for_child1 = check_fitness(future_cube2_for_child1, lookahead_moves2)
        fitness1_for_child2 = check_fitness(future_cube1_for_child2, lookahead_moves1)
        fitness2_for_child2 = check_fitness(future_cube2_for_child2, lookahead_moves2)

        # choose best move for child1
        if fitness1_for_child1 <= fitness2_for_child1:
            chosen_move_for_child1 = parent1[i]
            alternate_move_for_child2 = parent2[i]
        else:
            chosen_move_for_child1 = parent2[i]
            alternate_move_for_child2 = parent1[i]

        # choose second-best move for child2, if fitness are equal prefer parent2
        if fitness1_for_child2 < fitness2_for_child2 or \
                (fitness1_for_child2 == fitness2_for_child2 and
                 alternate_move_for_child2 == parent2[i]):
            chosen_move_for_child2 = alternate_move_for_child2
        else:
            if alternate_move_for_child2 == parent1[i]:
                chosen_move_for_child2 = parent2[i]
            else:
                chosen_move_for_child2 = parent1[i]

        # apply chosen move to intermediate cube and add to child moves
        intermediate_cube1 = rubiks.make_move(intermediate_cube1, chosen_move_for_child1)
        child1_moves.append(chosen_move_for_child1)

        intermediate_cube2 = rubiks.make_move(intermediate_cube2, chosen_move_for_child2)
        child2_moves.append(chosen_move_for_child2)

    return child1_moves, child2_moves


# point mutation
# def mutate(sequence, mutation_rate=0.1):  # Mutate a sequence of moves with given probability (mutation_rate)"
#     new_sequence = sequence.copy()
#     for i in range(len(new_sequence)):
#         if random.random() < mutation_rate:
#             new_sequence[i] = random.choice(moves)  # replace with a random move
#     return new_sequence

# scramble mutation
# def mutate_with_scramble(sequence, mutation_rate=0.1):
#     new_sequence = sequence.copy()
#     length = len(new_sequence)
#     if random.random() < mutation_rate:
#         # determine starting and ending points of subset to scramble
#         start = random.randint(0, length - 2)
#         end = random.randint(start + 1, length - 1)
#
#         # extract subset and shuffle it
#         subset = new_sequence[start:end]
#         random.shuffle(subset)
#
#         # reinsert shuffled subset back into the sequence
#         new_sequence[start:end] = subset
#
#     return new_sequence


def mutate_with_permutation(sequence, permutations_=permutations, mutation_rate=0.1):
    new_sequence = sequence.copy()
    length = len(new_sequence)
    if random.random() < mutation_rate:
        permutation = random.choice(permutations_)  # select random permutation from list
        start = random.randint(0, length - len(permutations_))  # determine segment of individual sequence to replace
        end = start + len(permutations_)
        new_sequence[start:end] = permutations_  # replace segment with the permutation

    return new_sequence


def run_genetic_algorithm(cube, generations=100, pop_size=100, sequence_length=25):
    try:
        population = init_population_with_permutations(pop_size, sequence_length)

        for generation in range(generations):
            print(f"Generation {generation + 1}")

            new_population = []

            for seq in population:
                if check_fitness(cube, seq) == 0:
                    print(f"Solution found in generation {generation + 1}: {seq}")
                    return seq

            for _ in range(pop_size // 2):
                parent1 = tournament_selection(population, cube)
                parent2 = tournament_selection(population, cube)
                child1, child2 = lookahead_crossover(parent1, parent2, cube, lookahead_depth=2)
                new_population.append(mutate_with_permutation(child1))
                new_population.append(mutate_with_permutation(child2))

            population = new_population

        return "solution not found :("
    except Exception as e:
        print(f"An error occurred: {e}")


solution = run_genetic_algorithm(cube=scramble_cube(cube_dev, moves), generations=10)
print(solution)


# def run_genetic_algorithm(cube, generations=100, pop_size=100, sequence_length=25):
#     population = init_population(pop_size, sequence_length)
#
#     for generation in range(generations):
#         print(f"Generation {generation + 1}")
#
#         new_population = []
#
#         # check if any sequence solves the cube in the current population
#         for seq in population:
#             if check_fitness(cube, seq) == 0:
#                 print(f"Solution found in generation {generation + 1}: {seq}")
#                 return seq
#
#
#             # selection, crossover, mutation to create new population
#             for _ in range(pop_size // 2):
#                 parent1 = tournament_selection(population, cube)
#                 parent2 = tournament_selection(population, cube)
#                 child1, child2 = lookahead_crossover(parent1=parent1, parent2=parent2,
#                                                      cube=cube, lookahead_depth=2)
#                 new_population.append(mutate(child1))
#                 new_population.append(mutate(child2))
#
#             population = new_population



# print(scramble_cube(cube_dev, moves))

# parent01 = init_population(pop_size=1)[0]
# parent02 = init_population(pop_size=1)[0]
#
# print(f"parent1: {parent01}")
# print(f"parent2: {parent02}")
# #
# result = lookahead_crossover(parent01, parent02, scramble_cube(cube_dev, moves), 2)
# #
# print(f"xover: {result}")
# #
# test1, test2 = result
# print(test1 == test2)






# def state_aware_crossover(parent1, parent2, cube, crossover_point):
#     # apply first part of parent1 moves
#     child_moves = parent1[:crossover_point]
#     intermediate_cube = apply_moves(cube, child_moves)
#
#     # evaluate effectiveness of each subsequent move in parent1 and parent2
#     for i in range(crossover_point, len(parent1)):
#         move1 = parent1[i]
#         move2 = parent2[i]
#
#         # simulate moves
#         # cube_after_move1 = rubiks.make_move(copy.deepcopy(intermediate_cube), move1)
#         # cube_after_move2 = rubiks.make_move(copy.deepcopy(intermediate_cube), move2)
#
#         cube_after_move1 = copy.deepcopy(intermediate_cube)
#         cube_after_move2 = copy.deepcopy(intermediate_cube)
#
#         # choose move resulting in cube state closer to being solved
#         if check_fitness(cube_after_move1, move1) < check_fitness(cube_after_move2, move2):
#             child_moves.append(move1)
#             intermediate_cube = cube_after_move1
#         else:
#             child_moves.append(move2)
#             intermediate_cube = cube_after_move2
#
#     return child_moves




# swap mutation

# def mutate_with_swap(sequence, mutation_rate=0.1):
#     """Mutate a sequence of moves with given probability (mutation_rate) by swapping two moves."""
#     new_sequence = sequence.copy()
#     length = len(new_sequence)
#
#     for _ in range(int(length * mutation_rate)):
#         if random.random() < mutation_rate:
#             # Pick two indices to swap that are not the same
#             idx1, idx2 = random.sample(range(length), 2)
#             # Swap the moves at these indices
#             new_sequence[idx1], new_sequence[idx2] = new_sequence[idx2], new_sequence[idx1]
#
#     return new_sequence
#
#



# parent01 = init_population(pop_size=1)
# parent02 = init_population(pop_size=1)
#
# print(f"parent1: {parent01}")
# print(f"parent2: {parent02}")
#
# result = lookahead_crossover(parent01, parent02, scramble_cube(cube_dev, moves), 2)
#
# print(result)
#
# test1, test2 = result
# print(test1 == test2)


# scramble the cube with the shuffled moves
# scrambled_cube = scramble_cube(cube_dev, moves)
# print(f"new cube is: {scrambled_cube}")

# print(f"winner: {tournament_selection(init_population(), cube_dev)}")
# print(apply_moves(cube_dev,moves))
# print(fitness(cube_dev))

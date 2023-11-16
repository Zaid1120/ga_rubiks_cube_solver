from random import randint, shuffle, choice, sample
import copy
from rubiks import make_move

# borrowed from https://github.com/rvaccarim/genetic_rubik
single_moves = ["U", "U'", "U2", "D", "D'", "D2",
                "R", "R'", "R2", "L", "L'", "L2",
                "F", "F'", "F2", "B", "B'", "B2"]

full_rotations, orientation = ["x", "x'", "x2", "y", "y'", "y2"], ["z", "z'", "z2"]

permutations = [
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


def apply_moves(cube, moves_sequence):
    for move in moves_sequence:
        make_move(cube, move)
    return cube


def random_single_move(cube):
    move = single_moves[randint(0, len(single_moves) - 1)]
    print(f"move: {move}")
    cube = apply_moves(cube, move)
    return cube

# print(random_single_move(cube))


def random_permutation(cube):
    cube = apply_moves(cube, permutations[randint(0, len(permutations) - 1)])
    return cube


def random_full_rotation(cube):
    cube = apply_moves(cube, full_rotations[randint(0, len(full_rotations) - 1)])
    return cube


def random_orientation(cube):
    cube = apply_moves(cube, orientation[randint(0, len(orientation) - 1)])
    return cube


def scramble_cube(cube):
    moves_list = ["B", "B'", "B2", "D", "D'", "D2", "E", "E'", "E2", "F", "F'", "F2", "L", "L'", "L2", "M", "M'",
                  "M2", "R", "R'", 'S', "S'", "S2", "U", "U'", "U2", "b", "b'", "b2", "d", "d'", "d2", "f", "f'",
                  "f2", "l", "l'", "l2", "r", "r'", "r2", "u", "u'", "x", "x'", "y", "y'", "z", "z'"]
    shuffle(moves_list)
    for move in moves_list:
        make_move(cube, move)
    return cube

# print(scramble_cube(cube_dev))

# fitness
def check_fitness(cube):  # lower this is, the better - 0 means that it is solved
    misplaced_stickers = 0
    for face, stickers in cube.items():
        centre = stickers[1][1]
        for i in range(3):
            for j in range(3):
                if stickers[i][j] != centre:
                    misplaced_stickers += 1

    return misplaced_stickers

# print(check_fitness(cube_dev))











def run_genetic_algorithm(generations=150, pop_size=2000, elitism_count=50, resets=30):

    best_cube = None

    cube = {
        "U": [["U", "U", "U"], ["U", "U", "U"], ["U", "U", "U"]],
        "R": [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"]],
        "L": [["L", "L", "L"], ["L", "L", "L"], ["L", "L", "L"]],
        "D": [["D", "D", "D"], ["D", "D", "D"], ["D", "D", "D"]],
        "F": [["F", "F", "F"], ["F", "F", "F"], ["F", "F", "F"]],
        "B": [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"]],
    }

    for i in range(resets):
        cubes = []

        # Add the best cube from the previous reset if it exists
        if best_cube is not None:
            cubes.append(copy.deepcopy(best_cube))

        # Fill the rest with the population
        while len(cubes) < pop_size:
            subject_cube = copy.deepcopy(cube)
            scramble_cube(subject_cube)
            cubes.append(subject_cube)

        for generation in range(generations):
            print(f"\nGeneration {generation + 1}")
            # calculate fitness scores for each cube
            cube_fitness_pairs = [(cube, check_fitness(cube)) for cube in cubes]
            # sort cubes based on fitness scores in ascending order
            cube_fitness_pairs.sort(key=lambda x: x[1])
            # print(f"pair: {cube_fitness_pairs}")

            # Extract the best fitness score
            current_best_fitness = cube_fitness_pairs[0][1]
            print(f"Best fitness score in generation {generation + 1} reset {i+1}: {current_best_fitness}")

            # if current_best_fitness < best_fitness:
            #     best_fitness = current_best_fitness
            #     stagnation_counter = 0  # Reset stagnation counter
            # else:
            #     stagnation_counter += 1

            # extract sorted cubes
            cubes = [pair[0] for pair in cube_fitness_pairs]
            # print(cubes)

            # just checking
            scores = [pair[1] for pair in cube_fitness_pairs] # delete
            # print(scores)

            for c in range(len(cubes)):

                if check_fitness(cubes[c]) == 0:
                    print(f"Solution found in generation {generation + 1}: {c[0]}")
                    return None

                if c > elitism_count:

                    cubes[c] = copy.deepcopy(cubes[randint(0, elitism_count)])

                    evolution_type = randint(0, 5)

                    if evolution_type == 0:
                        random_permutation(cubes[c])

                    elif evolution_type == 1:
                        random_permutation(cubes[c])
                        random_permutation(cubes[c])

                    elif evolution_type == 2:
                        random_full_rotation(cubes[c])
                        random_permutation(cubes[c])

                    elif evolution_type == 3:
                        random_orientation(cubes[c])
                        random_permutation(cubes[c])

                    elif evolution_type == 4:
                        random_full_rotation(cubes[c])
                        random_orientation(cubes[c])
                        random_permutation(cubes[c])

                    elif evolution_type == 5:
                        random_orientation(cubes[c])
                        random_full_rotation(cubes[c])
                        random_permutation(cubes[c])

                    # additional cases for further randomisation
                    # elif evolution_type == 6:
                    #     random_full_rotation(cubes[c])
                    #     random_orientation(cubes[c])
                    #
                    # elif evolution_type == 7:
                    #     random_orientation(cubes[c])
                    #     random_full_rotation(cubes[c])
                    #
                    # elif evolution_type == 8:
                    #     random_permutation(cubes[c])
                    #     random_full_rotation(cubes[c])
                    #
                    # elif evolution_type == 9:
                    #     random_permutation(cubes[c])
                    #     random_orientation(cubes[c])
                    #
                    # elif evolution_type == 10:
                    #     random_full_rotation(cubes[c])
                    #     random_full_rotation(cubes[c])
                    #
                    # elif evolution_type == 11:
                    #     random_orientation(cubes[c])
                    #     random_orientation(cubes[c])
                    #
                    # elif evolution_type == 12:
                    #     random_orientation(cubes[c])
                    #     random_full_rotation(cubes[c])
                    #     random_full_rotation(cubes[c])

                # Update best cube if a better one is found
                if best_cube is None or check_fitness(cubes[c]) < check_fitness(best_cube):
                    best_cube = copy.deepcopy(cubes[c])

    print("")
    print(f"Solution not found")


print(run_genetic_algorithm())

















    # # stagnation_counter = 0  # counter to track stagnation
    # print(f" initial population: {population}")
    #
    # for generation in range(generations):
    #     print(f"\nGeneration {generation + 1}")
    #
    #     # evaulate fitness of each individual in the population
    #     fitness_scores = [(sequence, check_fitness(cube, sequence)) for sequence in population]
    #
    #     # sort population by fitness scores in ascending order (lower is better)
    #     sorted_population = sorted(fitness_scores, key=lambda x: x[1])
    #
    #     print(f" sorted pop: {sorted_population}")
    #
    #     # get the best fitness score in this generation
    #     best_fitness_score = sorted_population[0][1]
    #     print(f"Best fitness score in generation {generation + 1}: {best_fitness_score}")
    #
    #     # check if any sequence solves the cube
    #     if best_fitness_score == 0:
    #         solution_sequence = sorted_population[0][0]
    #         print(f"Solution found in generation {generation + 1}: {solution_sequence}")
    #         return solution_sequence
    #
    #     # if best_fitness_score <= sorted_population[0][1]:
    #     #     stagnation_counter += 1
    #     # else:
    #     #     best_fitness_score = sorted_population[0][1]
    #     #     stagnation_counter = 0
    #
    #     # if stagnation_counter >= 5:
    #     #     # Stagnation detected, apply strategies to reintroduce diversity
    #     #     mutation_rate *= 2
    #     #     last_few = sequence_length-2
    #     #     init_population(pop_size-2, sequence_length)
    #     #
    #     #     stagnation_counter = 0  # Reset the stagnation counter
    #
    #     # carry over the best elitism_count individuals to the new population - PROBLEM HERE?
    #     new_population = [sequence for sequence, fitness in sorted_population[:elitism_count]]
    #
    #     # tournament selection, crossover, and mutation
    #     while len(new_population) < pop_size:
    #         parent1 = tournament_selection(population, cube, tournament_size)
    #         parent2 = tournament_selection(population, cube, tournament_size)
    #
    #         # perform crossover
    #         offspring1, offspring2 = two_point_crossover(parent1, parent2)
    #         # apply scramble mutation based on mutation_rate
    #         if random.random() < mutation_rate:
    #             print("offspring 1 got mutated")
    #             offspring1 = scramble_mutation(offspring1)
    #         if random.random() < mutation_rate:
    #             print("offspring 2 got mutated")
    #             offspring2 = scramble_mutation(offspring2)
    #
    #         # add offspring to the new population
    #         new_population.append(offspring1)
    #         new_population.append(offspring2)
    #
    #     print(f"\nold population: {population}")
    #     print(f"new population: {new_population} \n")
    #
    #     print(f"old population last element: {population[-1]}")
    #     print(f"new population last element: {new_population[-1]} \n")
    #
    #     print(f"old population length: {len(population)}")
    #     print(f"new population length: {len(new_population)} \n \n")
    #     population = new_population  # update population
    #
    # print("No solution found within the given generations.")
    # return None



# cube_use = scramble_cube(cube_dev)
# # print(f"initial cube: {cube_use}")
# print(run_genetic_algorithm())
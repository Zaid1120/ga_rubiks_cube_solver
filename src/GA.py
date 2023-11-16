import random
import copy
from rubiks import make_move

cube_dev = {
    "U": [["U", "U", "U"], ["U", "U", "U"], ["U", "U", "U"]],
    "R": [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"]],
    "L": [["L", "L", "L"], ["L", "L", "L"], ["L", "L", "L"]],
    "D": [["D", "D", "D"], ["D", "D", "D"], ["D", "D", "D"]],
    "F": [["F", "F", "F"], ["F", "F", "F"], ["F", "F", "F"]],
    "B": [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"]],
}


def scramble_cube(cube):
    moves_list = ["B", "B'", "B2", "D", "D'", "D2", "E", "E'", "E2", "F", "F'", "F2", "L", "L'", "L2", "M", "M'",
                  "M2", "R", "R'", 'S', "S'", "S2", "U", "U'", "U2", "b", "b'", "b2", "d", "d'", "d2", "f", "f'",
                  "f2", "l", "l'", "l2", "r", "r'", "r2", "u", "u'", "x", "x'", "y", "y'", "z", "z'"]
    modded_cube = copy.deepcopy(cube)
    shuffle_moves = copy.deepcopy(moves_list)
    random.shuffle(shuffle_moves)
    for move in shuffle_moves:
        modded_cube = make_move(modded_cube, move)
    return modded_cube


# print(scramble_cube(cube_dev))

def apply_moves(cube, moves_sequence):
    modified_cube = copy.deepcopy(cube)
    for move in moves_sequence:
        make_move(modified_cube, move)
    return modified_cube


# population
def init_population(pop_size=2, sequence_length=25):
    moves_list = ["B", "B'", "B2", "D", "D'", "D2", "E", "E'", "E2", "F", "F'", "F2", "L", "L'", "L2", "M", "M'",
                  "M2", "R", "R'", 'S', "S'", "S2", "U", "U'", "U2", "b", "b'", "b2", "d", "d'", "d2", "f", "f'",
                  "f2", "l", "l'", "l2", "r", "r'", "r2", "u", "u'", "x", "x'", "y", "y'", "z", "z'"]
    population = [[random.choice(moves_list) for _ in range(sequence_length)] for _ in range(pop_size)]
    return population


# print(len(init_population()))


# fitness
def check_fitness(cube, moves_sequence):  # lower this is, the better - 0 means that it is solved
    modified_cube = apply_moves(cube, moves_sequence)  # applying moves to cube first
    misplaced_stickers = 0
    for face, stickers in modified_cube.items():
        centre = stickers[1][1]
        for i in range(3):
            for j in range(3):
                if stickers[i][j] != centre:
                    misplaced_stickers += 1

    return misplaced_stickers

# print(check_fitness(cube_dev, []))


# selection
def tournament_selection(population, cube, tournament_size=2):

    # randomly select tournament_size individuals from population
    tournament_individuals = random.sample(population, tournament_size)

    # evaluate fitness of each individual
    fitness_scores = []
    for sequence in tournament_individuals:
        fitness_score = check_fitness(cube, sequence)
        # print(f"sequence: {sequence} \n score: {fitness_score} ")
        fitness_scores.append(fitness_score)

    # list comprehension version of above for-loop
    # fitness_scores = [check_fitness(cube, sequence) for sequence in tournament_individuals]
    # print(f"fitness scores: {fitness_scores}")

    winner_index = fitness_scores.index(min(fitness_scores))  # get index of lowest fitness score individual
    return tournament_individuals[winner_index]  # return the tournament winner (lowest fitness score)


# print(f"winner: {tournament_selection(population=init_population(), cube=cube_dev)}")

# crossover
def two_point_crossover(parent1, parent2):

    # ensure parents are of the same length
    if len(parent1) != len(parent2):
        raise ValueError("Parents must be of the same length for crossover")

    length = len(parent1)

    # choose two crossover points
    crossover_point1 = random.randint(1, length - 2)  # leave space for crossover point 2
    # print(f"crossover point 1: {crossover_point1}")
    crossover_point2 = random.randint(crossover_point1+1, length - 1)  # to not go beyond length
    # print(f"crossover point 2: {crossover_point2}")

    # create offspring by combining the segments
    offspring1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
    offspring2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[crossover_point2:]

    return offspring1, offspring2

# print(two_point_crossover(['D2', "d'", "f'", 'b2', 'E2', "D4", "P1"], ["b'", 'R', "B'", 'E', 'F2', "H1", "H4"]))


def scramble_mutation(sequence):
    if len(sequence) < 2:
        # no mutation is possible if the sequence is too short
        return sequence

    # choose two indices at random for the start and end of the segment to scramble
    start_index = random.randint(0, len(sequence) - 2)
    end_index = random.randint(start_index + 1, len(sequence) - 1)
    # print(f"start index: {start_index}")
    # print(f"end index: {end_index}")

    # extract the segment and shuffle (scramble) it
    segment_to_scramble = sequence[start_index:end_index]
    # print(f"segment to scramble: {segment_to_scramble}")
    random.shuffle(segment_to_scramble)

    # reconstruct the sequence with the scrambled segment
    mutated_sequence = sequence[:start_index] + segment_to_scramble + sequence[end_index:]

    return mutated_sequence


# print(scramble_mutation(['D2', "d'", "f'", 'b2', 'E2', "D4", "P1", 'v2', "h'", "r'" ]))


def run_genetic_algorithm(cube, generations=2000, pop_size=100, sequence_length=20, elitism_count=2, tournament_size=10, mutation_rate=0.1):
    population = init_population(pop_size, sequence_length)

    for generation in range(generations):
        print(f"Generation {generation + 1}")

        # evaluate fitness of each individual in the population
        fitness_scores = [(sequence, check_fitness(cube, sequence)) for sequence in population]

        # sort population by fitness scores in ascending order (lower is better)
        sorted_population = sorted(fitness_scores, key=lambda x: x[1])

        # get the best fitness score in this generation
        best_fitness_score = sorted_population[0][1]
        print(f"Best fitness score in generation {generation + 1}: {best_fitness_score}")

        # check if any sequence solves the cube
        if best_fitness_score == 0:
            solution_sequence = sorted_population[0][0]
            print(f"Solution found in generation {generation + 1}: {solution_sequence}")
            return solution_sequence

        # carry over the best 'elitism_count' individuals to the new population
        new_population = [sequence for sequence, fitness in sorted_population[:elitism_count]]

        # tournament selection, crossover, and mutation
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, cube, tournament_size)
            parent2 = tournament_selection(population, cube, tournament_size)

            # perform crossover
            offspring1, offspring2 = two_point_crossover(parent1, parent2)

            # apply scramble mutation based on mutation_rate
            if random.random() < mutation_rate:
                offspring1 = scramble_mutation(offspring1)
            if random.random() < mutation_rate:
                offspring2 = scramble_mutation(offspring2)

            # add offspring to the new population not to exceed pop_size
            if len(new_population) < pop_size:
                new_population.append(offspring1)
            if len(new_population) < pop_size:
                new_population.append(offspring2)

        population = new_population

    print("No solution found within the given generations.")
    return None



# def run_genetic_algorithm(cube, generations=20, pop_size=100, sequence_length=21, elitism_count=2, tournament_size=10, mutation_rate=0.1):
# def run_genetic_algorithm(cube, generations=200, pop_size=1000, sequence_length=25, elitism_count=7, tournament_size=10, mutation_rate=0.1):
#     population = init_population(pop_size, sequence_length)
#     # stagnation_counter = 0  # counter to track stagnation
#     # print(f" initial population: {population}")
#
#     for generation in range(generations):
#         print(f"\nGeneration {generation + 1}")
#
#         # evaulate fitness of each individual in the population
#         fitness_scores = [(sequence, check_fitness(cube, sequence)) for sequence in population]
#
#         # sort population by fitness scores in ascending order (lower is better)
#         sorted_population = sorted(fitness_scores, key=lambda x: x[1])
#
#         # print(f" sorted pop: {sorted_population}")
#
#         # get the best fitness score in this generation
#         best_fitness_score = sorted_population[0][1]
#         # print(f"Best fitness score in generation {generation + 1}: {best_fitness_score}")
#
#         # check if any sequence solves the cube
#         if best_fitness_score == 0:
#             solution_sequence = sorted_population[0][0]
#             print(f"Solution found in generation {generation + 1}: {solution_sequence}")
#             return solution_sequence
#
#         # if best_fitness_score <= sorted_population[0][1]:
#         #     stagnation_counter += 1
#         # else:
#         #     best_fitness_score = sorted_population[0][1]
#         #     stagnation_counter = 0
#
#         # if stagnation_counter >= 5:
#         #     # Stagnation detected, apply strategies to reintroduce diversity
#         #     mutation_rate *= 2
#         #     last_few = sequence_length-2
#         #     init_population(pop_size-2, sequence_length)
#         #
#         #     stagnation_counter = 0  # Reset the stagnation counter
#
#         # carry over the best elitism_count individuals to the new population - PROBLEM HERE?
#         new_population = [sequence for sequence, fitness in sorted_population[:elitism_count]]
#
#         # tournament selection, crossover, and mutation
#         while len(new_population) < pop_size:
#             parent1 = tournament_selection(population, cube, tournament_size)
#             parent2 = tournament_selection(population, cube, tournament_size)
#
#             # perform crossover
#             offspring1, offspring2 = two_point_crossover(parent1, parent2)
#             # apply scramble mutation based on mutation_rate
#             if random.random() < mutation_rate:
#                 # print("offspring 1 got mutated")
#                 offspring1 = scramble_mutation(offspring1)
#             if random.random() < mutation_rate:
#                 # print("offspring 2 got mutated")
#                 offspring2 = scramble_mutation(offspring2)
#
#             # add offspring to the new population
#             new_population.append(offspring1)
#             new_population.append(offspring2)
#
#         # print(f"\nold population: {population}")
#         # print(f"new population: {new_population} \n")
#         #
#         # print(f"old population last element: {population[-1]}")
#         # print(f"new population last element: {new_population[-1]} \n")
#         #
#         # print(f"old population length: {len(population)}")
#         # print(f"new population length: {len(new_population)} \n \n")
#         population = new_population  # update population
#
#     print("No solution found within the given generations.")
#     return None



cube_use = scramble_cube(cube_dev)
# print(f"initial cube: {cube_use}")
run_genetic_algorithm(cube=cube_use)

# # scramble mutation
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

# def run_genetic_algorithm(cube, generations=1, pop_size=10, sequence_length=5):
#     population = init_population(pop_size, sequence_length)
#
#     # print(f"this is the population: {population}")
#
#     for generation in range(generations):
#         print(f"Generation {generation + 1}")
#         new_population = []
#
#         # check if any sequence solves the cube in the current population
#         for sequence in population:
#
#             if check_fitness(cube, sequence) == 0:
#                 print(f"Solution found in generation {generation + 1}: {sequence}")
#                 return sequence

# parent1 = tournament_selection(population, cube)
# print(parent1)
            # parent2 = tournament_selection(population, cube)

    #         # selection, crossover, mutation to create new population
    #         for _ in range(pop_size // 2):
                # print(_)
    #             parent1 = tournament_selection(population, cube)
    #             parent2 = tournament_selection(population, cube)
    #             child1, child2 = lookahead_crossover(parent1=parent1, parent2=parent2,
    #                                                  cube=cube, lookahead_depth=2)
    #             new_population.append(mutate_with_scramble(child1))
    #             new_population.append(mutate_with_scramble(child2))
    #
    #         population = new_population


# scrambled_cube = scramble_cube(cube_dev)
# solution = run_genetic_algorithm(cube=cube_dev)
# print(solution)
# print(is_solved(cube_dev))








# # cross over
# def lookahead_crossover(parent1, parent2, cube, lookahead_depth):
#     child1_moves = []
#     child2_moves = []
#     intermediate_cube1 = copy.deepcopy(cube)
#     intermediate_cube2 = copy.deepcopy(cube)
#
#     for i in range(len(parent1)):
#         # look ahead
#         lookahead_moves1 = parent1[i:i + lookahead_depth]
#         lookahead_moves2 = parent2[i:i + lookahead_depth]
#
#         # apply lookahead moves to separate copies of the cube for each child
#         future_cube1_for_child1 = apply_moves(copy.deepcopy(intermediate_cube1), lookahead_moves1)
#         future_cube2_for_child1 = apply_moves(copy.deepcopy(intermediate_cube1), lookahead_moves2)
#         future_cube1_for_child2 = apply_moves(copy.deepcopy(intermediate_cube2), lookahead_moves1)
#         future_cube2_for_child2 = apply_moves(copy.deepcopy(intermediate_cube2), lookahead_moves2)
#
#         # evaluate which future state is better for each child
#         fitness1_for_child1 = check_fitness(future_cube1_for_child1, lookahead_moves1)
#         fitness2_for_child1 = check_fitness(future_cube2_for_child1, lookahead_moves2)
#         fitness1_for_child2 = check_fitness(future_cube1_for_child2, lookahead_moves1)
#         fitness2_for_child2 = check_fitness(future_cube2_for_child2, lookahead_moves2)
#
#         # choose best move for child1
#         if fitness1_for_child1 <= fitness2_for_child1:
#             chosen_move_for_child1 = parent1[i]
#             alternate_move_for_child2 = parent2[i]
#         else:
#             chosen_move_for_child1 = parent2[i]
#             alternate_move_for_child2 = parent1[i]
#
#         # choose second-best move for child2, if fitness are equal prefer parent2
#         if fitness1_for_child2 < fitness2_for_child2 or \
#                 (fitness1_for_child2 == fitness2_for_child2 and
#                  alternate_move_for_child2 == parent2[i]):
#             chosen_move_for_child2 = alternate_move_for_child2
#         else:
#             if alternate_move_for_child2 == parent1[i]:
#                 chosen_move_for_child2 = parent2[i]
#             else:
#                 chosen_move_for_child2 = parent1[i]
#
#         # apply chosen move to intermediate cube and add to child moves
#         intermediate_cube1 = rubiks.make_move(intermediate_cube1, chosen_move_for_child1)
#         child1_moves.append(chosen_move_for_child1)
#
#         intermediate_cube2 = rubiks.make_move(intermediate_cube2, chosen_move_for_child2)
#         child2_moves.append(chosen_move_for_child2)
#
#     return child1_moves, child2_moves
#
#
# # scramble mutation
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
#































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
#                 new_population.append(mutate_with_scramble(child1))
#                 new_population.append(mutate_with_scramble(child2))
#
#             population = new_population
#
#
#
#
# solution = run_genetic_algorithm(cube=scramble_cube(cube_dev), generations=100)
# print(solution)

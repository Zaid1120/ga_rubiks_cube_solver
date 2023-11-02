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


def random_sequence(length=25):
    return [random.choice(moves) for _ in range(length)]

# print(random_sequence())


def init_population(pop_size=100, sequence_length=25):
    return [random_sequence(sequence_length) for _ in range(pop_size)]


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
def tournament_selection(population, cube, tournament_size=3):
    # randomly select tournament_size individuals from population
    tournament_individuals = random.sample(population, tournament_size)
    print(f"tournament individuals: {tournament_individuals}")

    # evaluate fitness of each individual
    fitness_scores = []
    for sequence in tournament_individuals:
        fitness_score = check_fitness(cube, sequence)
        print(f"sequence: {sequence} \n score: {fitness_score} ")
        fitness_scores.append(fitness_score)

    # fitness_scores = [fitness(cube, sequence) for sequence in tournament_individuals]
    # print(f"fitness scores: {fitness_scores}")

    # get index of lowest fitness score individual
    winner_index = fitness_scores.index(min(fitness_scores))

    # return the tournament winner (lowest fitness score)
    return tournament_individuals[winner_index]


# cross over
def lookahead_crossover(parent1, parent2, cube, lookahead_depth):
    child_moves = []
    intermediate_cube = copy.deepcopy(cube)

    # ensure moves are same length
    assert len(parent1) == len(parent2)

    for i in range(len(parent1)):
        # look ahead
        lookahead_moves1 = parent1[i:i + lookahead_depth]
        lookahead_moves2 = parent2[i:i + lookahead_depth]

        # apply lookahead moves to separate copies of the cube
        # future_cube1 = apply_moves(copy.deepcopy(intermediate_cube), lookahead_moves1)
        # future_cube2 = apply_moves(copy.deepcopy(intermediate_cube), lookahead_moves2)

        future_cube1 = copy.deepcopy(intermediate_cube)
        future_cube2 = copy.deepcopy(intermediate_cube)

        # evaluate which future state is better
        if check_fitness(future_cube1, lookahead_moves1) < check_fitness(future_cube2, lookahead_moves2):
            chosen_move = parent1[i]
        else:
            chosen_move = parent2[i]

        # apply chosen move to intermediate cube and add to child moves
        intermediate_cube = rubiks.make_move(intermediate_cube, chosen_move)
        child_moves.append(chosen_move)

    return child_moves


def state_aware_crossover(parent1, parent2, cube, crossover_point):
    # apply first part of parent1 moves
    child_moves = parent1[:crossover_point]
    intermediate_cube = apply_moves(cube, child_moves)

    # evaluate effectiveness of each subsequent move in parent1 and parent2
    for i in range(crossover_point, len(parent1)):
        move1 = parent1[i]
        move2 = parent2[i]

        # simulate moves
        # cube_after_move1 = rubiks.make_move(copy.deepcopy(intermediate_cube), move1)
        # cube_after_move2 = rubiks.make_move(copy.deepcopy(intermediate_cube), move2)

        cube_after_move1 = copy.deepcopy(intermediate_cube)
        cube_after_move2 = copy.deepcopy(intermediate_cube)

        # choose move resulting in cube state closer to being solved
        if check_fitness(cube_after_move1, move1) < check_fitness(cube_after_move2, move2):
            child_moves.append(move1)
            intermediate_cube = cube_after_move1
        else:
            child_moves.append(move2)
            intermediate_cube = cube_after_move2

    return child_moves


# point mutation
def mutate(sequence, mutation_rate=0.1):  # Mutate a sequence of moves with given probability (mutation_rate)"
    new_sequence = sequence.copy()
    for i in range(len(new_sequence)):
        if random.random() < mutation_rate:
            new_sequence[i] = random.choice(moves)  # replace with a random move
    return new_sequence


# swap mutation

def mutate_with_swap(sequence, mutation_rate=0.1):
    """Mutate a sequence of moves with given probability (mutation_rate) by swapping two moves."""
    new_sequence = sequence.copy()
    length = len(new_sequence)

    for _ in range(int(length * mutation_rate)):
        if random.random() < mutation_rate:
            # Pick two indices to swap that are not the same
            idx1, idx2 = random.sample(range(length), 2)
            # Swap the moves at these indices
            new_sequence[idx1], new_sequence[idx2] = new_sequence[idx2], new_sequence[idx1]

    return new_sequence


# scramble mutation
def mutate_with_scramble(sequence, mutation_rate=0.1):
    """Mutate a given sequence of moves by scrambling a subset with a given probability (mutation_rate)."""
    new_sequence = sequence.copy()
    length = len(new_sequence)
    if random.random() < mutation_rate:
        # Determine the starting and ending points of the subset to scramble
        start = random.randint(0, length - 2)
        end = random.randint(start + 1, length - 1)

        # Extract the subset and shuffle it
        subset = new_sequence[start:end]
        random.shuffle(subset)

        # Reinsert the shuffled subset back into the sequence
        new_sequence[start:end] = subset

    return new_sequence


# scramble the cube with the shuffled moves
scrambled_cube = scramble_cube(cube_dev, moves)
print(f"new cube is: {scrambled_cube}")

# print(f"winner: {tournament_selection(init_population(), cube_dev)}")
# print(apply_moves(cube_dev,moves))
# print(fitness(cube_dev))

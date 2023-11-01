import src.rubiks as rubiks
import random

moves = ["U", "U'", "R", "R'", "L", "L'", "D", "D'", "F", "F'", "B", "B'"]


def random_sequence(length=25):
    return [random.choice(moves) for _ in range(length)]


def init_population(pop_size=100, sequence_length=25):
    return [random_sequence(sequence_length) for _ in range(pop_size)]

print(init_population())

# def __calculate_fitness():
#     misplaced_stickers = 0
#
#     for k, face in self.faces.items():
#         # centers are fixed in a Rubik cube
#         center = face[1, 1]
#
#         for i in range(0, 3):
#             for j in range(0, 3):
#                 if face[i, j] != center:
#                     misplaced_stickers += 1
#
#     return misplaced_stickers



def fitness(cube, sequence):
    temp_cube = cube.copy()
    for move in sequence:
        rubiks.make_move(temp_cube, move)
    return rubiks.is_solved(temp_cube)


def tournament_selection(population, cube, k=5):
    selected = random.sample(population, k)
    results = [fitness(cube, s) for s in selected]

    if True in results:
        # If any sequence solves the cube, return it
        return selected[results.index(True)]
    else:
        # Otherwise, return a randomly selected sequence for now
        # (you can implement a better metric for selection later if needed)
        return random.choice(selected)


def crossover(seq1, seq2):
    point = random.randint(1, len(seq1) - 1)
    return seq1[:point] + seq2[point:], seq2[:point] + seq1[point:]


def mutate(seq, mutation_rate=0.5):
    for i in range(len(seq)):
        if random.random() < mutation_rate:
            seq[i] = random.choice(moves)
    return seq


def run_genetic_algorithm(cube, generations=1000, pop_size=100, sequence_length=25):
    population = init_population(pop_size, sequence_length)

    for generation in range(generations):
        print(f"Generation {generation + 1}")

        # Check if any sequence solves the cube in the current population
        for seq in population:
            if fitness(cube, seq):
                print(f"Solution found in generation {generation + 1}: {seq}")
                return seq

        new_population = []

        # Selection, Crossover, and Mutation to create a new population
        for _ in range(pop_size // 2):
            parent1 = tournament_selection(population, cube)
            parent2 = tournament_selection(population, cube)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))

        population = new_population

    print("Solution not found!")
    return None


solution = run_genetic_algorithm(rubiks.cube)












#
#
# def crossover(seq1, seq2):
#     # Implement one-point or two-point crossover
#     pass
#
#
# def mutate(seq):
#     # Randomly change some moves in the sequence
#     pass


# check = False
# while not check:
#     check = fitness(rubiks.cube, random_sequence())
#
# print("nice")


# print(fitness(rubiks.cube, random_sequence()))

# def random_sequence(length=20):
#     return [random.choice(MOVES) for _ in range(length)]
#
# def fitness(cube, sequence):
#     temp_cube = cube.copy()
#     for move in sequence:
#         apply_move(temp_cube, move)
#     return sum([is_solved(temp_cube)])
#
# def crossover(seq1, seq2):
#     # Implement one-point or two-point crossover
#     pass
#
# def mutate(seq):
#     # Randomly change some moves in the sequence
#     pass

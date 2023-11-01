combinations = [("F'", "F"), ("B'", "B"), ("U'", "U"), ("D'", "D"), ("R'", "R"), ("L'", "L")]
for move1, move2 in combinations:
    print(move1, move2)





# import rubiks
# import copy
#
#
# def test_initialisation():
#     assert rubiks.is_solved(rubiks.cube), "cube should start in a solved state"
#     print("test_initialisation passed")
#
#
# def test_single_rotation():
#     test_cube = copy.deepcopy(rubiks.cube)
#     test_cube = rubiks.make_move(test_cube, "F")
#     assert not rubiks.is_solved(test_cube), "cube should not be solved after a single F move"
#     print("test_single_rotation passed")
#
#
# def test_multiple_rotations():
#     test_cube = copy.deepcopy(rubiks.cube)
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "F")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating F 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "F'")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating F' 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "B")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating B 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "B'")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating B' 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "L")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating L 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "L'")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating L' 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "R")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating R 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "R")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating R' 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "U")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating U 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "U'")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating U' 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "D")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating D 4 times."
#
#     for _ in range(4):
#         test_cube = rubiks.make_move(test_cube, "D")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating D' 4 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "F'")
#     assert not rubiks.is_solved(test_cube), "Cube should not be solved after rotating F' 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "F")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating F 3 times followed by F 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "B'")
#     assert not rubiks.is_solved(test_cube), "Cube should not be solved after rotating B' 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "B")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating B' 3 times followed by B 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "U'")
#     assert not rubiks.is_solved(test_cube), "Cube should not be solved after rotating U' 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "U")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating U' 3 times followed by U 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "D'")
#     assert not rubiks.is_solved(test_cube), "Cube should not be solved after rotating D' 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "D")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating D' 3 times followed by D 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "R'")
#     assert not rubiks.is_solved(test_cube), "Cube should not be solved after rotating R' 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "R")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating R' 3 times followed by R 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "L'")
#     assert not rubiks.is_solved(test_cube), "Cube should not be solved after rotating L' 3 times."
#
#     for _ in range(3):
#         test_cube = rubiks.make_move(test_cube, "L")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after rotating L' 3 times followed by L 3 times."
#
#     print("test_multiple_rotations passed")
#
#
# def test_solution_check():
#     test_cube = copy.deepcopy(rubiks.cube)
#     assert rubiks.is_solved(test_cube), "Initial cube should be solved."
#
#     test_cube = rubiks.make_move(test_cube, "L")
#     assert not rubiks.is_solved(test_cube), "Cube should not be solved after an L move."
#
#     test_cube = rubiks.make_move(test_cube, "L'")
#     assert rubiks.is_solved(test_cube), "Cube should be solved after an L followed by an L' move."
#
#     print("test_solution_check passed")
#
#
# if __name__ == "__main__":
#     test_initialisation()
#     test_single_rotation()
#     test_multiple_rotations()
#     test_solution_check()
#     print("\nAll tests passed!")
import src.rubiks as rubiks
import copy
import unittest


class RubiksCubeTests(unittest.TestCase):

    def test_initialisation(self):
        self.assertTrue(rubiks.is_solved(rubiks.cube_main), "cube should start in a solved state")

    def test_single_rotation(self):
        test_cube = copy.deepcopy(rubiks.cube_main)
        test_cube = rubiks.make_move(test_cube, "F")
        self.assertFalse(rubiks.is_solved(test_cube), "cube should not be solved after a single F move")

    def test_multiple_rotations(self):
        test_cube = copy.deepcopy(rubiks.cube_main)
        moves = ["F", "F'", "B", "B'", "L", "L'", "R", "R'", "U", "U'", "D", "D'"]

        for move in moves:
            for _ in range(4):
                test_cube = rubiks.make_move(test_cube, move)
            self.assertTrue(rubiks.is_solved(test_cube), f"cube should be solved after rotating {move} 4 times.")

        combinations = [("F'", "F"), ("B'", "B"), ("U'", "U"), ("D'", "D"), ("R'", "R"), ("L'", "L")]
        for move1, move2 in combinations:
            for _ in range(3):
                test_cube = rubiks.make_move(test_cube, move1)
            self.assertFalse(rubiks.is_solved(test_cube), f"Cube should not be solved after rotating {move1} 3 times.")

            for _ in range(3):
                test_cube = rubiks.make_move(test_cube, move2)
            self.assertTrue(rubiks.is_solved(test_cube),
                            f"cube should be solved after rotating {move1} 3 times followed by {move2} 3 times.")

    def test_solution_check(self):
        test_cube = copy.deepcopy(rubiks.cube_main)
        self.assertTrue(rubiks.is_solved(test_cube), "initial cube should be solved.")

        test_cube = rubiks.make_move(test_cube, "L")
        self.assertFalse(rubiks.is_solved(test_cube), "cube should not be solved after an L move.")

        test_cube = rubiks.make_move(test_cube, "L'")
        self.assertTrue(rubiks.is_solved(test_cube), "cube should be solved after an L followed by an L' move.")

    def test_different_moves(self):
        test_cube = copy.deepcopy(rubiks.cube_main)
        moves = ["U", "R", "L", "D", "F", "B", "B'", "F'", "D'", "L'", "R'", "U'"]
        for i in moves:
            rubiks.make_move(test_cube, i)
        self.assertTrue(rubiks.is_solved(test_cube)), "cube should be solved after symmetric moves"


if __name__ == "__main__":
    unittest.main()

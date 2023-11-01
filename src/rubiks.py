import copy

# cube = { # this cube is for testing
#     "U": [["U1", "U2", "U3"],
#           ["U4", "U5", "U6"],
#           ["U7", "U8", "U9"]],
#     "R": [["R1", "R2", "R3"],
#           ["R4", "R5", "R6"],
#           ["R7", "R8", "R9"]],
#     "L": [["L1", "L2", "L3"],
#           ["L4", "L5", "L6"],
#           ["L7", "L8", "L9"]],
#     "D": [["D1", "D2", "D3"],
#           ["D4", "D5", "D6"],
#           ["D7", "D8", "D9"]],
#     "F": [["F1", "F2", "F3"],
#           ["F4", "F5", "F6"],
#           ["F7", "F8", "F9"]],
#     "B": [["B1", "B2", "B3"],
#           ["B4", "B5", "B6"],
#           ["B7", "B8", "B9"]],
# }


cube = {
    "U": [["U", "U", "U"],
          ["U", "U", "U"],
          ["U", "U", "U"]],
    "R": [["R", "R", "R"],
          ["R", "R", "R"],
          ["R", "R", "R"]],
    "L": [["L", "L", "L"],
          ["L", "L", "L"],
          ["L", "L", "L"]],
    "D": [["D", "D", "D"],
          ["D", "D", "D"],
          ["D", "D", "D"]],
    "F": [["F", "F", "F"],
          ["F", "F", "F"],
          ["F", "F", "F"]],
    "B": [["B", "B", "B"],
          ["B", "B", "B"],
          ["B", "B", "B"]],
}

def shift_faces(edges, temp_face, array_end=False): # TODO: fix code to make optimise make_move
    """
    function is outdated
    """
    for j in range(3):
        idx = -1 if array_end else 0
        temp = cube[temp_face][j][0]
        for i in range(len(edges) - 1, 0, -1):
            cube[edges[i]][j][idx] = cube[edges[i - 1]][j][idx]
        cube[edges[-1]][j][idx] = temp

# def rotate_face(face, clockwise=True):
#     if clockwise:
#         return [list(reversed(i)) for i in zip(*cube[face])]
#     else:
#         return [list(i) for i in zip(*cube[face])]


def rotate_face(face, clockwise=True):
    if clockwise:
        # Clockwise rotation: last column -> first row, middle column -> middle row, first column -> last row
        return [list(reversed(i)) for i in zip(*cube[face])]
    else:
        # Counter-clockwise rotation: first column -> first row, middle column -> middle row, last column -> last row
        return [list(i) for i in reversed(list(zip(*cube[face])))]


def make_move(cube, move):

    if move == "F":
        cube["F"] = rotate_face("F")

        temp = copy.deepcopy(cube["U"])
        cube["U"][2] = list(list(zip(*cube["L"]))[2])

        for j in range(3):
            cube["L"][j][2] = cube["D"][2][j]

        cube["D"][2] = list(list(zip(*cube["R"]))[0])

        for j in range(3):
            cube["R"][j][0] = temp[2][j]

    elif move == "F'":
        temp = copy.deepcopy(cube["U"])
        cube["U"][2] = list(list(zip(*cube["R"]))[0])

        for j in range(3):
            cube["R"][j][0] = cube["D"][2][j]

        cube["D"][2] = list(list(zip(*cube["L"]))[2])

        for j in range(3):
            cube["L"][j][2] = temp[2][j]

    elif move == "B":
        cube["B"] = rotate_face("B", False)
        temp = copy.deepcopy(cube["U"])
        cube["U"][0] = list(list(zip(*cube["R"]))[2])

        # # print(cube["L"])

        for j in range(3):
            cube["R"][j][2] = cube["D"][0][j]

        cube["D"][0] = list(list(zip(*cube["L"]))[0])

        for j in range(3):
            cube["L"][j][0] = temp[0][j]
            # cube["L"][j][0] = temp[0][::-1][j]

    elif move == "B'":
        cube["B"] = rotate_face("B")

        temp = copy.deepcopy(cube["U"])
        cube["U"][0] = list(list(zip(*cube["L"]))[0])

        for j in range(3):
            cube["L"][j][0] = cube["D"][0][j]

        cube["D"][0] = list(list(zip(*cube["R"]))[2])

        for j in range(3):
            cube["R"][j][2] = temp[0][j]

    elif move == "L":
        cube["L"] = rotate_face("L", False)

        temp = copy.deepcopy(cube["U"])
        for j in range(3):
            cube["U"][j][0] = cube["B"][::-1][j][2]
        for j in range(3):
            cube["B"][j][2] = cube["D"][j][2]
        for j in range(3):
            cube["D"][j][2] = cube["F"][::-1][j][0]
        for j in range(3):
            cube["F"][j][0] = temp[j][0]

    elif move == "L'":
        cube["L"] = rotate_face("L")

        temp = copy.deepcopy(cube["U"])
        for j in range(3):
            cube["U"][j][0] = cube["F"][j][0]
        for j in range(3):
            cube["F"][j][0] = cube["D"][::-1][j][2]
        for j in range(3):
            cube["D"][j][2] = cube["B"][j][2]
        for j in range(3):
            cube["B"][j][2] = temp[::-1][j][0]

    elif move == "R":
        cube["R"] = rotate_face("R")

        temp = copy.deepcopy(cube["U"])
        for j in range(3):
            cube["U"][j][2] = cube["F"][j][2]
        for j in range(3):
            cube["F"][j][2] = cube["D"][::-1][j][0]
        for j in range(3):
            cube["D"][j][0] = cube["B"][j][0]
        for j in range(3):
            cube["B"][j][0] = temp[::-1][j][2]

    elif move == "R'":
        cube["R"] = rotate_face("R", False)

        temp = copy.deepcopy(cube["U"])

        for j in range(3):
            cube["U"][j][2] = cube["B"][::-1][j][0]
        for j in range(3):
            cube["B"][j][0] = cube["D"][j][0]
        for j in range(3):
            cube["D"][j][0] = cube["F"][::-1][j][2]
        for j in range(3):
            cube["F"][j][2] = temp[j][2]

    elif move == "D":
        cube["D"] = rotate_face("D", False)

        temp = copy.deepcopy(cube["F"])
        cube["F"][2] = cube["L"][2]
        cube["L"][2] = cube["B"][2]
        cube["B"][2] = cube["R"][2]
        cube["R"][2] = temp[2]

    elif move == "D'":
        cube["D"] = rotate_face("D")

        temp = copy.deepcopy(cube["F"])
        cube["F"][2] = cube["R"][2]
        cube["R"][2] = cube["B"][2]
        cube["B"][2] = cube["L"][2]
        cube["L"][2] = temp[2]

    elif move == "U":
        cube["U"] = rotate_face("U")

        temp = copy.deepcopy(cube["F"])
        cube["F"][0] = cube["R"][0]
        cube["R"][0] = cube["B"][0]
        cube["B"][0] = cube["L"][0]
        cube["L"][0] = temp[0]

    elif move == "U'":
        cube["U"] = rotate_face("U", False)

        temp = copy.deepcopy(cube["F"])
        cube["F"][0] = cube["L"][0]
        cube["L"][0] = cube["B"][0]
        cube["B"][0] = cube["R"][0]
        cube["R"][0] = temp[0]

    return cube



def test():
    moves = ["U", "U'", "R", "R'", "L", "L'", "D", "D'", "F", "F'", "B", "B'"]
    for i in moves:
        initial_cube = copy.deepcopy(cube)
        [make_move(cube, i) for _ in range(3)]
        final_cube = copy.deepcopy(make_move(cube,i))
        if initial_cube == final_cube:
            print(f"rotate works for {i}")
        else:
            print(f"rotate does not work for {i}")

# test()

# # print(cube)
# print("anticlock:")
# print(make_move(cube, "B"))
# print(make_move(cube, "B"))
# print(make_move(cube, "B"))
#
# print("clock:")
# print(make_move(cube, "B'"))
# print(make_move(cube, "B'"))
# print(make_move(cube, "B'"))


# print(make_move(cube, "B'"))


def is_solved(cube):
    for face, rows in cube.items():
        center_color = rows[1][1]
        for row in rows:
            for color in row:
                if color != center_color:
                    return False
    return True

# print(cube)



# [['B7', 'B4', 'B1'], ['B8', 'B5', 'B2'], ['B9', 'B6', 'B3']]
# [['B9', 'B8', 'B7'], ['B6', 'B5', 'B4'], ['B3', 'B2', 'B1']]
# [['B3', 'B6', 'B9'], ['B2', 'B5', 'B8'], ['B1', 'B4', 'B7']]
# [['B1', 'B2', 'B3'], ['B4', 'B5', 'B6'], ['B7', 'B8', 'B9']]

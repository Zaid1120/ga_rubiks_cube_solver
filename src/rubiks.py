import copy

cube_dev = {  # this cube is for testing
    "U": [["U1", "U2", "U3"], ["U4", "U5", "U6"], ["U7", "U8", "U9"]],
    "R": [["R1", "R2", "R3"], ["R4", "R5", "R6"], ["R7", "R8", "R9"]],
    "L": [["L1", "L2", "L3"], ["L4", "L5", "L6"], ["L7", "L8", "L9"]],
    "D": [["D1", "D2", "D3"], ["D4", "D5", "D6"], ["D7", "D8", "D9"]],
    "F": [["F1", "F2", "F3"], ["F4", "F5", "F6"], ["F7", "F8", "F9"]],
    "B": [["B1", "B2", "B3"], ["B4", "B5", "B6"], ["B7", "B8", "B9"]],
}

cube_main = {
    "U": [["U", "U", "U"], ["U", "U", "U"], ["U", "U", "U"]],
    "R": [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"]],
    "L": [["L", "L", "L"], ["L", "L", "L"], ["L", "L", "L"]],
    "D": [["D", "D", "D"], ["D", "D", "D"], ["D", "D", "D"]],
    "F": [["F", "F", "F"], ["F", "F", "F"], ["F", "F", "F"]],
    "B": [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"]],
}


def rotate_face(cube,  face, clockwise=True):
    if clockwise:
        # clockwise rotation: last column -> first row, middle column -> middle row, first column -> last row
        return [list(reversed(i)) for i in zip(*cube[face])]
    else:
        # counter-clockwise rotation: first column -> first row, middle column -> middle row, last column -> last row
        return [list(i) for i in reversed(list(zip(*cube[face])))]


def make_move(cube, move):
    if move in ["F", "F2"]:
        repeat_count = 2 if move == "F2" else 1
        for _ in range(repeat_count):
            cube["F"] = rotate_face(cube, "F")
            temp = copy.deepcopy(cube["U"])
            cube["U"][2] = list(list(zip(*cube["L"]))[2][::-1])
            for j in range(3):
                cube["L"][j][2] = cube["D"][2][::-1][j]
            cube["D"][2] = list(list(zip(*cube["R"]))[0])
            for j in range(3):
                cube["R"][j][0] = temp[2][j]

    elif move in ["f", "f2"]:
        repeat_count = 2 if move == "f2" else 1
        for _ in range(repeat_count):
            cube["F"] = rotate_face(cube, "F")
            temp = copy.deepcopy(cube["U"])
            cube["U"][2] = list(list(zip(*cube["L"]))[2][::-1])
            for j in range(3):
                cube["L"][j][2] = cube["D"][2][::-1][j]
            cube["D"][2] = list(list(zip(*cube["R"]))[0])
            for j in range(3):
                cube["R"][j][0] = temp[2][j]

        for _ in range(repeat_count):
            temp = copy.deepcopy(cube["U"])
            cube["U"][1] = list(list(zip(*cube["L"]))[1])[::-1]
            for j in range(3):
                cube["L"][j][1] = cube["D"][1][::-1][j]
            cube["D"][1] = list(list(zip(*cube["R"]))[1])
            for j in range(3):
                cube["R"][j][1] = temp[1][j]

    elif move == "F'":
        cube["F"] = rotate_face(cube,  "F", False)
        temp = copy.deepcopy(cube["U"])
        cube["U"][2] = list(list(zip(*cube["R"]))[0])
        for j in range(3):
            cube["R"][j][0] = cube["D"][2][j]
        cube["D"][2] = list(list(zip(*cube["L"]))[2])[::-1]
        for j in range(3):
            cube["L"][j][2] = temp[2][::-1][j]

    elif move == "f'":
        cube["F"] = rotate_face(cube,  "F", False)
        temp = copy.deepcopy(cube["U"])
        cube["U"][2] = list(list(zip(*cube["R"]))[0])
        for j in range(3):
            cube["R"][j][0] = cube["D"][2][j]
        cube["D"][2] = list(list(zip(*cube["L"]))[2])[::-1]
        for j in range(3):
            cube["L"][j][2] = temp[2][::-1][j]

        temp = copy.deepcopy(cube["U"])
        cube["U"][1] = list(list(zip(*cube["R"]))[1])
        for j in range(3):
            cube["R"][j][1] = cube["D"][1][j]
        cube["D"][1] = list(list(zip(*cube["L"]))[1])[::-1]
        for j in range(3):
            cube["L"][j][1] = temp[1][::-1][j]

    elif move in ["B", "B2"]:
        repeat_count = 2 if move == "B2" else 1
        for _ in range(repeat_count):
            cube["B"] = rotate_face(cube, "B")
            temp = copy.deepcopy(cube["U"])
            cube["U"][0] = list(list(zip(*cube["R"]))[2])
            for j in range(3):
                cube["R"][j][2] = cube["D"][0][j]
            cube["D"][0] = list(list(zip(*cube["L"]))[0])[::-1]
            for j in range(3):
                cube["L"][j][0] = temp[0][::-1][j]

    elif move in ["b", "b2"]:
        repeat_count = 2 if move == "b2" else 1
        for _ in range(repeat_count):
            cube["B"] = rotate_face(cube, "B")
            temp = copy.deepcopy(cube["U"])
            cube["U"][0] = list(list(zip(*cube["R"]))[2])
            for j in range(3):
                cube["R"][j][2] = cube["D"][0][j]
            cube["D"][0] = list(list(zip(*cube["L"]))[0])[::-1]
            for j in range(3):
                cube["L"][j][0] = temp[0][::-1][j]

        for _ in range(repeat_count):
            temp = copy.deepcopy(cube["U"])
            cube["U"][1] = list(list(zip(*cube["R"]))[1])
            for j in range(3):
                cube["R"][j][1] = cube["D"][1][j]
            cube["D"][1] = list(list(zip(*cube["L"]))[1])[::-1]
            for j in range(3):
                cube["L"][j][1] = temp[1][::-1][j]

    elif move == "B'":
        cube["B"] = rotate_face(cube, "B", False)
        temp = copy.deepcopy(cube["U"])
        cube["U"][0] = list(list(zip(*cube["L"]))[0])[::-1]
        for j in range(3):
            cube["L"][j][0] = cube["D"][0][::-1][j]
        cube["D"][0] = list(list(zip(*cube["R"]))[2])
        for j in range(3):
            cube["R"][j][2] = temp[0][j]

    elif move == "b'":
        cube["B"] = rotate_face(cube, "B", False)
        temp = copy.deepcopy(cube["U"])
        cube["U"][0] = list(list(zip(*cube["L"]))[0])[::-1]
        for j in range(3):
            cube["L"][j][0] = cube["D"][0][::-1][j]
        cube["D"][0] = list(list(zip(*cube["R"]))[2])
        for j in range(3):
            cube["R"][j][2] = temp[0][j]

        temp = copy.deepcopy(cube["U"])
        cube["U"][1] = list(list(zip(*cube["L"]))[1])[::-1]
        for j in range(3):
            cube["L"][j][1] = cube["D"][1][::-1][j]
        cube["D"][1] = list(list(zip(*cube["R"]))[1])
        for j in range(3):
            cube["R"][j][1] = temp[1][j]

    elif move in ["L", "L2"]:
        repeat_count = 2 if move == "L2" else 1
        for _ in range(repeat_count):
            cube["L"] = rotate_face(cube, "L", False)
            temp = copy.deepcopy(cube["U"])
            for j in range(3):
                cube["U"][j][0] = cube["B"][::-1][j][2]
            for j in range(3):
                cube["B"][j][2] = cube["D"][j][2]
            for j in range(3):
                cube["D"][j][2] = cube["F"][::-1][j][0]
            for j in range(3):
                cube["F"][j][0] = temp[j][0]

    elif move in ["l", "l2"]:
        repeat_count = 2 if move == "l2" else 1
        for _ in range(repeat_count):
            cube["L"] = rotate_face(cube, "L", False)
            temp = copy.deepcopy(cube["U"])
            for j in range(3):
                cube["U"][j][0] = cube["B"][::-1][j][2]
            for j in range(3):
                cube["B"][j][2] = cube["D"][j][2]
            for j in range(3):
                cube["D"][j][2] = cube["F"][::-1][j][0]
            for j in range(3):
                cube["F"][j][0] = temp[j][0]
        # middle
        for _ in range(repeat_count):
            temp = copy.deepcopy(cube["U"])
            for j in range(3):
                cube["U"][j][1] = cube["B"][::-1][j][1]
            for j in range(3):
                cube["B"][j][1] = cube["D"][j][1]
            for j in range(3):
                cube["D"][j][1] = cube["F"][::-1][j][1]
            for j in range(3):
                cube["F"][j][1] = temp[j][1]

    elif move == "L'":
        cube["L"] = rotate_face(cube, "L")
        temp = copy.deepcopy(cube["U"])
        for j in range(3):
            cube["U"][j][0] = cube["F"][j][0]
        for j in range(3):
            cube["F"][j][0] = cube["D"][::-1][j][2]
        for j in range(3):
            cube["D"][j][2] = cube["B"][j][2]
        for j in range(3):
            cube["B"][j][2] = temp[::-1][j][0]

    elif move == "l'":
        cube["L"] = rotate_face(cube, "L")
        temp = copy.deepcopy(cube["U"])
        for j in range(3):
            cube["U"][j][0] = cube["F"][j][0]
        for j in range(3):
            cube["F"][j][0] = cube["D"][::-1][j][2]
        for j in range(3):
            cube["D"][j][2] = cube["B"][j][2]
        for j in range(3):
            cube["B"][j][2] = temp[::-1][j][0]

        temp = copy.deepcopy(cube["U"])
        for j in range(3):
            cube["U"][j][1] = cube["F"][j][1]
        for j in range(3):
            cube["F"][j][1] = cube["D"][::-1][j][1]
        for j in range(3):
            cube["D"][j][1] = cube["B"][j][1]
        for j in range(3):
            cube["B"][j][1] = temp[::-1][j][1]

    elif move in ["R", "R2"]:
        repeat_count = 2 if move == "R2" else 1
        for _ in range(repeat_count):
            cube["R"] = rotate_face(cube, "R")
            temp = copy.deepcopy(cube["U"])
            for j in range(3):
                cube["U"][j][2] = cube["F"][j][2]
            for j in range(3):
                cube["F"][j][2] = cube["D"][::-1][j][0]
            for j in range(3):
                cube["D"][j][0] = cube["B"][j][0]
            for j in range(3):
                cube["B"][j][0] = temp[::-1][j][2]

    elif move in ["r", "r2"]:
        repeat_count = 2 if move == "r2" else 1
        for _ in range(repeat_count):
            cube["R"] = rotate_face(cube, "R")
            temp = copy.deepcopy(cube["U"])
            for j in range(3):
                cube["U"][j][2] = cube["F"][j][2]
            for j in range(3):
                cube["F"][j][2] = cube["D"][::-1][j][0]
            for j in range(3):
                cube["D"][j][0] = cube["B"][j][0]
            for j in range(3):
                cube["B"][j][0] = temp[::-1][j][2]

        for _ in range(repeat_count):
            temp = copy.deepcopy(cube["U"])
            for j in range(3):
                cube["U"][j][1] = cube["F"][j][1]
            for j in range(3):
                cube["F"][j][1] = cube["D"][::-1][j][1]
            for j in range(3):
                cube["D"][j][1] = cube["B"][j][1]
            for j in range(3):
                cube["B"][j][1] = temp[::-1][j][1]

    elif move == "r'":
        cube["R"] = rotate_face(cube, "R", False)
        temp = copy.deepcopy(cube["U"])
        for j in range(3):
            cube["U"][j][2] = cube["B"][::-1][j][0]
        for j in range(3):
            cube["B"][j][0] = cube["D"][j][0]
        for j in range(3):
            cube["D"][j][0] = cube["F"][::-1][j][2]
        for j in range(3):
            cube["F"][j][2] = temp[j][2]

        temp = copy.deepcopy(cube["U"])
        for j in range(3):
            cube["U"][j][1] = cube["B"][::-1][j][1]
        for j in range(3):
            cube["B"][j][1] = cube["D"][j][1]
        for j in range(3):
            cube["D"][j][1] = cube["F"][::-1][j][1]
        for j in range(3):
            cube["F"][j][1] = temp[j][1]

    elif move == "R'":
        cube["R"] = rotate_face(cube, "R", False)
        temp = copy.deepcopy(cube["U"])
        for j in range(3):
            cube["U"][j][2] = cube["B"][::-1][j][0]
        for j in range(3):
            cube["B"][j][0] = cube["D"][j][0]
        for j in range(3):
            cube["D"][j][0] = cube["F"][::-1][j][2]
        for j in range(3):
            cube["F"][j][2] = temp[j][2]

    elif move in ["M", "M2"]:
        repeat_count = 2 if move == "M2" else 1
        for _ in range(repeat_count):
            temp = copy.deepcopy(cube["U"])
            for j in range(3):
                cube["U"][j][1] = cube["B"][::-1][j][1]
            for j in range(3):
                cube["B"][j][1] = cube["D"][j][1]
            for j in range(3):
                cube["D"][j][1] = cube["F"][::-1][j][1]
            for j in range(3):
                cube["F"][j][1] = temp[j][1]

    elif move == "M'":
        temp = copy.deepcopy(cube["U"])
        for j in range(3):
            cube["U"][j][1] = cube["F"][j][1]
        for j in range(3):
            cube["F"][j][1] = cube["D"][::-1][j][1]
        for j in range(3):
            cube["D"][j][1] = cube["B"][j][1]
        for j in range(3):
            cube["B"][j][1] = temp[::-1][j][1]

    if move in ["S", "S2"]:
        repeat_count = 2 if move == "S2" else 1
        for _ in range(repeat_count):
            temp = copy.deepcopy(cube["U"])
            cube["U"][1] = list(list(zip(*cube["L"]))[1])[::-1]
            for j in range(3):
                cube["L"][j][1] = cube["D"][1][::-1][j]
            cube["D"][1] = list(list(zip(*cube["R"]))[1])
            for j in range(3):
                cube["R"][j][1] = temp[1][j]

    elif move == "S'":
        temp = copy.deepcopy(cube["U"])
        cube["U"][1] = list(list(zip(*cube["R"]))[1])
        for j in range(3):
            cube["R"][j][1] = cube["D"][1][j]
        cube["D"][1] = list(list(zip(*cube["L"]))[1])[::-1]
        for j in range(3):
            cube["L"][j][1] = temp[1][::-1][j]

    elif move in ["E", "E2", "E'"]:
        repeat_count = 2 if move == "E2" else 1
        for _ in range(repeat_count):
            temp = copy.deepcopy(cube["F"])
            if move == "E'":
                cube["F"][1] = cube["R"][1]
                cube["R"][1] = cube["B"][1]
                cube["B"][1] = cube["L"][1]
                cube["L"][1] = temp[1]
            else:
                cube["F"][1] = cube["L"][1]
                cube["L"][1] = cube["B"][1]
                cube["B"][1] = cube["R"][1]
                cube["R"][1] = temp[1]

    elif move in ["D", "D2", "D'"]:
        repeat_count = 2 if move == "D2" else 1
        for _ in range(repeat_count):
            cube["D"] = rotate_face(cube, "D", move != "D'")
            temp = copy.deepcopy(cube["F"])
            if move == "D'":
                cube["F"][2] = cube["R"][2]
                cube["R"][2] = cube["B"][2]
                cube["B"][2] = cube["L"][2]
                cube["L"][2] = temp[2]
            else:
                cube["F"][2] = cube["L"][2]
                cube["L"][2] = cube["B"][2]
                cube["B"][2] = cube["R"][2]
                cube["R"][2] = temp[2]

    elif move in ["d", "d2"]:
        repeat_count = 2 if move == "d2" else 1
        for _ in range(repeat_count):
            cube["D"] = rotate_face(cube, "D")
            temp = copy.deepcopy(cube["F"])
            cube["F"][2] = cube["L"][2]
            cube["L"][2] = cube["B"][2]
            cube["B"][2] = cube["R"][2]
            cube["R"][2] = temp[2]
        for _ in range(repeat_count):
            temp = copy.deepcopy(cube["F"])
            cube["F"][1] = cube["L"][1]
            cube["L"][1] = cube["B"][1]
            cube["B"][1] = cube["R"][1]
            cube["R"][1] = temp[1]

    elif move == "d'":
        cube["D"] = rotate_face(cube, "D", False)
        temp = copy.deepcopy(cube["F"])
        cube["F"][2] = cube["R"][2]
        cube["R"][2] = cube["B"][2]
        cube["B"][2] = cube["L"][2]
        cube["L"][2] = temp[2]
        # middle
        temp = copy.deepcopy(cube["F"])
        cube["F"][1] = cube["R"][1]
        cube["R"][1] = cube["B"][1]
        cube["B"][1] = cube["L"][1]
        cube["L"][1] = temp[1]

    elif move in ["U", "U2", "U'"]:
        repeat_count = 2 if move == "U2" else 1
        for _ in range(repeat_count):
            cube["U"] = rotate_face(cube, "U", move == "U'")
            temp = copy.deepcopy(cube["F"])
            if move == "U'":
                cube["F"][0] = cube["L"][0]
                cube["L"][0] = cube["B"][0]
                cube["B"][0] = cube["R"][0]
                cube["R"][0] = temp[0]
            else:
                cube["F"][0] = cube["R"][0]
                cube["R"][0] = cube["B"][0]
                cube["B"][0] = cube["L"][0]
                cube["L"][0] = temp[0]

    elif move in ["u", "u2"]:
        repeat_count = 2 if move == "U2" else 1
        for _ in range(repeat_count):
            cube["U"] = rotate_face(cube, "U")
            temp = copy.deepcopy(cube["F"])
            cube["F"][0] = cube["R"][0]
            cube["R"][0] = cube["B"][0]
            cube["B"][0] = cube["L"][0]
            cube["L"][0] = temp[0]

            temp = copy.deepcopy(cube["F"])
            cube["F"][1] = cube["R"][1]
            cube["R"][1] = cube["B"][1]
            cube["B"][1] = cube["L"][1]
            cube["L"][1] = temp[1]

    elif move == "u'":
        cube["U"] = rotate_face(cube, "U", False)
        temp = copy.deepcopy(cube["F"])
        cube["F"][0] = cube["L"][0]
        cube["L"][0] = cube["B"][0]
        cube["B"][0] = cube["R"][0]
        cube["R"][0] = temp[0]
        # middle
        temp = copy.deepcopy(cube["F"])
        cube["F"][1] = cube["L"][1]
        cube["L"][1] = cube["B"][1]
        cube["B"][1] = cube["R"][1]
        cube["R"][1] = temp[1]

    elif move in ["x", "x2", "x'"]:
        repeat_count = 2 if move == "x2" else 1
        for _ in range(repeat_count):
            if move == "x'":
                temp = cube["U"]
                cube["U"] = cube["B"]
                cube["B"] = cube["D"]
                cube["D"] = cube["F"]
                cube["F"] = temp
            else:
                temp = cube["F"]
                cube["F"] = cube["D"]
                cube["D"] = cube["B"]
                cube["B"] = cube["U"]
                cube["U"] = temp

    elif move in ["y", "y2", "y'"]:
        repeat_count = 2 if move == "y2" else 1
        for _ in range(repeat_count):
            if move == "y'":
                temp = cube["L"]
                cube["L"] = cube["B"]
                cube["B"] = cube["R"]
                cube["R"] = cube["F"]
                cube["F"] = temp
            else:
                temp = cube["F"]
                cube["F"] = cube["R"]
                cube["R"] = cube["B"]
                cube["B"] = cube["L"]
                cube["L"] = temp

    elif move in ["z", "z2", "z'"]:
        repeat_count = 2 if move == "z2" else 1
        for _ in range(repeat_count):
            if move == "z'":
                temp = cube["R"]
                cube["R"] = cube["D"]
                cube["D"] = cube["L"]
                cube["L"] = cube["U"]
                cube["U"] = temp
            else:
                temp = cube["U"]
                cube["U"] = cube["L"]
                cube["L"] = cube["D"]
                cube["D"] = cube["R"]
                cube["R"] = temp

    return cube


def is_solved(cube):
    for face, rows in cube.items():
        center_color = rows[1][1]
        for row in rows:
            for color in row:
                if color != center_color:
                    return False
    return True

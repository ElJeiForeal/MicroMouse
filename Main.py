import Modules.GenerateMaze as MG
import Modules.printcolors as PC
import copy
import time as t
import random as r
import os
from Modules.MicroMouse import Mouse as Mouse

maze_size = (16,16)
CenterPositions = [(7,7), (8,7), (7,8), (8,8)]
StartPos = (0,maze_size[1]-1)

WallChar = f"{PC.COLORS["BLACK"]}██{PC.COLORS["_"]}"
EmptyChar = f"{PC.COLORS["_"]}██{PC.COLORS["_"]}"
MicroChar = f"{PC.COLORS["RED"]}██{PC.COLORS["_"]}"
WinChar = f"{PC.COLORS["BLUE"]}██{PC.COLORS["_"]}"
DirChar = f"{PC.COLORS["GREEN"]}██{PC.COLORS["_"]}"

def get_maze(size, scramble):
    def get_maze_structure(size, scramble):
        maze = MG.generate_maze(size, scramble, 2)
        return maze

    structure = get_maze_structure(size, scramble)

    AllWalls = {}

    for y in range(1 + size[1]*2):
        AllWalls[y] = {}
        for x in range(1 + size[0] * 2):
            AllWalls[y][x] = "W"


    for row in structure:
        for col in structure[row]:
            letters = structure[row][col]

            WallRow = 1 + row*2
            WallCol = 1 + col*2

            AllWalls[WallRow][WallCol] = "E"

            moves = {
                "U" : (0,-1),
                "D" : (0, 1),
                "R" : (1, 0),
                "L" : (-1,0)
            }

            for char in letters:
                ROW = WallRow
                COL = WallCol

                if char == "F":
                    AllWalls[ROW][COL] = "F"
                    continue

                ROW += moves[char][1]
                COL += moves[char][0]

                AllWalls[ROW][COL] = "E"
            
    return AllWalls

def draw_maze(MAZE):
    MazeTXT = ""
    for row in MAZE:
        if row != 0:
            MazeTXT += "\n"
        for col in MAZE[row]:
            letter = MAZE[row][col]
            if letter == "W":
                MazeTXT += WallChar
            elif letter == "E":
                MazeTXT += EmptyChar
            elif letter == "M":
                MazeTXT += MicroChar
            elif letter == "F":
                MazeTXT += WinChar
            elif letter == "Dir":
                MazeTXT += DirChar

    print(MazeTXT)

def draw_micro_mouse_to_maze(Maze):
    FakeMaze = copy.deepcopy(Maze)
    MicroMousePos = [Mouse.Position[0], Mouse.Position[1]]

    MicroRealPos = (MicroMousePos[0]*2 +1, MicroMousePos[1]*2 +1)
    MouseDirectionalPos = (MicroRealPos[0] + Mouse.Directions[Mouse.Direction][0], MicroRealPos[1] +Mouse.Directions[Mouse.Direction][1])
    
    FakeMaze[MicroRealPos[1]][MicroRealPos[0]] = "M"
    FakeMaze[MouseDirectionalPos[1]][MouseDirectionalPos[0]] = "Dir"

    return FakeMaze

MAZE = get_maze(maze_size, scramble=5)
Mouse.reset(StartPos, maze_size)

a = "asking"

os.system("cls")
while True:
    print("\033[2J\033[H", end="")
    #MAZE

    FakeMaze = draw_micro_mouse_to_maze(MAZE)
    draw_maze(FakeMaze)

    if a == "asking":
        a = input("")

    #Manual Control
    elif a == "r":
            MAZE = get_maze(maze_size, scramble=5)
            Mouse.reset(StartPos, maze_size)
            a = "asking"
            continue
    
    elif a == "sm":
        Mouse.reset(StartPos, maze_size)
        a ="solving"
        continue

    elif a == "BP" and Mouse.found_solution():
        print("\033[2J\033[H", end="")
        Mouse.Position = StartPos
        Mouse.FollowingPath = 0

        while not Mouse.at_finnish(CenterPositions):
            print("\033[2J\033[H", end="")


            FakeMaze = draw_micro_mouse_to_maze(MAZE)
            draw_maze(FakeMaze)

            Mouse.do_next_best_move(CenterPositions, MAZE)

            t.sleep(0.1)
        
        a = "asking"
    
    elif a == "BP" and (not Mouse.found_solution()):
        a = "asking"

    elif a == "solving":
        Mouse.do_next_best_move(CenterPositions, MAZE)
        if Mouse.found_solution():
            a = "asking"
    
    else:
        a = "asking"
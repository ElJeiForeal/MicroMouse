from collections import deque

class Mouse:
    #Important Arrays
    Directions = {
        0 : (1, 0),
        90 : (0, -1),
        180 : (-1, 0),
        270 : (0, 1)
    }

    LetterToDir ={
            "R" : 0,
            "U" : 90,
            "L" : 180,
            "D" : 270
        }

    Opposite= {
            "R" : "L",
            "U" : "D",
            "L" : "R",
            "D" : "U"
        }

    AngleToDir = {
            0 : "R",
            90 : "U",
            180 : "L",
            270 : "D"
        }

    checkingDirections = {
            "R": (1, 0),
            "U": (0, -1),
            "L": (-1, 0),
            "D": (0, 1)
        }

    #Micro Mouse
    Direction = 0

    Position = (0, 16)
    RAM = {}

    SavedPath = ""
    BestPath = ""
    FollowingPath = 0

    #Main Functions

    @staticmethod
    def SetupRam(maze_size):
        Mouse.RAM = {}
        for y in range(maze_size[1]*2 +1):
            Mouse.RAM[y] = {}
            for x in range(maze_size[0]*2+1):
                if y == 0 or y == maze_size[1]*2:
                    Mouse.RAM[y][x] = "W"
                    continue
                
                if x == 0 or x == maze_size[0]*2:
                    Mouse.RAM[y][x] = "W"
                    continue

                Mouse.RAM[y][x] = "E"
        
        #CHECKING WALLS
        for y in range(maze_size[1]-1):
            for x in range(maze_size[0]-1):
                WALLX = (x+1)*2
                WALLY = (y+1)*2
                Mouse.RAM[WALLY][WALLX] = "W"

    @staticmethod
    def RotateRight():
        Mouse.Direction = (Mouse.Direction - 90) % 360

    @staticmethod
    def RotateLeft():
        Mouse.Direction = (Mouse.Direction + 90) % 360
    
    @staticmethod
    def MoveForward():
        Mouse.Position = (Mouse.Position[0] + Mouse.Directions[Mouse.Direction][0], Mouse.Position[1] + Mouse.Directions[Mouse.Direction][1])

    @staticmethod
    def zadni():
        Mouse.Position = (Mouse.Position[0] - Mouse.Directions[Mouse.Direction][0], Mouse.Position[1] - Mouse.Directions[Mouse.Direction][1])

    @staticmethod
    def WallInFront(Maze):
        CheckForX = 1 + Mouse.Position[0]*2 + Mouse.Directions[Mouse.Direction][0]
        CheckForY = 1 + Mouse.Position[1]*2 + Mouse.Directions[Mouse.Direction][1]

        if Maze[CheckForY][CheckForX] == "W":
            return (True, (CheckForX, CheckForY))

        return (False, None)

    @staticmethod
    def WallOnRight(Maze):
        Direction = Direction = (Mouse.Direction + 90) % 360
        CheckForX = 1 + Mouse.Position[0]*2 + Mouse.Directions[Direction][0]
        CheckForY = 1 + Mouse.Position[1]*2 + Mouse.Directions[Direction][1]

        if Maze[CheckForY][CheckForX] == "W":
            return (True, (CheckForX, CheckForY))

        return (False, None)

    @staticmethod
    def WallOnLeft(Maze):
        Direction = Direction = (Mouse.Direction - 90) % 360
        CheckForX = 1 + Mouse.Position[0]*2 + Mouse.Directions[Direction][0]
        CheckForY = 1 + Mouse.Position[1]*2 + Mouse.Directions[Direction][1]

        if Maze[CheckForY][CheckForX] == "W":
            return (True, (CheckForX, CheckForY))

        return (False, None)

    @staticmethod
    def WallBehinde(Maze):
        Direction = Direction = (Mouse.Direction + 180) % 360
        CheckForX = 1 + Mouse.Position[0]*2 + Mouse.Directions[Direction][0]
        CheckForY = 1 + Mouse.Position[1]*2 + Mouse.Directions[Direction][1]

        if Maze[CheckForY][CheckForX] == "W":
            return (True, (CheckForX, CheckForY))

        return (False, None)

    @staticmethod
    def CheckForWalls(Maze):
        Infront = Mouse.WallInFront(Maze)
        Right = Mouse.WallOnRight(Maze)
        Left = Mouse.WallOnLeft(Maze)
        Down = Mouse.WallBehinde(Maze)

        if Infront[0]:
            if Mouse.RAM[Infront[1][1]][Infront[1][0]] != "W":
                Mouse.RAM[Infront[1][1]][Infront[1][0]] = "W"
            
        if Right[0]:
            if Mouse.RAM[Right[1][1]][Right[1][0]] != "W":
                Mouse.RAM[Right[1][1]][Right[1][0]] = "W"
        
        if Left[0]:
            if Mouse.RAM[Left[1][1]][Left[1][0]] != "W":
                Mouse.RAM[Left[1][1]][Left[1][0]] = "W"
        
        if Down[0]:
            if Mouse.RAM[Down[1][1]][Down[1][0]] != "W":
                Mouse.RAM[Down[1][1]][Down[1][0]] = "W"
    
    @staticmethod
    def assign_values(WinningPositions, Finnish=True, comingfrom=0):
        queue = deque()

        if Finnish:
            for position in WinningPositions:
                RealPosX = position[0] * 2 + 1
                RealPosY = position[1] * 2 + 1

                Mouse.RAM[RealPosY][RealPosX] = 0

                for dir in Mouse.checkingDirections.values():
                    adjX = RealPosX + dir[0]
                    adjY = RealPosY + dir[1]

                    if Mouse.RAM[adjY][adjX] == "W":
                        continue

                    Mouse.RAM[adjY][adjX] = 1
                    queue.append(((adjX, adjY), 1))
        else:
            queue.append((WinningPositions, comingfrom))

        while queue:
            (x, y), value = queue.popleft()

            for dir in Mouse.checkingDirections.values():
                adjX = x + dir[0]
                adjY = y + dir[1]

                val = Mouse.RAM[adjY][adjX]

                if val == "W":
                    continue

                if val == "E" or (isinstance(val, int) and val > value + 1):
                    Mouse.RAM[adjY][adjX] = value + 1
                    queue.append(((adjX, adjY), value + 1))

    @staticmethod  
    def next_best_move(WinningPositions, Maze):
        RealPosX = Mouse.Position[0] * 2 +1
        RealPosY = Mouse.Position[1]*2 +1
        
        Mouse.RAM = {y: {x: ("E" if isinstance(v, int) else v) for x, v in row.items()} for y, row in Mouse.RAM.items()}
        Mouse.CheckForWalls(Maze) # only thing that needs walls
        Mouse.assign_values(WinningPositions, Finnish = True, comingfrom = 0)

        for i in Mouse.RAM:
            txt = ""
            for x in Mouse.RAM[i]:
                txt = txt + " " + str(Mouse.RAM[i][x]) 

        allIndexesAndValls = {}
        
        for i in Mouse.checkingDirections:
            dir = Mouse.checkingDirections[i]

            posToCheckX = RealPosX+dir[0]
            posToCheckY = RealPosY+dir[1]

            VAL = Mouse.RAM[posToCheckY][posToCheckX]
            if VAL == "W":
                continue
            
            posToCheckX = RealPosX+(dir[0]*2)
            posToCheckY = RealPosY+(dir[1]*2)

            VALL = Mouse.RAM[posToCheckY][posToCheckX]

            allIndexesAndValls[i] = int(VALL/2)

        BestVal = min(allIndexesAndValls.values())

        BestLetter = next((k for k, v in allIndexesAndValls.items() if v == BestVal), None)

        return (BestLetter, BestVal)

    @staticmethod
    def narrow_down_the_path():
        if len(Mouse.SavedPath) < 2: Mouse.BestPath = Mouse.SavedPath; return

        _ = Mouse.SavedPath

        a_index = 0
        while True:
            if a_index >= len(_)-1: break

            b_index = a_index+1

            a = _[a_index]
            b = _[b_index]

            assumption = a == Mouse.Opposite.get(b)

            if not assumption:
                a_index +=1
                continue
        
            c = _[:a_index]
            d = _[(b_index+1):]
            _ = str(c + d)
            a_index -=1
        
        Mouse.BestPath = _

    @staticmethod
    def next_action(directionLetter, WinningPositions, Solving : bool = True):

        Angle = Mouse.LetterToDir[directionLetter]

        if Mouse.Direction == Angle:
            if not Mouse.at_finnish(WinningPositions):
                Mouse.MoveForward()

                if Solving:
                    Mouse.SavedPath += Mouse.AngleToDir.get(Mouse.Direction)

                    if Mouse.at_finnish(WinningPositions):
                        Mouse.narrow_down_the_path()
                
                return "Forward"
        else:
            angle_diff = (Angle - Mouse.Direction) % 360
        
            if angle_diff > 180:
                angle_diff -= 360
            
            if angle_diff == 90:
                Mouse.RotateLeft()
            elif angle_diff == -90:
                Mouse.RotateRight()
            elif abs(angle_diff) == 180:
                Mouse.zadni()

                if Solving:
                    Mouse.SavedPath += Mouse.Opposite.get(Mouse.AngleToDir.get(Mouse.Direction))
                
                return "Zadni"

            return "Rotating"

    @staticmethod
    def reset(start_pos, maze_size):
        Mouse.SavedPath = ""
        Mouse.BestPath = ""
        Mouse.Position = start_pos
        Mouse.FollowingPath = 0
        Mouse.SetupRam(maze_size)

    @staticmethod
    def found_solution():
        return Mouse.BestPath != ""

    @staticmethod
    def at_finnish(WinningPositions):
        return Mouse.Position in WinningPositions

    @staticmethod
    def set_best_path(path):
        Mouse.BestPath = path

    @staticmethod
    def do_next_best_move(WinningPositions, Maze):
        if not Mouse.found_solution():
            directionLetter,  length = Mouse.next_best_move(WinningPositions, Maze)
            Mouse.next_action(directionLetter, WinningPositions)
        else:
            if Mouse.at_finnish(WinningPositions): print("it solved the maze") ;return
            if Mouse.FollowingPath > len(Mouse.BestPath) -1: print(" SOMETHING IS AWFULLY WRONG" ) ;return    

            directionLetter= Mouse.BestPath[Mouse.FollowingPath]
            info = Mouse.next_action(directionLetter, WinningPositions, Solving= False)

            if info != "Rotating":

                Mouse.FollowingPath +=1
            

#Mouse.SetupRam((16,16)) -- gaushvi dasawyisshi
#CenterPositions = [(7,7), (8,7), (7,8), (8,8)] -- CheckingPositions = CenterPositions
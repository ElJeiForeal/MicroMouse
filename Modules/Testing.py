import os
from printcolors import COLORS

STRING = "DDLULULULULDURDRDRDRDRUU"

RED = COLORS["RED"]
BLUE = COLORS["BLUE"]
GREEN = COLORS["GREEN"]
WHITE = COLORS["_"]

os.system('cls')
print(STRING)

def shorten(string: str):
    if len(string) < 2: return string

    opposites = {
        "U" : "D",
        "L" : "R",
        "R" : "L",
        "D" : "U"
    }

    _ = string

    a_index = 0
    while True:
        if a_index >= len(_)-1: break

        b_index = a_index+1

        a = _[a_index]
        b = _[b_index]

        assumption = a == opposites.get(b)

        if not assumption:
            a_index +=1
            continue
    
        c = _[:a_index]
        d = _[(b_index+1):]
        _ = str(c + d)
        a_index -=1
    
    return _
    
        




Shortened = shorten(STRING)

print(Shortened)
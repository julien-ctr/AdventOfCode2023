import re
from typing import *
from itertools import groupby

def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()
        
def get_nearby_space(t: List[Tuple[int,int]], d: Dict, v : Set) -> int:
    result = set()
    for el in t:

        if d.get((el[0]+1,el[1]), "#") != "#" and (el[0]+1, el[1]) not in v:
            result.add((el[0]+1,el[1]))
        if d.get((el[0]-1,el[1]), "#") != "#" and (el[0]-1, el[1]) not in v:
            result.add((el[0]-1,el[1]))
        if d.get((el[0],el[1]+1), "#") != "#" and (el[0], el[1]+1) not in v:
            result.add((el[0],el[1]+1))
        if d.get((el[0],el[1]-1), "#") != "#" and (el[0], el[1]-1) not in v:
            result.add((el[0],el[1]-1))
    return result
    
def get_nearby_space2(t: List[Tuple[int,int]], d: Dict, v : Set) -> int:
    result = set()
    max_width = max([key[1] for key in d.keys()])+1
    max_height = max([key[0] for key in d.keys()])+1

    for el in t:
        if d.get(((el[0]+1)%max_height,el[1]%max_width), "#") != "#" and (el[0]+1, el[1]) not in v:
            result.add((el[0]+1,el[1]))

        if d.get(((el[0]-1)%max_height,el[1]%max_width), "#") != "#" and (el[0]-1, el[1]) not in v:
            result.add((el[0]-1,el[1]))

        if d.get((el[0]%max_height,(el[1]+1)%max_width), "#") != "#" and (el[0], el[1]+1) not in v:
            result.add((el[0],el[1]+1))

        if d.get((el[0]%max_height,(el[1]-1)%max_width), "#") != "#" and (el[0], el[1]-1) not in v:
            result.add((el[0],el[1]-1))
    
    return result

def part1(input_name: str) -> int:    
    txt = get_txt_array(input_name)
    d = {}
    start = ()

    for row in range(len(txt)):
        for col in range(len(txt[0])):
            d[(row,col)] = txt[row][col]
            if txt[row][col] == "S":
                start = (row,col)
                
    new_visited = {0: set([start])}
    visited = set([start])
    
    for k in range(1,64+1):
        print(k-1, len(new_visited[k-1]))
        new_visited[k] = get_nearby_space(list(new_visited[k-1]),d,visited)
        for newly_visited in new_visited[k]:
            visited.add(newly_visited)
    
    total = 0
    
    for key, val in list(new_visited.items())[::2]:
        total += len(val)
        
    return total
    
def part2(input_name: str) -> int:
    """
    As our map is a repeating pattern on a 2d grid, we can expect the function f(x) (where
    x is the number of times we crossed the map) to be a second degree polynomial function.
    Therefore, we can calculate the double derivative at some point (which would then be constant
    at any point)
    and extrapolate the rest of the values to get the answer.
    """    
    
    txt = get_txt_array(input_name)
    d = {}
    start = ()
    
    for row in range(len(txt)):
        for col in range(len(txt[0])):
            d[(row,col)] = txt[row][col]
            if txt[row][col] == "S":
                start = (row,col)
                
    new_visited = {0: set([start])}
    visited = set([start])
    
    max_width = max([key[1] for key in d.keys()])+1
    max_height = max([key[0] for key in d.keys()])+1

    for k in range(1,3*max_width+1):
        if (k-1)%100 == 0:
            print(f"Steps taken : {k-1}, total for now : {len(new_visited[k-1])}", end="\r")
        new_visited[k] = get_nearby_space2(list(new_visited[k-1]),d,visited)
        for newly_visited in new_visited[k]:
            visited.add(newly_visited)

    STEPS = 26501365
    
    remaining = STEPS%max_width
    nb = (STEPS - remaining)//max_width
    print(f"\nHave to do {nb} cycles over {remaining} ({nb}*{max_width}+{remaining} = {STEPS})")
    a = sum([len(val) for key, val in new_visited.items() if key%2==(remaining+2*max_width)%2 and key <= (remaining+2*max_width)])
    b = sum([len(val) for key, val in new_visited.items() if key%2==(remaining+max_width)%2 and key <= (remaining+max_width)])
    c = sum([len(val) for key, val in new_visited.items() if key%2==(remaining)%2 and key <= (remaining)])
    
    INC = (a-b)-(b-c)
    
    inc = b-c
    y = b
    p = remaining + max_width
    
    print(f"Start value of y : {y} (step {p}). starts with increment value of {inc}, a = {a}, b = {b}")
    for _ in range(nb-1):
        p += max_width
        inc = inc + INC
        y += inc
        # ~ print(f"Step {p} achieved, y is now {y}. inc = {inc}")
        real_val = sum([len(val) for key, val in new_visited.items() if key%2==(k)%2 and key <= (p)])

    return y

print(part2("inputs/21-input.txt"))


from __future__ import annotations
import re
from typing import *
from itertools import groupby

class Coord():
    def __init__(self,p):
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]
    
    def __str__(self) -> str:
        return f"x : {self.x}, y : {self.y}, z : {self.z}"

class Cuboid():
    def __init__(self, point1: Coord, point2: Coord, _id: int):
        self.id = _id
        self.p1 = point1
        self.p2 = point2
    
    def __str__(self) -> str:
        return f"{str(self.p1)} | {str(self.p2)}"
    
def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def print_layer(layers: List[List[Tuple,Tuple]], n: int, w: int = 10, h: int = 10):
    
    print("\n" + f"LAYER {n}".center(10))
    layer = layers[n]
    result = [["." for _ in range(w)] for _ in range(h)]
    for couple in layer:
        for y in range(couple[0][1], couple[1][1]+1):
            for x in range(couple[0][0], couple[1][0]+1):
                result[y][x] = "#"
    print("\n".join(["".join(line) for line in result]))

def can_go_down(layers: List[List[Tuple,Tuple]], coord: Coord):
    if coord.z == 1:
        return False
        
    layer = layers[coord.z-2]
    
    for couple in layer:
         if couple[0][0] <= coord.x <= couple[1][0] and couple[0][1] <= coord.y <= couple[1][1]:
             return False
             
    return True

def is_supporting(c1: Cuboid, c2: Cuboid) -> bool:
    """
    Returns whether c1 is supporting c2 or not
    """
    if c1.p2.z+1 != c2.p1.z:
        return False
    
    #Iterate through each block constituting the upper layer of c1
    for x in range(c1.p1.x, c1.p2.x+1):
        for y in range(c1.p1.y, c1.p2.y+1):
            if c2.p1.x <= x <= c2.p2.x and c2.p1.y <= y <= c2.p2.y:
                return True
                
    return False


def parts(input_name: str) -> int:
    txt = get_txt_array(input_name)
    first_coords = [tuple(map(lambda x : int(x),line.split("~")[0].split(","))) for line in txt]
    last_coords = [tuple(map(lambda x : int(x),line.split("~")[1].split(","))) for line in txt]
    cuboids = [Cuboid(Coord(p1), Coord(p2),i) for p1, p2, i in zip(first_coords, last_coords, range(len(first_coords)))]
    max_z = max(el[2] for el in last_coords)
    
    # ~ print(f"Max x : {max(el[0] for el in last_coords)}")
    # ~ print(f"Max y : {max(el[1] for el in last_coords)}")
    
    """
    Z layers represented by a 2d array of corners positions
    
    .................
    .................
    ....X##..........
    ....##XX#######..
    .......########..
    .......########..
    X###...########..
    ####...#######X..
    ###X.............
    
    """
    
    z_layers = [[] for _ in range(max_z)]
    
    for c in cuboids:
        min_x = c.p1.x
        max_x = c.p2.x
        min_y = c.p1.y
        max_y = c.p2.y
        for z in range(c.p1.z,c.p2.z+1):
            z_layers[z-1].append([(min_x,min_y),(max_x,max_y)])
    
    cuboids.sort(key = lambda x : (x.p1.z, x.p2.z))
    for c in cuboids:
        results = []
        while all(results):
            results = []
            for x in range(c.p1.x, c.p2.x+1):
                for y in range(c.p1.y, c.p2.y+1):
                    results.append(can_go_down(z_layers, Coord((x,y,c.p1.z))))
            if all(results):
                #Update cuboid corners
                c.p1 = Coord((c.p1.x,c.p1.y,c.p1.z-1))
                c.p2 = Coord((c.p2.x,c.p2.y,c.p2.z-1))
                
                #Update layers
                new_slice = [(c.p1.x,c.p1.y),(c.p2.x,c.p2.y)]
                z_layers[c.p1.z-1].append(new_slice)
                z_layers[c.p2.z].remove(new_slice)
    
    supporting = [[] for _ in range(len(cuboids))]
    supported = [[] for _ in range(len(cuboids))]
    for c1 in cuboids:
        for c2 in cuboids:
            if is_supporting(c2,c1):
                # ~ print(f"{c} supports {c2}")
                supporting[c1.id].append(c2.id)
                supported[c2.id].append(c1.id)
                
    can_be_removed = [True for _ in range(len(cuboids))]
    for i in supporting:
        if len(i)==1:
            can_be_removed[i[0]] = False
    
    print(f"Part 1 : {can_be_removed.count(True)}")

    
    fall_counts = 0
    for c in [x.id for x in cuboids if not can_be_removed[x.id]]:
        above_cuboids = set()
        stack = [c]
        count = 0

        while stack:
            next_block = stack.pop()
            above_cuboids.add(next_block)
            
            for block in supported[next_block]:
                if all(v in above_cuboids for v in supporting[block]):
                    count += 1
                    stack.append(block)
        
        fall_counts += count
    
    print(f"Part 2 : {fall_counts}")

parts("22-input.txt")

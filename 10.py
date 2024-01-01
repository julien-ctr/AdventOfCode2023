import re
import time
from typing import *

def get_txt_array(input: str) -> List[str]:
    with open(input,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()


def find_start(t: str) -> Tuple[int,int]:
    for y, row in enumerate(t):
        if "S" in row:
            return (y, row.index('S'))


def solve(input: str, part: int) -> int:
    
    def find_neighbours(x,y) -> List[Tuple[int,int]]:
        neighbours = []
        
        match txt[y][x]:
            case "|":
                if distances[y-1][x] == -1:
                    neighbours.append((y-1,x))
                if distances[y+1][x] == -1:
                    neighbours.append((y+1,x))
            case "-":
                if distances[y][x-1] == -1:
                    neighbours.append((y,x-1))
                if distances[y][x+1] == -1:
                    neighbours.append((y,x+1))
            case "F":
                if distances[y+1][x] == -1:
                    neighbours.append((y+1,x))
                if distances[y][x+1] == -1:
                    neighbours.append((y,x+1))
            case "L":
                if distances[y-1][x] == -1:
                    neighbours.append((y-1,x))
                if distances[y][x+1] == -1:
                    neighbours.append((y,x+1))
            case "7":
                if distances[y+1][x] == -1:
                    neighbours.append((y+1,x))
                if distances[y][x-1] == -1:
                    neighbours.append((y,x-1))
            case "J":
                if distances[y-1][x] == -1:
                    neighbours.append((y-1,x))
                if distances[y][x-1] == -1:
                    neighbours.append((y,x-1))
        
        return neighbours
    
    def replace_start(x,y):
        connection = [0,0,0,0] #NSEW
        if txt[y][x-1] in ("-","L","F"):
            connection[3] = 1
        if txt[y][x+1] in ("-","7","J"):
            connection[2] = 1
        if txt[y-1][x] in ("|","7","F"):
            connection[0] = 1
        if txt[y+1][x] in ("|","J","L"):
            connection[1] = 1
            
        match connection:
            case [1,1,0,0]:
                txt[y] = txt[y][:x] + "|" + txt[y][x+1:]
            case [1,0,1,0]:
                txt[y] = txt[y][:x] + "L" + txt[y][x+1:]
            case [1,0,0,1]:
                txt[y] = txt[y][:x] + "J" + txt[y][x+1:]
            case [0,1,1,0]:
                txt[y] = txt[y][:x] + "F" + txt[y][x+1:]
            case [0,1,0,1]:
                txt[y] = txt[y][:x] + "7" + txt[y][x+1:]
            case [0,0,1,1]:
                txt[y] = txt[y][:x] + "-" + txt[y][x+1:]
    
    def is_inside(x,y):
        inter = 0
        for dx in range(len(txt[0])-x):
            if txt[y][x+dx] in "|JL" and (y,x+dx) in in_loop :
                inter += 1
            
        return inter % 2 == 1
    
    txt = get_txt_array(input)
    s = find_start(txt)
    
    distances  = [[-1 for _ in range(len(txt[0]))] for _ in range(len(txt))]
    
    distances[s[0]][s[1]] = 0
    
    to_treat = [s]
    in_loop = set()
    
    replace_start(s[1],s[0])
    
    count = 0
    
    while len(to_treat) != 0:
        
        node = to_treat.pop(0)
        in_loop.add(node)
        n = find_neighbours(node[1],node[0])
        
        for neighbour in n:
            distances[neighbour[0]][neighbour[1]] = distances[node[0]][node[1]] + 1  #Just set it to something other than -1 to show it has been treated
            to_treat.append(neighbour)
    
    if part == 1:
        return distances[node[0]][node[1]]
    
    #else, it's part 2
    for row in range(len(txt)):
        for col in range(len(txt[0])):
            if (row, col) not in in_loop and is_inside(col, row):
                count += 1
                
    return count

print(solve('inputs/10-input.txt', part = 2))

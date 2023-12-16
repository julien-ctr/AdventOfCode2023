import re
from typing import *
import sys

def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def debug_print(v, g):
    w,h = len(g[0]), len(g)
    t = ["" for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if (x,y) in v:
                t[y] += "#"
            else:
                t[y] += "."
    for el in t:
        print(el)

def part1(input_name: str, debug: bool = False) -> int:
    def visit(cell: Tuple[int,int], direction: Tuple[int,int]):
        #print(f"Visiting {cell} with direction {direction}")
        visited.add(cell + direction)
        visited_cells.add(cell)
        
        #If out of bounds
        if cell[0] + direction[0] < 0 or cell[0] + direction[0] > len(grid[0])-1\
        or cell[1] + direction[1] < 0 or cell[1] + direction[1] > len(grid)-1:
            return 0
        
        next_cell_x, next_cell_y = cell[0] + direction[0], cell[1] + direction[1]
        next_cell = grid[next_cell_y][next_cell_x]
        if next_cell == "/":
            if (next_cell_x, next_cell_y, -direction[1],-direction[0]) not in visited:
                visit((next_cell_x,next_cell_y), (-direction[1],-direction[0]))
            
        elif next_cell == "\\":
            if (next_cell_x, next_cell_y, direction[1], direction[0]) not in visited:
                visit((next_cell_x,next_cell_y), (direction[1],direction[0]))
            
        elif next_cell == "|" and direction[0] != 0:
            if (next_cell_x, next_cell_y, 0, -1) not in visited:
                visit((next_cell_x,next_cell_y), (0,1))
                visit((next_cell_x,next_cell_y), (0,-1))
            
        elif next_cell == "-" and direction[1] != 0:
            if (next_cell_x, next_cell_y, 1, 0) not in visited:
                visit((next_cell_x,next_cell_y), (1,0))
                visit((next_cell_x,next_cell_y), (-1,0))
            
        else:
            visit((next_cell_x,next_cell_y), direction)
        
    grid = get_txt_array(input_name)
    visited = set()
    visited_cells = set()
    visit((-1,0),(1,0))
    
    if debug:
        debug_print(visited_cells, grid)
    
    return len(visited_cells)-1


def part2(input_name: str, debug: bool = False) -> int:
    def visit(cell: Tuple[int,int], direction: Tuple[int,int]):
        #print(f"Visiting {cell} with direction {direction}")
        visited.add(cell + direction)
        visited_cells.add(cell)
        
        #If out of bounds
        if cell[0] + direction[0] < 0 or cell[0] + direction[0] > len(grid[0])-1\
        or cell[1] + direction[1] < 0 or cell[1] + direction[1] > len(grid)-1:
            return 0
        
        next_cell_x, next_cell_y = cell[0] + direction[0], cell[1] + direction[1]
        next_cell = grid[next_cell_y][next_cell_x]
        if next_cell == "/":
            if (next_cell_x, next_cell_y, -direction[1],-direction[0]) not in visited:
                visit((next_cell_x,next_cell_y), (-direction[1],-direction[0]))
            
        elif next_cell == "\\":
            if (next_cell_x, next_cell_y, direction[1], direction[0]) not in visited:
                visit((next_cell_x,next_cell_y), (direction[1],direction[0]))
            
        elif next_cell == "|" and direction[0] != 0:
            if (next_cell_x, next_cell_y, 0, -1) not in visited:
                visit((next_cell_x,next_cell_y), (0,1))
                visit((next_cell_x,next_cell_y), (0,-1))
            
        elif next_cell == "-" and direction[1] != 0:
            if (next_cell_x, next_cell_y, 1, 0) not in visited:
                visit((next_cell_x,next_cell_y), (1,0))
                visit((next_cell_x,next_cell_y), (-1,0))
            
        else:
            visit((next_cell_x,next_cell_y), direction)
    
    results = {}
    grid = get_txt_array(input_name)
    size = len(grid)
    
    for x in range(size):
        grid = get_txt_array(input_name)
        visited = set()
        visited_cells = set()
        visit((x,-1),(0,1))
        results[str(x) + "_0"] = len(visited_cells)
        
        grid = get_txt_array(input_name)
        visited = set()
        visited_cells = set()
        visit((x,size),(0,-1))
        results[str(x) + "_" + str(size-1)] = len(visited_cells)
        
        grid = get_txt_array(input_name)
        visited = set()
        visited_cells = set()
        visit((-1,x),(1,0))
        results["0_" + str(x)] = len(visited_cells)
        
        grid = get_txt_array(input_name)
        visited = set()
        visited_cells = set()
        visit((size,x),(-1,0))
        results[str(size-1) + "_" + str(x)] = len(visited_cells)
        
    
    if debug:
        for k, v in results.items():
            print(f"{k} : {v}")
    
    return (results[max(results, key = results.get)]-1)
    
sys.setrecursionlimit(10000)
print(part1("16-input.txt", debug = True))

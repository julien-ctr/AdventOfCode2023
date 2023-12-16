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

def solve(input_name: str, part: int, debug: bool = False) -> int:
    def visit(cell: Tuple[int, int], direction: Tuple[int, int]):
        visited.add(cell + direction)
        visited_cells.add(cell)

        if cell[0] + direction[0] < 0 or cell[0] + direction[0] > len(grid[0]) - 1 \
                or cell[1] + direction[1] < 0 or cell[1] + direction[1] > len(grid) - 1:
            return 0

        next_cell_x, next_cell_y = cell[0] + direction[0], cell[1] + direction[1]
        next_cell = grid[next_cell_y][next_cell_x]
        
        if next_cell == "/":
            if (next_cell_x, next_cell_y, -direction[1], -direction[0]) not in visited:
                stack.append(((next_cell_x, next_cell_y), (-direction[1], -direction[0])))
        elif next_cell == "\\":
            if (next_cell_x, next_cell_y, direction[1], direction[0]) not in visited:
                stack.append(((next_cell_x, next_cell_y), (direction[1], direction[0])))
        elif next_cell == "|" and direction[0] != 0:
            if (next_cell_x, next_cell_y, 0, -1) not in visited:
                stack.append(((next_cell_x, next_cell_y), (0, 1)))
                stack.append(((next_cell_x, next_cell_y), (0, -1)))
        elif next_cell == "-" and direction[1] != 0:
            if (next_cell_x, next_cell_y, 1, 0) not in visited:
                stack.append(((next_cell_x, next_cell_y), (1, 0)))
                stack.append(((next_cell_x, next_cell_y), (-1, 0)))
        else:
            stack.append(((next_cell_x, next_cell_y), direction))

    results = {}
    grid = get_txt_array(input_name)
    size = len(grid)
    
    if part == 1: 
        visited = set()
        visited_cells = set()
        stack = [((-1,0),(1,0))] # ((Cell), (direction))
        
        while stack:
            current_cell, current_direction = stack.pop()
            visit(current_cell, current_direction)
        
        results["0_0"] = len(visited_cells)-1
            
    elif part == 2:
        visited = set()
        visited_cells = set()
        for x in range(size):
            for i in range(4):
                grid = get_txt_array(input_name)
                visited = set()
                visited_cells = set()

                if i == 0:
                    stack = [((x,-1),(0,1))]
                elif i == 1:
                    stack = [((x,size),(0,-1))]
                elif i == 2:
                    stack = [((-1,x),(1,0))]
                elif i == 3:
                    stack = [((size,x),(-1,0))]
                    
                while stack:
                    current_cell, current_direction = stack.pop()
                    visit(current_cell, current_direction)

                if i == 0:
                    results[str(x) + "_0"] = len(visited_cells)-1
                elif i == 1:
                    results[str(x) + "_" + str(size-1)] = len(visited_cells)-1
                elif i == 2:
                    results["0_" + str(x)] = len(visited_cells)-1
                elif i == 3:
                    results[str(size-1) + "_" + str(x)] = len(visited_cells)-1
        
    if debug:
        if part == 1:
            debug_print(visited_cells, grid)
        else:
            print(f"Max length found for starting point {max(results, key=results.get)}")
    
    return (results[max(results, key=results.get)])

print(solve("16-input.txt", part = 2, debug = True))

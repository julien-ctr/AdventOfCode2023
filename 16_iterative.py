import re
from typing import *
from PIL import Image, ImageDraw, ImageFont, ImageColor
import cv2
import numpy as np
from itertools import groupby
import colorsys

def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def debug_print(v, g):
    v = [i[0] for i in v]
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

def current_img(last_image, new_pixels, upscale, i):
    for new_pixel in new_pixels:
        x, y = new_pixel[0], new_pixel[1]
        for dx in range(upscale):
            for dy in range(upscale):
                # Input
                (h, s, v) = (i%360, 1, 1)

                # Normalize
                h = h / 360

                # Convert to RGB
                (r, g, b) = colorsys.hsv_to_rgb(h, s, v)

                # Expand RGB range
                (r, g, b) = (int(r * 255), int(g * 255), int(b * 255))
                last_image.putpixel((upscale*x+dx,upscale*y+dy), (r,g,b))
    return last_image

def add_frame(vid, fr):
    imtemp = fr.copy()
    vid.write(cv2.cvtColor(np.array(imtemp), cv2.COLOR_RGB2BGR))

def solve(input_name: str, part: int, debug: bool = False, generate_video: bool = False) -> int:
    def visit(cell: Tuple[int, int], direction: Tuple[int, int], depth = 0):
        visited.add(cell + direction)
        if cell not in [i[0] for i in visited_cells]:
            visited_cells.add((cell,depth))

        if cell[0] + direction[0] < 0 or cell[0] + direction[0] > len(grid[0]) - 1 \
                or cell[1] + direction[1] < 0 or cell[1] + direction[1] > len(grid) - 1:
            return 0

        next_cell_x, next_cell_y = cell[0] + direction[0], cell[1] + direction[1]
        next_cell = grid[next_cell_y][next_cell_x]
        
        if next_cell == "/":
            if (next_cell_x, next_cell_y, -direction[1], -direction[0]) not in visited:
                stack.append(((next_cell_x, next_cell_y), (-direction[1], -direction[0]), depth+1))
        elif next_cell == "\\":
            if (next_cell_x, next_cell_y, direction[1], direction[0]) not in visited:
                stack.append(((next_cell_x, next_cell_y), (direction[1], direction[0]), depth+1))
        elif next_cell == "|" and direction[0] != 0:
            if (next_cell_x, next_cell_y, 0, -1) not in visited:
                stack.append(((next_cell_x, next_cell_y), (0, 1), depth+1))
                stack.append(((next_cell_x, next_cell_y), (0, -1), depth+1))
        elif next_cell == "-" and direction[1] != 0:
            if (next_cell_x, next_cell_y, 1, 0) not in visited:
                stack.append(((next_cell_x, next_cell_y), (1, 0), depth+1))
                stack.append(((next_cell_x, next_cell_y), (-1, 0), depth+1))
        else:
            stack.append(((next_cell_x, next_cell_y), direction, depth+1))
    
    
    results = {}
    grid = get_txt_array(input_name)
    size = len(grid)
    
    if part == 1: 
        i = 0
        visited = set() # Can contain a cell multiple times if it has been reached with different direction rays
        visited_cells = set() # Only contains each cell once, with its depth (distance from starting point)
        stack = [((-1,0),(1,0),0)] # ((Cell), (direction), depth)
        
        while stack:
            current_cell, current_direction, depth = stack.pop(0) # Remove 0 for depth search, faster but makes the video look less good
            visit(current_cell, current_direction, depth)
            
        results["0_0"] = len(visited_cells)-1
        
        if generate_video:
            cells_order = sorted(list(visited_cells), key = lambda x: x[1])
            cells_order = [list(g) for key, g in groupby(cells_order, key = lambda x: x[1])]
            cells_order = [[j[0] for j in i] for i in cells_order][1:]
            TARGET_SIZE = 500
            UPSCALE = TARGET_SIZE // size
            FPS = 30
            FINAL_PAUSE = 1 # How much seconds do we stay on last state
            s = size * UPSCALE
            videodims = (s,s)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')    
            video = cv2.VideoWriter("test.mp4",fourcc, FPS,videodims)
            im = Image.new(mode="RGB", size=(s, s), color = (255,255,255))
            
            for i, cells in enumerate(cells_order):
                im = current_img(im, cells, UPSCALE, i)
                add_frame(video,im)
                print(f"{i+1} / {len(cells_order)} frames created", end = '\r')
            print()
            for _ in range(FINAL_PAUSE*FPS):
                add_frame(video,im)               
            video.release()
            
    elif part == 2:
        visited = set()
        visited_cells = set()
        for x in range(size):
            for i in range(4):
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
                    if debug:
                        im = current_img(grid,visited_cells)


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

print(solve("16-input.txt", part = 1, debug = False, generate_video = True))


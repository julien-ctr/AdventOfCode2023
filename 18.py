import re
from typing import *
import sys
from PIL import Image, ImageDraw, ImageFont, ImageColor

def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def cross_product(a, b):
    return a[0]*b[1]-a[1]*b[0]

def is_inside(col,row,t):
    t = [list(g) for key, g in groupby(t[row][col+1:])]
    count = 0
    for group in t:
        if 1 in group:
            if len(group) > 1:
                count += 2
            else:
                count += 1
    return count%2==1
        

def part1(input_name: str):
    d = {'R' : (1,0), 'L': (-1,0), 'U': (0,-1), 'D': (0,1)}
    txt = get_txt_array(input_name)
    instructions = [(line.split(" ")[0],int(line.split(" ")[1])) for line in txt]
    positions = [(0,0)]
    
    current_y = 0
    current_x = 0
    min_x, max_x, min_y, max_y = (0,0,0,0)
    for ins in instructions:
        if ins[0] == "R":
            current_x += ins[1]
            if current_x > max_x:
                max_x = current_x
        elif ins[0] == "L":
            current_x -= ins[1]
            if current_x < min_x:
                min_x = current_x
        if ins[0] == "D":
            current_y += ins[1]
            if current_y > max_y:
                max_y = current_y
        elif ins[0] == "U":
            current_y -= ins[1]
            if current_y < min_y:
                min_y = current_y
                
    max_width = max_x - min_x + 1
    max_height = max_y - min_y + 1
    
    tab = [[0 for _ in range(max_width)] for _ in range(max_height)]
    
    
    current_y = -min_y
    current_x = -min_x
    tab[current_y][current_x] = 1
    
    for ins in instructions:
        match ins[0]:
            case "R":
                for dx in range(ins[1]):
                    tab[current_y][current_x+dx] = 1
                current_x += ins[1]
            case "L":
                for dx in range(ins[1]):
                    tab[current_y][current_x-dx] = 1
                current_x -= ins[1]
            case "U":
                for dy in range(ins[1]):
                    tab[current_y-dy][current_x] = 1
                current_y -= ins[1]
            case "D":
                for dy in range(ins[1]):
                    tab[current_y+dy][current_x] = 1
                current_y += ins[1]
                
    
         
    
    for row in range(len(tab)):
        inside = False
        in_wall = False
        wall_dir = 0
        last_checked = 0
        for col in range(len(tab[0])):
            if tab[row][col] == 1:
                if last_checked == 1 and not in_wall:
                    in_wall = True
                    if row-1 > 0 and tab[row-1][col-1] == 1:
                        wall_dir = -1
                    elif row+1 < max_height and tab[row+1][col-1] == 1:
                        wall_dir = 1
                    else:
                        wall_dir = None
                if not in_wall:
                    inside = not inside
                last_checked = 1
            elif tab[row][col] == 0:
                if in_wall: # If getting out of a series of walls
                    print(wall_dir)
                    print(max_height)
                    if tab[row+wall_dir][col-1] == 1:
                        inside = not inside
                    in_wall = False
                if inside:
                    tab[row][col] = 2
                last_checked = 0
                
    im = Image.new(mode="RGB", size=(max_width, max_height), color = (255,255,255))
    for row in range(len(tab)):
        for col in range(len(tab[0])):
            if tab[row][col] in (1,2):
                im.putpixel((col,row),(255,0,0))
    im.save("testimg.jpg")
    
    for el in tab:
        print(el)
        
    print(sum([line.count(1) + line.count(2) for line in tab]))
    
def part2(input_name: str) -> int:
    d = {'R' : (1,0), 'L': (-1,0), 'U': (0,-1), 'D': (0,1)}
    digit_to_dir = "RDLU"
    txt = get_txt_array(input_name)
    instructions = [(digit_to_dir[int(line.split("#")[1][-2:-1])],int(line.split("#")[1][:-2],16)) for line in txt]
    #instructions = [(line.split(" ")[0],int(line.split(" ")[1])) for line in txt]
    
    positions = [(0,0)]
    for ins in instructions:
        command = ins[0]
        qty = ins[1]
        
        positions.append((positions[-1][0] + qty * d[command][0], positions[-1][1] + qty * d[command][1]))
        
    s=0
    perimeter = 0
    for i in range(len(positions)-1):
        
        s += positions[i][0]*positions[i+1][1]-positions[i][1]*positions[i+1][0]
    
        perimeter += abs(positions[i][0]-positions[i+1][0]) + abs(positions[i][1]-positions[i+1][1])
        
    return ((s+perimeter)//2 + 1)

print(part2("inputs/18-input.txt"))
    

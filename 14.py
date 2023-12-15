import re
import time
from typing import *
from itertools import groupby

def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def string_swap(s, a, b):
    """
    Given a string s, exchanges the characters at index a and b
    """
    
    if a > b:
        a, b = b, a
    return s[:a] + s[b] + s[a+1:b] + s[a] + s[b+1:]

def part1(input_name: str) -> int:
    total = 0
    
    txt = get_txt_array(input_name)
    width, height = len(txt[0]), len(txt)
    
    for col in range(width):
        x = 0
        for row in range(height):
            if txt[row][col] == "O":
                total += (height - x)
                print(height-x)
                x += 1
            elif txt[row][col] == "#":
                x = row+1
                
    return total


def cycle(t):
    w, h = len(t[0]), len(t)

    #North
    for col in range(w):
        for row in range(h):
            if t[row][col] == "O":
                i = row
                while i > 0 and t[i-1][col] == ".":
                    i -= 1
                if i != row:
                    t[row] = t[row][:col] + "." + t[row][col+1:]
                    t[i] = t[i][:col] + "O" + t[i][col+1:]
                    
    #West
    for row in range(h):
        for col in range(w):
            if t[row][col] == "O":
                i = col
                while i > 0 and t[row][i-1] == ".":
                    i -= 1
                if i != col:
                    t[row] = string_swap(t[row],col,i)
    
    #South
    for col in range(w):
        for row in range(h-1,-1,-1):
            if t[row][col] == "O":
                i = row
                while i < h-1 and t[i+1][col] == ".":
                    i += 1
                if i != row:
                    t[row] = t[row][:col] + "." + t[row][col+1:]
                    t[i] = t[i][:col] + "O" + t[i][col+1:]

    #East
    for row in range(h):
        for col in range(w-1,-1,-1):
            if t[row][col] == "O":
                i = col
                while i < w-1 and t[row][i+1] == ".":
                    i += 1
                if i != col:
                    t[row] = string_swap(t[row],col,i)

def current_score(t: List[str]) -> int:
    """
    Calculates the score for a given configuration t
    """
    total = 0
    width, height = len(t[0]), len(t)
    for col in range(width):
        for row in range(height):
            if t[row][col] == "O":
                total += (height - row)
    return total

def get_grid_identity(t: List[str]) -> Set:
    """
    Returns a unique set contaning rocks positions as integers
    """
    res = set()
    for row in range(len(t)):
        for col in range(len(t[0])):
            if t[row][col] == "O":
                res.add(row * len(t[0]) + col)
    return res

def part2(input_name: str, debug: bool = True) -> int:
    """
    Strategy : 
    Look for a loop of length < 1_000_000_000
    then just take the remainder of (1_000_000_000 - loop_start) / loop_length
    and plug it into the score values of the loop
    """
    
    txt = get_txt_array(input_name)
    old_ids = []
    old_scores = []
    
    current_id = get_grid_identity(txt)
    c = 0
    while current_id not in old_ids and c < 1_000_000_000:
        old_ids.append(current_id)
        old_scores.append(current_score(txt))
        cycle(txt)
        current_id = get_grid_identity(txt)
        
        c += 1
            
    
    loop_start = old_ids.index(current_id)
    loop_length = len(old_ids)-loop_start
    remaining = (1_000_000_000 - loop_start) % loop_length
    final_score = old_scores[loop_start+remaining]
    
    if debug:
        print(f"loop found after {len(old_ids)-1} cycles")
        print(f"Possible scores : {old_scores[:]}")
        print(f"loop starts at {loop_start}. total length : {loop_length}")
        print(f"remaining : {remaining}")

    return final_score

a = part2("14-input.txt", debug = True)
print(a)  


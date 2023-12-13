import re
import time
from typing import *
from itertools import groupby

def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()
        
def compute_strings(t: List[List[str]], axis: str, i: int, dx: int) -> tuple:
    if axis == "h":  # Horizontal
        s1 = t[i + dx + 1]
        s2 = t[i - dx]
    else:  # Vertical
        s1 = "".join(line[i + dx + 1] for line in t)
        s2 = "".join(line[i - dx] for line in t)
    return s1, s2
        
def check_mirror(t: List[List[str]], axis: str, i: int, verbose=False, tolerance=0) -> bool:
    # Mirror line between i and i+1
    
    d = 0  # Differences counter
    n = min(len(t) - i - 1, i + 1) if axis == "h" else min(len(t[0]) - i - 1, i + 1)  # Distance to closest border
    
    for dn in range(n):
        s1, s2 = compute_strings(t, axis, i, dn)

        if verbose:
            print(f"{i + dn + 1}, {i - dn}")
            print(f"Currently comparing these two:\n{s1}\n{s2}")

        differing_count = sum(1 for a, b in zip(s1, s2) if a != b)
        d += differing_count

    return d == tolerance
        
def prettyprint(a,b,c):
    if c == "h":
        for i, line in enumerate(a):
            arrow = "v" if i == b else "^" if i == b + 1 else " "
            print(f"{i % 10} {arrow} {line} {arrow} {i % 10}")
    else:   
        separator = " " * (b) + "><" + " " * (len(a[0]) - b + 1)
        indices = "".join(str(k % 10) for k in range(len(a[0])))
        print(indices)
        print(separator)
        for line in a:
            print(line)
        print(separator)
        print(indices)
        
    print()

def solve(input_name: str, part: int, debug = False) -> int:
    txt = get_txt_array(input_name)
    formated_txt = [[]]
    result = 0
    tolerance = 1 if part == 2 else 0
    
    #Separate each dataset
    formated_txt = [list(group) for key, group in groupby(txt, key=bool) if key]
    
    for dataset in formated_txt:
        height, width = len(dataset), len(dataset[0])
        mirror = -1
        
        for y in range(0,height-1):
            if check_mirror(dataset, "h", y, tolerance = tolerance):
                result += 100*(y+1)
                mirror = y+1
                mirror_type = "h"
                
        
        for x in range(0,width-1):
            if check_mirror(dataset, "v", x, tolerance = tolerance):
                result += (x+1)
                mirror = x+1
                mirror_type = "v"
                
        if debug:
            print("\n[New dataset]")
            prettyprint(dataset, mirror-1, mirror_type)
    
    return result

res = solve("13-input.txt", part = 1, debug = False)
print(res)

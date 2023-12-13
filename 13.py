import re
import time
from typing import *

def get_txt_array(input: str) -> List[str]:
    with open(input,'r',encoding = 'utf-8') as f:
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
            if i == b :
                print(f"{i%10} v {line} v {i%10}")
            elif i == b+1:
                print(f"{i%10} ^ {line} ^ {i%10}")
            else:
                print(f"{i%10}   {line}   {i%10}")
    else:   
        for k in range(len(a[0])):
            print((k%10), end = "")
        print("\n" + " " * (b) + "><" + " " * (len(a[0])-b+1))
        for line in a:
            print(line)
        print(" " * (b) + "><" + " " * (len(a[0])-b+1))
        for k in range(len(a[0])):
            print((k%10), end = "")

def solve(input: str, part: int, debug = False) -> int:
    txt = get_txt_array(input)
    formated_txt = [[]]
    result = 0
    tol = 1 if part == 2 else 0
    
    #Separate each dataset
    for i in range(len(txt)):
        if not txt[i]:
            formated_txt.append([])
        else:
            formated_txt[-1].append(txt[i])
    
    for dataset in formated_txt:
        height = len(dataset)
        width = len(dataset[0])
        mirror = -1
        
        for y in range(0,height-1):
            if check_mirror(dataset, "h", y, tolerance = tol):
                result += 100*(y+1)
                mirror = y+1
                mirror_type = "h"
                
        
        for x in range(0,width-1):
            if check_mirror(dataset, "v", x, tolerance = tol):
                result += (x+1)
                mirror = x+1
                mirror_type = "v"
                
        if debug:
            print("\n\n[New dataset]")
            prettyprint(dataset, mirror-1, mirror_type)
    
    return result

a = solve("13-input.txt", part = 2, debug = True)
print(a)

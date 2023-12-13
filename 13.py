import re
import time
from typing import *

def get_txt_array(input: str) -> List[str]:
    with open(input,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def check_mirror(t: List[List[str]], axis: str, i: int, verbose = False)-> bool:
    #mirror line between i and i+1
    
    if axis == "h": #horizontal
        y = min(len(t)-i-1,i+1) #distance to closest border
        
        for dy in range(y):
            s1 = t[i+dy+1]
            s2 = t[i-dy]
            
            if verbose:
                print(i+dy+1, i-dy)
                print(f"CurrentlY comparing these two :\n{s1}\n{s2}")
                
            if s1 != s2:
                return False
                
        return True
    
    if axis == "v":
        x = min(len(t[0])-i-1,i+1) #distance to closest border
        
        for dx in range(x):
            s1 = "".join([line[i+dx+1] for line in t])
            s2 = "".join([line[i-dx] for line in t])
            
            if verbose:
                print(i+dx+1, i-dx)
                print(f"Currently comparing these two :\n{s1}\n{s2}")
                
            if s1 != s2:
                return False
                
        return True
        
def check_almost_mirror(t: List[List[str]], axis: str, i: int, verbose = False)-> bool:
    #mirror line between i and i+1
    d = 0
    if axis == "h": #horizontal
        y = min(len(t)-i-1,i+1) #distance to closest border
        
        for dy in range(y):
            s1 = t[i+dy+1]
            s2 = t[i-dy]
            
            if verbose:
                print(i+dy+1, i-dy)
                print(f"CurrentlY comparing these two :\n{s1}\n{s2}")
                
            if s1 != s2:
                differing_count = sum(1 for a, b in zip(s1, s2) if a != b)
                d += differing_count
                
        
    
    if axis == "v":
        x = min(len(t[0])-i-1,i+1) #distance to closest border
        
        for dx in range(x):
            s1 = "".join([line[i+dx+1] for line in t])
            s2 = "".join([line[i-dx] for line in t])
            
            if verbose:
                print(i+dx+1, i-dx)
                print(f"Currently comparing these two :\n{s1}\n{s2}")
                
            if s1 != s2:
                differing_count = sum(1 for a, b in zip(s1, s2) if a != b)
                d += differing_count
    
    return d == 1
        
def prettyprint(a,b,c):
    print(b)
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

def part1(input: str, debug = False)-> int:
    txt = get_txt_array(input)
    formated_txt = [[]]
    result = 0
    
    for i in range(len(txt)):
        if not txt[i]:
            formated_txt.append([])
        else:
            formated_txt[-1].append(txt[i])
    
    for dataset in formated_txt:
        height = len(dataset)
        width = len(dataset[0])
        mirror = 0
        
        for y in range(0,height-1):
            if check_mirror(dataset,"h",y):
                result += 100*(y+1)
                mirror = y+1
                mirror_type = "h"
                
                
        for x in range(0,width-1):
            if check_mirror(dataset,"v",x):
                result += (x+1)
                mirror = x+1
                mirror_type = "v"
                
        if debug:
            print("\n\n[New dataset]")
            prettyprint(dataset, mirror-1, mirror_type)
                
    return result

def part2(input: str, debug = False)-> int:
    txt = get_txt_array(input)
    formated_txt = [[]]
    result = 0
    
    for i in range(len(txt)):
        if not txt[i]:
            formated_txt.append([])
        else:
            formated_txt[-1].append(txt[i])
    
    for dataset in formated_txt:
        height = len(dataset)
        width = len(dataset[0])
        mirror = 0
        
        for y in range(0,height-1):
            if check_almost_mirror(dataset,"h",y):
                result += 100*(y+1)
                mirror = y+1
                mirror_type = "h"
                
                
        for x in range(0,width-1):
            if check_almost_mirror(dataset,"v",x):
                result += (x+1)
                mirror = x+1
                mirror_type = "v"
                
        if debug:
            print("\n\n[New dataset]")
            prettyprint(dataset, mirror-1, mirror_type)
                
    print(result)
    return result
    
part2("13-input.txt", debug = True)

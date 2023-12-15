import re
import time
from typing import *

def get_txt_array(input: str) -> List[str]:
    with open(input,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def prettyprint(t: List[List[int]]):
    result = ""    
    width = len(str(max(t[0],key=abs)))+1
    
    for row in t:
        s = ""
        for val in row:
            s += str(val) + ' ' * (width - len(str(val)))
        result += '\n' + s.center(width * len(t[0]))
        
    print(result)
    
def part1(input: str, debug: bool = False) -> int:
    txt = get_txt_array(input)
    score = 0
    
    for k, line in enumerate(txt):
        #Get the initial values
        t = [list(map(lambda x: int(x),re.findall(r"(-?\d+)",line)))]
        
        #Build the differences arrays
        while t[-1] != [0 for _ in range(len(t[-1]))]:
            t.append([t[-1][i]-t[-1][i-1] for i in range(1,len(t[-1]))])
        
        if debug:
            print("====== BEFORE EXTRAPOLATION ======")
            prettyprint(t)
        
        
        #Extrapolate
        t[-1].append(0)
        for n in range(len(t)-2,-1,-1):
            t[n].append(t[n][-1] + t[n+1][-1])
            
        score += t[0][-1]
        
        if debug:
            print("====== AFTER EXTRAPOLATION ======")
            prettyprint(t)
            #print(f"Dataset {k} gives an extrapolation of {t[0][-1]}")
    return score

def part2(input: str, debug: bool = False) -> int:
    txt = get_txt_array(input)
    score = 0
    
    for k, line in enumerate(txt):
        #Get the initial values
        t = [list(map(lambda x: int(x),re.findall(r"(-?\d+)",line)))]
        
        #Build the differences arrays
        while t[-1] != [0 for _ in range(len(t[-1]))]:
            t.append([t[-1][i]-t[-1][i-1] for i in range(1,len(t[-1]))])
        
        if debug:
            print("====== BEFORE EXTRAPOLATION ======")
            prettyprint(t)
        
        
        #Extrapolate
        t[-1].insert(0,0)
        for n in range(len(t)-2,-1,-1):
            t[n].insert(0, t[n][0] - t[n+1][0])
            
        score += t[0][0]
        
        if debug:
            print("====== AFTER EXTRAPOLATION ======")
            prettyprint(t)
            #print(f"Dataset {k} gives an extrapolation of {t[0][0]}")
    return score
    
    
print(part2('09-input.txt', debug = True))

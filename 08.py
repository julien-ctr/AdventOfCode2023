import re
from typing import *

def get_txt_array(input: str) -> List[str]:
  with open(input,'r',encoding="utf-8") as f:
    return f.read().splitlines()

def pgcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a
  
def ppcm(a: int, b: int) -> int:
    return (a*b)//pgcd(a,b)

def part1(input: str, debug: bool = False) -> int:
    txt = get_txt_array(input)
    
    instructions =txt[0].strip()
    starts = [line.split(' ')[0] for line in txt[2:]]
    a = [line.split('(')[1].split(',')[0] for line in txt[2:]]
    b = [line.split(',')[-1].split(')')[0].strip() for line in txt[2:]]
    d = dict((key, value) for key, value in zip(starts, zip(a,b)))
    
    i = 0
    
    act = 'AAA'
    while act != 'ZZZ':
        if instructions[i%len(instructions)]=='L':
            act = d[act][0]
        elif instructions[i%len(instructions)]=='R':
            act = d[act][1]
            
        i += 1
        
        if debug:
            print(f"\nWent  {instructions[i%len(instructions)]}")
            print(f"now at {act} after {i} steps. Next choices : {d[act]}")
      
    
  
    return i

def part2(input: str, debug: bool = False) -> int:
    txt = get_txt_array(input)
    
    instructions =txt[0].strip()
    starts = [line.split(' ')[0] for line in txt[2:]]
    a = [line.split('(')[1].split(',')[0] for line in txt[2:]]
    b = [line.split(',')[-1].split(')')[0].strip() for line in txt[2:]]
    d = dict((key, value) for key, value in zip(starts, zip(a,b)))
  
    
  
    acts = []
    for line in txt[2:]:
        if line[2] == 'A':
            acts.append(line[:3])

    mins = [0 for _ in range(len(acts))]
  
    for k, node in enumerate(acts):
        i = 0
        while mins[k] == 0:
            if instructions[i%len(instructions)]=='L':
                node = d[node][0]
            elif instructions[i%len(instructions)]=='R':
                node = d[node][1]
                
            if node[2]=="Z":
                mins[k] = i+1
                if debug:
                    print(f"min {k} is {i}")
                
            i += 1
            
    r = mins[0]
    for m in mins[1:]:
        if debug:
            print(f"r = {r}\nm = {m}\nppcm = {ppcm(r,m)}\n")
        r = ppcm(r, m)
    return r

print(part2("08-input.txt", debug = False))

import re
import time
from typing import *

def get_txt_array(input: str) -> List[str]:
    with open(input,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def find_empty_rows(t: List[List[str]]) -> List[int]:
    res = []
    for i, row in enumerate(t):
        if row == "." * len(row):
            res.append(i)
    return res

def find_empty_cols(t: List[List[str]]) -> List[int]:
    res = []
    for i in range(len(t[0])):
        if [t[k][i] for k in range(len(t))] == ["." for _ in range(len(t))]:
            res.append(i)
    return res

def find_galaxies(t: List[List[str]]) -> List[Tuple[int,int]]:
    res = []
    for irow in range(len(t)):
        for icol in range(len(t[0])):
            if t[irow][icol] == "#":
                res.append((irow, icol))
    return res

def calc_dist(g1 : Tuple[int,int], g2 : Tuple[int,int], empty_rows: List[int], empty_cols: List[int], fact: int) -> int:
    start_row = min(g1[0],g2[0])
    end_row = max(g1[0],g2[0])
    
    start_col = min(g1[1],g2[1])
    end_col = max(g1[1],g2[1])
    
    #Calculate initial distance (Manhattan distance)
    dy = abs(g1[0] - g2[0])
    dx = abs(g1[1] - g2[1])
    
    #Add space dilatation
    for e_row in empty_rows:
        if start_row < e_row and e_row < end_row:
            dy += fact-1
            
    for e_col in empty_cols:
        if start_col < e_col and e_col < end_col:
            dx += fact-1
    
    return dx+dy
            
        

def part1(input: str) -> int:
    txt = get_txt_array(input)
    a = find_empty_rows(txt)
    b = find_empty_cols(txt)
    g = find_galaxies(txt)
    min_dists = []
    
    for k in range(len(g)):
        for j in range(k+1,len(g)):
            d = calc_dist(g[k],g[j],a,b,fact=2)
            min_dists.append(d)
            
    
    return sum(min_dists)
    

def part2(input: str) -> int:
    txt = get_txt_array(input)
    a = find_empty_rows(txt)
    b = find_empty_cols(txt)
    g = find_galaxies(txt)
    min_dists = []
    
    for k in range(len(g)):
        for j in range(k+1,len(g)):
            d = calc_dist(g[k],g[j],a,b,fact=1_000_000)
            min_dists.append(d)
            
    
    return sum(min_dists)
    
print(part2("11-input.txt"))

import re
import time
from typing import *
from itertools import combinations
from functools import cache
from math import factorial as fact
from math import prod

def get_txt_array(input: str) -> List[str]:
    with open(input,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()


def calc_time(s : int)-> str:
    s = round(s)
    t = [s,0,0]
    for i in range(1,3):
        t[i] = t[i-1]//60
        t[i-1] = t[i-1]%60
    result = ''
    if t[2] != 0:
        result = f"{str(t[2])} hours {str(t[1])} minutes and {str(t[0])} seconds"
    elif t[1] != 0:
        result = f"{str(t[1])} minutes and {str(t[0])} seconds"
    else:
        result = f"{str(t[0])} seconds"
    return result


@cache
def f(txt, grps, k):
    
    if len(grps) == 0:
        #print("valid")
        return 1 if txt.count("#") == 0 else 0
    elif len(grps) == 1 and k == grps[0] and txt.count("#") == 0:
        #print("valid")
        return 1
    if txt == "":
        return 0

    first_char = txt[0]
    grp = grps[0]
    #print(txt, grps, k, first_char, grp)
    
    if first_char == ".":
        if k == grp:
            return f(txt[1:], grps[1:], 0)
        elif k == 0:
            return f(txt[1:],grps,0) 
        else:
            return 0

    elif first_char == "#":
        k+=1
        if k > grp:
            return 0
        return f(txt[1:], grps, k)
        
    elif first_char == "?":
        a = f("#" + txt[1:], grps, k)
        b = f("." + txt[1:], grps, k)
        return a+b


def verify(s, l):
    i = 0
    k = 0


    while k < len(s) and i < len(l):
        if s[k:k + l[i]] == "#" * l[i] and ((k + l[i] == len(s)) or s[k + l[i]] == "."):
            i += 1
            k += l[i - 1]
        else:
            k += 1
        if i == len(l):
            return True

    return False
    

def count_groups(txt: str, size: int) -> int:
    holes = txt.count("?")
    count = 0
    sol = []
    for k in range(2**holes):
        s = txt
        pos = []
        for bit in range(holes):
            if (k>>bit)&1 == 1:
                pos.append(s.index('?'))
                s = s.replace('?','#',1)
            else:
                s = s.replace('?','.',1)
                
        if verif(s,size) and k.bit_count() <= size:
            #print(f"{s} valid")
            count += 1
            sol.append(pos)
    
    return sol
    

def part1(input: str) -> int:
    """
    Strategy 1 : try each combination of k éléments
    where k is the amount of # missing to reach the sum of all
    spring groups lengths.
    """
    
    data = get_txt_array(input)
    tot = 0
    
    for n, d in enumerate(data):
        l = list(map(lambda x: int(x), re.findall(r'(\d+)', d.split(' ')[1])))
        chain = d.split(' ')[0]
        num = chain.count('?')
        a = sum(l)-chain.count("#")
        
        c = 0

        for combin in combinations([i for i in range(num)],a):
            s = chain
            xcount = 0
            for char in s:
                if char == "?":
                    if xcount in combin:
                        s = s.replace('?', '#', 1)
                    else:
                        s = s.replace('?', '.', 1)
                    xcount += 1

            if verify(s, l):
                c += 1
          
        #print(c)
        tot += c
      
    return tot

def part1b(input: str, debug = False) -> int:
    """
    Strategy 2 : recursive approach, read each line character by
    character from left to right, and "branch" when encountering a ?
    in order to consider all possibilities. When an impossible or valid
    solution is found, return either 0 or 1.
    """
    
    tot = 0
    data = get_txt_array(input)
    
    for i,li in enumerate(data):
        chain = li.split(' ')[0]
        l = list(map(lambda x:int(x),li.split(' ')[1].split(',')))
        
        a=(f(chain, tuple(l), 0))

        tot+=a
        
        now = time.time()
        
        if debug:
            print(chain,l)
            print(f"Line {i} : {a} found (Total elapsed time : {calc_time(now-start)})")
        
    print(tot)
    return tot
   

def part2(input: str, debug = False) -> int:
    tot = 0
    data = get_txt_array(input)
    
    for i,li in enumerate(data):
        chain = li.split(' ')[0]
        chain = ((chain+"?")*5)[:-1]
        l = list(map(lambda x:int(x),li.split(' ')[1].split(',')))
        l = 5*l
        
        a=(f(chain, tuple(l), 0))

        tot+=a
        
        now = time.time()
        
        if debug:
            print(chain,l)
            print(f"Line {i} : {a} found (Total elapsed time : {calc_time(now-start)})")
        
    print(tot)
    return tot
    
    
start = time.time()
t2 = part2("12-input.txt")
end = time.time()

print(end-start)

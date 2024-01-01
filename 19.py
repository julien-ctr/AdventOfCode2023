import re
from typing import *
import sys
from itertools import groupby

def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def rule_valid(rule: str, part: Dict):
    if ">" not in rule and "<" not in rule:
        return rule
    
    result = rule.split(':')[1]

    if "<" in rule:
        letter = rule.split('<')[0]
        value = int(rule.split('<')[1].split(':')[0])
        if part[letter] < value:
            return result
    else:
        letter = rule.split('>')[0]
        value = int(rule.split('>')[1].split(':')[0])
        if part[letter] > value:
            return result

def range_valid(rule: str, x,m,aa,s):
    """
    example : 
        rule = s < 1351 : fg
        a = 1
        b = 4000
        returns [((1,1350), fg),((1351,4000),None)]
    """
    if ">" not in rule and "<" not in rule:
        return [x+m+aa+s+(rule,)]
    
    result = rule.split(':')[1]
    t = []
    letter = rule[0]
    
    if letter == "x":
        a = x[0]
        b = x[1]
    elif letter == "m":
        a = m[0]
        b = m[1]
    elif letter == "a":
        a = aa[0]
        b = aa[1]
    elif letter == "s":
        a = s[0]
        b = s[1]
    
    if "<" in rule:
        value = int(rule.split('<')[1].split(':')[0])
        if a < value <= b:
            t.append((a,value-1,result))
            t.append((value,b,None))
        elif a <= b < value: 
            t.append((a,b,result))
        elif value <= a <= b:
            t.append((a,b,None))
    else:        
        value = int(rule.split('>')[1].split(':')[0])
        
        if b > value >= a:
            t.append((value+1,b,result))
            t.append((a,value,None))
        elif b >= a > value: 
            t.append((a,b,result))
        elif value >= b >= a:
            t.append((a,b,None))
    
    rt = []
    for el in t:
        if letter == "x":
            rt.append((el[0],) + (el[1],) + m + aa + s + (el[2],))
        if letter == "m":
            rt.append(x + (el[0],) + (el[1],) + aa + s + (el[2],))
        if letter == "a":
            rt.append(x + m + (el[0],) + (el[1],) + s + (el[2],))
        if letter == "s":
            rt.append(x + m + aa + (el[0],) + (el[1],) + (el[2],))
    return rt
    
def part1(input_name: str) -> int:
    txt = get_txt_array(input_name)
    txt = [list(g) for key, g in groupby(txt, bool) if g != [""]]
    txt.pop(1)
    
    workflows = dict((key, value) for key, value in zip([line.split("{")[0] for line in txt[0]], [line.split("{")[1][:-1].split(",") for line in txt[0]]))
    parts = list(dict((key,value) for key, value in zip("xmas", list(map(lambda x : int(x), re.findall(r'\d+',line)))))for line in txt[1])

    total = 0

    for p in parts:
        print(f"Current part : {p}")
        wf = "in" #current workflow
        result = rule_valid(workflows[wf][0],p)
        
        while result is None or result not in "AR":
            r = 0 #rule index
            result = rule_valid(workflows[wf][r],p)
            while result is None:
                r += 1
                result = rule_valid(workflows[wf][r],p)
                
            if result not in "AR":
                wf = result
                
        if result == "R":
            continue
        elif result == "A":
            total += sum(p.values())
            continue
        
    print(total)

def part2(input_name: str) -> int:
    txt = get_txt_array(input_name)
    txt = [list(g) for key, g in groupby(txt, bool) if g != [""]]
    txt.pop(1)
    
    workflows = dict((key, value) for key, value in zip([line.split("{")[0] for line in txt[0]], [line.split("{")[1][:-1].split(",") for line in txt[0]]))
    count = 0

    stack = [(1,4000, 1,4000, 1,4000, 1,4000, "in")]
    
    while stack:
        #print(f"\nStack before pop : {stack}")
        rule_i = 0
        a_x, b_x, a_m, b_m, a_a, b_a, a_s, b_s, wf = stack.pop()
        #print(f"Stack after pop : {stack}")
        
        if wf == "R":
            continue
        elif wf == "A":
            count += (b_x-a_x+1) * (b_m-a_m+1) * (b_a-a_a+1) * (b_s-a_s+1)
            continue
            
        res = range_valid(workflows[wf][rule_i],(a_x,b_x),(a_m,b_m),(a_a,b_a),(a_s,b_s))
        while res[-1][-1] is None:
            rule_i += 1
            a_x, b_x, a_m, b_m, a_a, b_a, a_s, b_s, _ = res.pop()
            rb = range_valid(workflows[wf][rule_i],(a_x,b_x),(a_m,b_m),(a_a,b_a),(a_s,b_s))
            for n in rb:
                res.append(n)

        
        for r in res:
            stack.append(r)
    print(count)
    
part2("inputs/19-input.txt")

    

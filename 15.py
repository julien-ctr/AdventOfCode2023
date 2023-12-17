import re
from typing import *
from copy import deepcopy

def read_data(input_name: str) -> str:
    with open(input_name,'r') as f:
        return f.read().split(',')

def hash_txt(s: str) -> int:
    x = 0
    for char in s:
        x = ((x + ord(char))*17)%256
    return x

def part1(input_name: str): 
    data = read_data(input_name)
    return sum(list(hash_txt(el) for el in data))
        

def part2(input_name: str): 
    data = read_data(input_name)
    total = 0
    boxes =[[] for _ in range(256)]
    
    for el in data:
        txt = re.findall(r'^[a-zA-Z]+',el)[0]
        h = hash_txt(txt)
    
    
        if txt in [x[0] for x in boxes[h]]: #If already in, either remove or change value 
            index = [x[0] for x in boxes[h]].index(txt)
            if el[len(txt)]=="-":
                boxes[h].pop(index)
            else:
                boxes[h][index][1] = el.split('=')[-1]
                
        elif el[len(txt)]=="=": #If not in and wanting to add, then add
            boxes[h].append([txt,el.split('=')[-1]])
    
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            total += (i+1)*(j+1)*int(lens[1])
        
    return total
        
print(part2("15-input.txt"))

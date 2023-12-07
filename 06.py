import re
import time
from typing import *

def get_txt_array(input: str) -> List[str]:
    with open(input,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def part1(input: str) -> int :
    txt = get_txt_array(input)
    times = list(map(lambda x: int(x),re.findall(r"(\d+)",txt[0].split(':')[1])))
    distances = list(map(lambda x: int(x),re.findall(r"(\d+)",txt[1].split(':')[1])))
    better_ways = [0 for _ in range(len(times))]
    score = 1

    for race in range(len(times)):
        for x in range(times[race]+1):
            if x * (times[race]-x) > distances[race]:
                better_ways[race] += 1

    for n in better_ways:
        score *= n

    return score

def part2(input: str) -> int :
    txt = get_txt_array(input)
    times = int(''.join(re.findall(r"(\d+)",txt[0].split(':')[1])))
    distances = int(''.join(re.findall(r"(\d+)",txt[1].split(':')[1])))
    better_ways = 0

    for x in range(times+1):
        #if x % 1000000 == 0:
            #print(f"Iteration {x}. {100*(x/times)}%")
        if x * (times-x) > distances:
            better_ways += 1

    return better_ways

def part2bis(input: str) -> int :
    """
    This solution using upper and lower bounds with while loops
    appears to be about 3 times more time efficient than part2()
    """
    
    txt = get_txt_array(input)
    times = int(''.join(re.findall(r"(\d+)",txt[0].split(':')[1])))
    distances = int(''.join(re.findall(r"(\d+)",txt[1].split(':')[1])))
    better_ways = 0
    i = 0
    j = times

    while i < j and i * (times-i) < distances:
        i += 1

    while i < j and j * (times-j) < distances:
        j -= 1

    return j-i+1

start = time.time()
a = part2bis("06-input.txt")
end = time.time()
print(f"{a} (found in {end-start} seconds)")

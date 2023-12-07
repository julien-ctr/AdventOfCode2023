import re
import time
from typing import *

def get_txt_array(input: str) -> List[str]:
    with open(input,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def is_in_range(n: int, l: List) -> int | None:
    """
    Returns whether n in in the range specified by l.
    If so, returns the value at which it stands
    If not, returns None
    """
    if l[1] <= n and n < l[1]+l[2]:
        return l[0] + n-l[1]
    return None

def part1(input: str, debug = False) -> int :
    txt = get_txt_array(input)
    seeds = list(map(lambda x: int(x), re.findall('(\d+)', txt[0])))

    txt2 = re.findall("([a-zA-Z-\s]+:\n(?:\d+\s\d+\s\d+\n)+)", '\n'.join(txt))
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temp = []
    temp_to_humidity = []
    humidity_to_loc = []

    target = [seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temp, temp_to_humidity, humidity_to_loc]
    itarget = 0

    for k in range(7):
        dest = target[itarget]
        x = list(map(lambda x: int(x), re.findall("(\d+)", txt2[k])))
        for i in range(0,len(x),3):
            dest.append(x[i:i+3])
        itarget+=1

    current_val = 0
    final_locations = []

    for seed in seeds:
        if debug:
            print(f"\n=========== SEED : {seed} ===========")

        current_val = seed
        itarget = 0

        for k in range(7):
            i = 0

            while i < len(target[itarget]) and is_in_range(current_val, target[itarget][i]) is None:
                i += 1

            if i != len(target[itarget]):
                current_val = is_in_range(current_val, target[itarget][i])
            if debug:
                print(f"After {itarget+1} mapping, current_value is now {current_val}. (i = {i})")

            itarget += 1

        final_locations.append(current_val)
    
    return(min(final_locations))

def part2(input: str, debug = False, progress = False) -> int :
    txt = get_txt_array(input)
    seeds = list(map(lambda x: int(x), re.findall('(\d+)', txt[0])))
    txt2 = re.findall("([a-zA-Z-\s]+:\n(?:\d+\s\d+\s\d+\n)+)", '\n'.join(txt))
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temp = []
    temp_to_humidity = []
    humidity_to_loc = []

    target = [seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temp, temp_to_humidity, humidity_to_loc]
    itarget = 0

    for k in range(7):
        dest = target[itarget]
        x = list(map(lambda x: int(x), re.findall("(\d+)", txt2[k])))
        for i in range(0,len(x),3):
            dest.append(x[i:i+3])
        itarget+=1
    
    if progress:
        start = time.time()
        c = 0
        remaining = 0
        for i,s in enumerate(seeds[1::2]):
            remaining += s

    current_val = 0
    min_final_location = -1
    
    for n, start_seed in enumerate(seeds[::2]):
        for seed in range(start_seed, start_seed+seeds[2*n+1]):
            
            if debug:
                print(f"\n=========== SEED : {seed} ===========")

            current_val = seed
            itarget = 0

            for k in range(7):
                i = 0

                while i < len(target[itarget]) and is_in_range(current_val, target[itarget][i]) is None:
                    i += 1

                if i != len(target[itarget]):
                    current_val = is_in_range(current_val, target[itarget][i])
                if debug:
                    print(f"After {itarget+1} mapping, current_value is now {current_val}. (i = {i})")

                itarget += 1

            if min_final_location == -1 or current_val < min_final_location:
                min_final_location = current_val

            if progress:
                c += 1
                if c % 1_000_000 == 0:
                    end = time.time()
                    print(f"{c} seeds checked. Only {remaining-c} left. ({100*(c/remaining)}%)")
                    print(f"Estimated remaining time : {(end-start) * ((remaining-c)/1_000_000)} seconds.")
                    print(f"Current minimum found : {min_final_location}")
                    start = end
                
    return(min_final_location)

print(part2("05-input.txt", progress = True))

import re
from typing import *
from itertools import groupby
from sympy import symbols, Eq, solve

def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def colineaire(v_1,v_2):
    i = 0
    while v_2[i] == 0:
        i += 1
    k = v_1[i] / v_2[i]
    
    return all([k*val2 == val1 for val1, val2 in zip(v_1,v_2)])

def get_intersection_coords(a_1, a_2, v_1, v_2) -> Tuple[int,int,int]:
    if colineaire(v_1,v_2):
        return None
    
    if (v_1[0]*v_2[1]-v_1[1]*v_2[0]) == 0:
        return None
 
    t2 = (v_1[0]*a_1[1]-v_1[0]*a_2[1]+v_1[1]*a_2[0]-v_1[1]*a_1[0])/(v_1[0]*v_2[1]-v_1[1]*v_2[0])
    t = (a_2[0] + t2*v_2[0] - a_1[0])/v_1[0]

    if t < 0 or t2 < 0:
        return None
        
    return tuple([c + t*d for c,d in zip(a_1,v_1)])
        
def part1(input_name: str) -> int:
    txt = get_txt_array(input_name)
    coords = [[int(v.replace(",","")) for v in line.split(" ")[:3]] for line in txt]
    velocities = [[int(v.replace(",","")) for v in line.split(" ")[4:] if v != ""] for line in txt]
    
    LOWER_BOUND = 200000000000000
    UPPER_BOUND = 400000000000000
    count = 0
    
    for i in range(len(coords)):
        asteroid_1_coords = coords[i][:2]
        asteroid_1_velocity = velocities[i][:2]
        for j in range(i+1,len(coords)):
            asteroid_2_coords = coords[j][:2]
            asteroid_2_velocity = velocities[j][:2]
            
            intersect = get_intersection_coords(asteroid_1_coords, asteroid_2_coords, asteroid_1_velocity, asteroid_2_velocity)
            if intersect is not None and all([LOWER_BOUND <= coord <= UPPER_BOUND for coord in intersect]):
                # ~ print(f"{i} ({asteroid_1_coords}, {asteroid_1_velocity}) crosses {j} ({asteroid_2_coords}, {asteroid_2_velocity}) at {intersect}")
                count += 1
    print(count)
    return count
    
def part2(input_name: str) -> int:
    txt = get_txt_array(input_name)
    coords = [[int(v.replace(",","")) for v in line.split(" ")[:3]] for line in txt]
    velocities = [[int(v.replace(",","")) for v in line.split(" ")[4:] if v != ""] for line in txt]
    
    num = 3 # 3 sets of 3 equations should be enough for 6 + num unknowns
    equations = []
    px, py, pz, pvx, pvy, pvz = symbols("px, py, pz, pvx, pvy, pvz") # Declare the projectile's coordinates and velocity as variables
    
    for coord, vel, i  in zip(coords[:num], velocities[:num], range(num)):
        x = coord[0]
        y = coord[1]
        z = coord[2]
        
        vx = vel[0]
        vy = vel[1]
        vz = vel[2]
        
        t = symbols(f"t{i}")
        
        #Add the equations for all 3 axes
        equations.append(Eq(x + t*vx, px + t*pvx))
        equations.append(Eq(y + t*vy, py + t*pvy))
        equations.append(Eq(z + t*vz, pz + t*pvz))
    
    #Solve the equations using sympy solve
    s = solve(equations)[0]
    print(s[px] + s[py] + s[pz])
    return s[px] + s[py] + s[pz]
    
part2("24-input.txt")


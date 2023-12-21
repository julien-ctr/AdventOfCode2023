import re
from typing import *
from itertools import groupby
from queue import Queue

def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()
        
def pgcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a
  
def ppcm(t : List) -> int:
    """
    Returns the LCM (PGCD in French) of an array of numbers
    """
    p = t[0]
    for v in t[1:]:
        p = (p*v)//pgcd(p,v)
    return p

def part1(input_name: str) -> int:
    txt = get_txt_array(input_name)
    senders = [line.split(" ")[0] for line in txt]
    receivers = [line.split('>')[1].strip().replace(" ","").split(",") for line in txt]
    d = dict((key, value) for key, value in zip(senders,receivers))
    instructions = Queue() # Tuples (Destination, source, signal (0 -> low, 1 -> high))
    flip_flops = dict((key[1:], 0) for key in senders if key[0] == "%")
    conjunctions = dict((key[1:], {}) for key in senders if key[0] == "&")
    PUSH_BUTTON = 1000
    
    for s, rs in zip(senders, receivers):
        for r in rs:
            if r in conjunctions:
                conjunctions[r][s[1:]] = 0
                
    low_count = 0
    high_count = 0
    
    for k in range(PUSH_BUTTON):
        instructions.put(("broadcaster","button",0)) #Push the button
        while not instructions.empty():
            dest, src, signal = instructions.get()
            
            if signal == 0:
                low_count += 1
            else:
                high_count += 1
                
            if dest in flip_flops:
                if signal == 1:
                    continue
                else:
                    new_level = (flip_flops[dest]+1)%2
                    flip_flops[dest] = new_level
                    for el in d["%"+dest]:
                        instructions.put((el,dest,new_level))
            
            elif dest in conjunctions:
                conjunctions[dest][src] = signal
                
                if all(v == 1 for v in conjunctions[dest].values()):
                    new_signal = 0
                else:
                    new_signal = 1
                    
                for el in d["&"+dest]:
                    instructions.put((el,dest,new_signal))
                
                
            elif dest == "broadcaster":
                for el in d[dest]:
                    instructions.put((el,dest,signal))

    return low_count*high_count

def part2(input_name: str) -> int:
    """
    For clarity's sake, let's call final_conjunction the conjunction that sends the signal to rx. 
    Find the first number of button pushes after which each of the inputs of the final_conjunction
    sent a high signal as their last one, and return the lcm of these numbers.
    """
    
    txt = get_txt_array(input_name)
    senders = [line.split(" ")[0] for line in txt]
    receivers = [line.split('>')[1].strip().replace(" ","").split(",") for line in txt]
    d = dict((key, value) for key, value in zip(senders,receivers))
    instructions = Queue() # Tuples (Destination, source, signal (0 -> low, 1 -> high))
    flip_flops = dict((key[1:], 0) for key in senders if key[0] == "%")
    conjunctions = dict((key[1:], {}) for key in senders if key[0] == "&")
    
    for s, rs in zip(senders, receivers):
        for r in rs:
            if r in conjunctions:
                conjunctions[r][s[1:]] = 0
            if r == "rx":
                final_conjunction = s[1:]
            
    final_conj_inputs = dict((key, 0) for key in conjunctions[final_conjunction].keys())
        
    k = 0
    while any(v == 0 for v in final_conj_inputs.values()):
        k += 1
        instructions.put(("broadcaster","button",0)) #Push the button
        while not instructions.empty():
            dest, src, signal = instructions.get()
                            
            if dest in flip_flops:
                if signal == 1:
                    continue
                else:
                    new_level = (flip_flops[dest]+1)%2
                    flip_flops[dest] = new_level
                    for el in d["%"+dest]:
                        instructions.put((el,dest,new_level))
            
            elif dest in conjunctions:
                conjunctions[dest][src] = signal
                
                if all(v == 1 for v in conjunctions[dest].values()):
                    new_signal = 0
                else:
                    new_signal = 1
                    
                for el in d["&"+dest]:
                    instructions.put((el,dest,new_signal))
                
                if dest == final_conjunction:
                    for f in final_conj_inputs.keys():
                        if conjunctions[final_conjunction][f] == 1 and final_conj_inputs[f] == 0:
                            final_conj_inputs[f] = k
                
            elif dest == "broadcaster":
                for el in d[dest]:
                    instructions.put((el,dest,signal))

    return ppcm(list(final_conj_inputs.values()))

print(f"{part2('20-input.txt'):,}")

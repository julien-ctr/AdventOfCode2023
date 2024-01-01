import re
import time
from typing import *

def get_txt_array(input: str) -> List[str]:
    with open(input,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def get_hand_value(h: str, jokers = False) -> int:
    if not jokers:
        five = re.compile(r"(.)\1{4}")
        four = re.compile(r"(.)(?:.*\1){3}")
        #full_house = re.compile(r"^(.)\1{0,2}([^\1])\1*\2+\1*\2+$")
        three = re.compile(r"(.)(?:.*\1){2}")
        pair = re.compile(r"(.).*\1")
        #high_card = re.compile(r"^(.)([^\1])([^\1\2])([^\1\2\3])([^\1\2\3\4])$")
    else:
        five = re.compile(r"^J*(.)(?:\1*J*)*$")
        four = re.compile(r"(.)(?:(?:[^J\1]*)(?:\1|J)){3,}.*$")
        #full_house = re.compile(r"^(.)\1{0,2}([^\1])\1*\2+\1*\2+$")
        three = re.compile(r"(.)(?:(?:[^J\1]*)(?:\1|J)){2,}.*$")
        pair = re.compile(r"(.)(?:(?:[^J\1]*)(?:\1|J)).*$")
        #high_card = re.compile(r"^(.)([^\1])([^\1\2])([^\1\2\3])([^\1\2\3\4])$")
        
        #Move jokers to the end to allow patterns to match
        if "J" in h:
            n = h.count("J")
            h = h.replace('J', '') + n*"J"
        
    if five.search(h):
        return 7
    elif four.search(h):
        return 6
    elif three.search(h):
        h = h.replace('J', three.search(h).group(1))
        h = h.replace(three.search(h).group(1), '')
        if pair.search(h): #Three of a kind + pair = Full House
            return 5
        else:
            return 4
    elif pair.search(h):
        h = h.replace('J', pair.search(h).group(1))
        h = h.replace(pair.search(h).group(1), '')
        if pair.search(h): #Pair + Pair = Two pairs
            return 3
        else:
            return 2
    else: #Nothing found : High Card
        return 1

def order_draws(hands : List[int]) -> List[int]:
    d = {'A': 14,
         'K': 13,
         'Q': 12,
         'J': 11,
         'T': 10,
         '9': 9,
         '8': 8,
         '7': 7,
         '6': 6,
         '5': 5,
         '4': 4,
         '3': 3,
         '2': 2,
         'J': 1}
    
    num_hands  = [[] for _ in range(len(hands))]
    indexes = [n for n in range(len(hands))]
    
    for i, hand in enumerate(hands):
        for char in hand:
            num_hands[i].append(d[char])
    
    indexes.sort(key = lambda x : num_hands[x])
    return indexes
    
def solve(input: str, jokers:bool, debug: bool) -> List[str]:
    txt = get_txt_array(input)
    hands = [txt[i].split(' ')[0] for i in range(len(txt))]
    values = [txt[i].split(' ')[1] for i in range(len(txt))]
    scores = [0 for i in range(len(txt))]
    ranks = []
    result = 0
    
    for i, hand in enumerate(hands):
        scores[i] = get_hand_value(hand, jokers)
    
    if debug:
        names = {7: 'Five', 6: 'Four', 5: 'Full house', 4: 'Three', 3: 'Two pairs', 2: 'Pair', 1: 'High card'}
        for hand, score in zip(hands,scores):
            if "J" in hand:
                print(f"Hand {hand} is a {names[score]}")
        
    for s in range(1,8):
        t = []
        it = []
        for i, hand in enumerate(hands):
            if scores[i] == s:
                t.append(hand)
                it.append(i)
                
        for di in order_draws(t):
            ranks.append(values[it[di]])
                
    for i, v in enumerate(ranks):
        result += (i+1)*int(v)
        
    return result

start = time.time()

#Part 1
#print(solve('07-input.txt', jokers = False, debug = True))

#Part 2
print(solve('inputs/07-input.txt', jokers = True, debug = False))

end = time.time()

print(f"Solution found in {round(end-start,5)} seconds")

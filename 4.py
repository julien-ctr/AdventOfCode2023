from typing import *
import re

def build_txt_array(input_file: str) -> List[str]:
    with open(input_file, "r", encoding = "utf-8") as f:
        return f.read().splitlines()
        
def part1(input_file: str) -> int:
    
    t = build_txt_array(input_file)
    winning_numbers = [re.findall(r"(\b\d+\b)" , line.split(':')[1:][0].split('|')[0]) for line in t]
    played_numbers = [re.findall(r"(\b\d+\b)" , line.split('|')[1]) for line in t]
    scores = [-1 for _ in range(len(t))]
    score = 0
    
    for line in range(len(t)):
        for number in played_numbers[line]:
            if number in winning_numbers[line]:
                scores[line] += 1
                
    for s in scores:
        if s != -1:
            score += 2**s
    
    return score

def part2(input_file: str) -> int:
    
    t = build_txt_array(input_file)
    winning_numbers = [re.findall(r"(\b\d+\b)" , line.split(':')[1:][0].split('|')[0]) for line in t]
    played_numbers = [re.findall(r"(\b\d+\b)" , line.split('|')[1]) for line in t]
    count = [1 for _ in range(len(t))]
    scores = [0 for _ in range(len(t))]
    
    for line in range(len(t)):
        for number in played_numbers[line]:
            if number in winning_numbers[line]:
                scores[line] += 1
        for i in range(scores[line]):
            count[line+i+1] += count[line]

    return sum(count)

if __name__ == "__main__":
    print(part2("4-input.txt"))

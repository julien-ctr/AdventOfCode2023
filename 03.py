from typing import *

def is_symbol(c: str) -> bool:
    return c != '.' and not c.isnumeric()

def is_gear(c: str) -> bool:
    return c == "*"

def scan_number(y: int, x: int, txt: str) -> int:
    res = ''
    
    i, j = (x, x)
    
    #while we have a number on the left, go more on the left
    while i > 0 and txt[y][i].isnumeric():
        i -= 1
    
    #while we have a number on the right, go more on the right
    while j < len(txt[0]) and txt[y][j].isnumeric():
        j += 1

    #Increase i / decrease j if necessary to get back to the first / last numeral
    if i == -1 or not txt[y][i].isnumeric():
        i += 1
    if j == len(txt[y]) or not txt[y][j].isnumeric():
        j -= 1    
    
    #build a string of the full number
    for c in range(i,j+1):
        res += txt[y][c]
        txt[y] = txt[y][:c] + '.' + txt[y][c+1:] #replace the numeral with a dot so it's not counter again afterwards
    
    return int(res)

def build_txt_array(input_file: str) -> List[str]:
    with open(input_file, "r", encoding = "utf-8") as f:
        return f.read().splitlines()

def part1(input_file: str) -> int:
    s = 0
    txt_mat = build_txt_array(input_file)
            
    #Reads the array 
    for line in range(len(txt_mat)):
        for char in range(len(txt_mat[0])):
            if is_symbol(txt_mat[line][char]): #if a symbol is found, scan its nearby chars
                for y in range(max(0,line-1), min(len(txt_mat), line+2),1):
                    for x in range(max(0,char-1), min(len(txt_mat[line]),char+2), 1):
                        if txt_mat[y][x].isnumeric(): #if a number is found, scan the area to get the whole number
                            s += scan_number(y, x, txt_mat)
                            
    return s

def part2(input_file: str) -> int:
    s = 0
    txt_mat = txt_mat = build_txt_array(input_file)
        
    #Reads the array
    for line in range(len(txt_mat)):
        for char in range(len(txt_mat[0])):
            if is_gear(txt_mat[line][char]):
                gear_numbers = []
                for y in range(max(0,line-1), min(len(txt_mat), line+2),1):
                    for x in range(max(0,char-1), min(len(txt_mat[line]),char+2), 1):
                        if txt_mat[y][x].isnumeric():
                            gear_numbers.append(scan_number(y,x,txt_mat))
                if len(gear_numbers) > 1:
                    m = 1
                    for num in gear_numbers:
                        m *= num
                    s += m
    return s
    
print(part2("inputs/03-input.txt"))

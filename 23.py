from __future__ import annotations
from typing import *
from queue import Queue
import time

class Graph():
    def __init__(self, nodes = None):
        if not nodes:
            nodes = []
        self.nodes = dict((key, value) for key, value in [(node.n, node) for node in nodes])

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node.n] = node
    
    def add_neigh(self, node_1, node_2, weight, reciprocal = True):
        n1, n2 = self.get_node(node_1), self.get_node(node_2)
        if n2.n not in [v[0] for v in n1.neighbours]:
            n1.neighbours.append((n2.n,weight))
        if reciprocal and n1.n not in [v[0] for v in n2.neighbours]:
            n2.neighbours.append((n1.n,weight))
                
    def get_node(self, label):
        return self.nodes[label]
    
    def __str__(self):
        s = ""
        for node in self.nodes.values():
            s += f"{node.n} | Neighbours : {node.neighbours}\n" 
        return s
    
    def __len__(self) -> int:
        return len(self.nodes)
    
class Node():
    def __init__(self, label):
        self.n = label
        self.neighbours = []
        
    def __str__(self):
        return self.n
            
def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def is_crossing(grid, row, col) -> bool:
    if (row,col) == (0,1) or (row,col) == (max([v[0] for v in grid.keys()]), max([v[1] for v in grid.keys()])-1):
        return True
    
    count = 0
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        if grid.get((row+dr, col+dc), "#") != "#":
            count += 1    
    return count >= 3

def part1(input_name: str) -> int:
    txt = get_txt_array(input_name)
    width, height = len(txt[0]), len(txt)

    grid = {}
    for row in range(height):
        for col in range(width):
            grid[(row,col)] = txt[row][col]
    
    start = (0,1)
    end = (height-1, width-2)
    stack = [(start, tuple([start]), 0)]
    max_path = (0, ())

    while stack:
        current, visited, count = stack.pop()
        
        if current == end and count > max_path[0]:
            max_path = (count, visited)
            
        visited += (current,)

        for dr, dc, char in [(1, 0, "^"), (-1, 0, "v"), (0, 1, "<"), (0, -1, ">")]:
            new_pos = (current[0] + dr, current[1] + dc)
            if grid.get(new_pos, "#") not in "#" + char and new_pos not in visited:
                stack.append((new_pos, visited, count + 1))
    
def part2(input_name: str) -> int:
    txt = get_txt_array(input_name)
    width, height = len(txt[0]), len(txt)
    
    grid = {}
    for row in range(height):
        for col in range(width):
            grid[(row,col)] = txt[row][col]
            
    start = "0_1"
    end = f"{height-1}_{width-2}"
    
    q = Queue()
    q.put(((0,1), 0, start, tuple()))
    graph = Graph()
    graph.add_node(Node(start))
    visited_intersections = set()
    
    #1- Create graph
    while not q.empty():
        current, count, actual_node, visited = q.get()
        current_label = f"{current[0]}_{current[1]}"
            
        if is_crossing(grid, current[0], current[1]):
            if current_label not in graph.nodes:
                print(f"Node {current_label} added to the graph ({len(graph)})")
                graph.add_node(Node(current_label))
                
            graph.add_neigh(actual_node,current_label, weight = count)
            count = 0
            actual_node = current_label
            
            if current in visited_intersections:
                continue
                
            visited_intersections.add(current)
            
        visited += (current,)
        
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (current[0] + dr, current[1] + dc)
            if grid.get(new_pos, "#") != "#" and new_pos not in visited:
                q.put((new_pos, count + 1, actual_node, visited))
    
    #2- Search longest path
    max_path = (0, ())
    stack = [("0_1", 0, tuple())]
    i = 0
    while stack:
        i += 1
        if i % 100_000 == 0:
            print(f"Iteration {i}, still going on. Current max : {max_path[0]}", end = "\r")
        
        current, dist, visited = stack.pop()
        if current == end and dist > max_path[0]:
            max_path = (dist, visited)
            
        visited += (current,)

        for neighbour in graph.get_node(current).neighbours:
            neigh_label, neigh_dist = neighbour
            if neigh_label not in visited:
                stack.append((neigh_label, dist + neigh_dist, visited))
    
    print(max_path)
    return max_path[0]
    
start = time.time()
part2("inputs/23-input.txt")
end = time.time()
print(f"Found in {round(end-start,2)} seconds")
    

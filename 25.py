from __future__ import annotations
from typing import *
import time
from random import choice

class Graph():
    def __init__(self, nodes = None):
        if not nodes:
            nodes = []
        self.nodes = dict((key, value) for key, value in [(node.n, node) for node in nodes])

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node.n] = node
    
    def add_neigh(self, node_1, node_2, weight = 1, reciprocal = True):
        n1, n2 = self.get_node(node_1), self.get_node(node_2)
        n1.neighbours.append((n2.n,weight))
        n2.neighbours.append((n1.n,weight))
                
    def get_node(self, label):
        return self.nodes[label]
    
    def merge_nodes(self, n1, n2):
        n1 = self.get_node(n1)
        n2 = self.get_node(n2)
        
        #Remove the link between the two nodes
        n2.neighbours.remove((n1.n,1))
        n1.neighbours.remove((n2.n,1))
        
        for neigh in n2.neighbours:
            if neigh[0] != n1.n:
                self.add_neigh(n1.n,neigh[0])
            self.get_node(neigh[0]).neighbours.remove((n2.n,1))
            
        n1.value += n2.value
        del self.nodes[n2.n]
        
    def __str__(self):
        s = ""
        for node in self.nodes.values():
            s += f"{node}\n" 
        return s
    
    def __len__(self) -> int:
        return len(self.nodes)
    
class Node():
    def __init__(self, label):
        self.n = label
        self.neighbours = []
        self.value = 1
        
    def __str__(self):
        return f"{self.n} | Neighbours : {self.neighbours} | val = {self.value}" 
            
def get_txt_array(input_name: str) -> List[str]:
    with open(input_name,'r',encoding = 'utf-8') as f:
        return f.read().splitlines()

def part1(input_name: str) -> int:
    """
    Karger's algorithm :
    Probabilistic approach to find the minimal cut of a graph
    We know that we can find a cut of 3 edges so that's what we aim for
    """
    c = 0
    txt = get_txt_array(input_name)
    graph = Graph()
    while all([len(v.neighbours) != 3 for v in graph.nodes.values()]):
        c += 1
        
        # Step 1 : create the graph
        graph = Graph()
        for line in txt:
            node = Node(line.split(":")[0])
            if node.n not in graph.nodes:
                graph.add_node(node)
            for neigh in line.split(" ")[1:]:
                if neigh not in graph.nodes:
                    graph.add_node(Node(neigh))
                graph.add_neigh(node.n, neigh)
        
        # Step 2 : Contract the graph until two nodes are remaining
        for k in range(len(graph)-2):
            node_a = choice(list(graph.nodes.keys()))
            node_b = choice([neigh[0] for neigh in graph.get_node(node_a).neighbours])
            graph.merge_nodes(node_a,node_b)
        
    print(graph)
    
    result = 1
    
    for k, v in graph.nodes.items():
        print(k, v.value)
        result *= v.value
        
    print(f"Result : {result} (found after {c} trials)")
    return result
        

start = time.time()
part1('inputs/25-input.txt')
end = time.time()
print(f"Solution found in {round(end-start,2)} seconds")

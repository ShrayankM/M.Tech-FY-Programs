import helper as h
import numpy as np

def check_current_solution(graph, assigned):
    for i in range(0, h.NODES):
        for neigh in graph.adjacency_list[i]:
            if assigned[i] == assigned[neigh]:
                return False
    return True

def find_conflicting_node(graph, assigned):
    conflicts = list()

    for i in range(0, h.NODES):
        for neigh in graph.adjacency_list[i]:
            if assigned[i] == assigned[neigh]:
                conflicts.append(i)
                break
    
    random_node = conflicts[np.random.randint(0, len(conflicts))]
    return random_node

def find_conflicts(graph, assigned, node, color):
    assigned[node] = color

    cnt = 0
    for neigh in graph.adjacency_list[node]:
        if assigned[node] == assigned[neigh]:
            cnt = cnt + 1
    return cnt

def local_search(graph, assigned, max_steps):
    for i in range(0, h.NODES):
        assigned[i] = np.random.randint(0, h.COLORS)
    
    for i in range(0, max_steps):
        if (check_current_solution(graph, assigned)):
            return assigned
        
        node = find_conflicting_node(graph, assigned)
    
        min_conflicts = h.sys.maxsize
        current_color = 0
        for i in range(0, h.COLORS):
            if i != assigned[node]:
                conflicts = find_conflicts(graph, assigned, node, i)

                if conflicts < min_conflicts:
                    min_conflicts = conflicts
                    current_color = i
        assigned[node] = current_color
    return assigned
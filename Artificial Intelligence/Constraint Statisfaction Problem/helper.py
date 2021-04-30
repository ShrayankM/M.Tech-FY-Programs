import sys

NODES = 7
COLORS = 3

#* Initial Color Matrix
color_matrix = [[1 for i in range(0, COLORS)] for j in range(0, NODES)]

class Edge:
    def __init__(self, i, j):
        self.source = i
        self.destination = j

class Graph:
    def __init__(self, edges):
        self.adjacency_list = [[] for i in range(0, NODES)]
        for edge in edges:
            self.adjacency_list[edge.source].append(edge.destination)
            self.adjacency_list[edge.destination].append(edge.source)

    def __str__(self):
        output = ""
        for i in range(0, len(self.adjacency_list)):
            output += "Node " + str(i) + " -> " + str(self.adjacency_list[i]) + "\n";
        return output


def select_node(graph, assigned):
    ans = list()
    max_value = 0
    min_color = 999999

    for i in range(0, NODES):
        value = len(graph.adjacency_list[i])

        #* Get the values with min possible colors and max neighbours
        allowed = sum(color_matrix[i])
        
        if min_color > allowed and assigned[i] == -1:
            min_color = allowed
        
        if value > max_value and assigned[i] == -1:
            max_value = value
    
    for i in range(0, NODES):
        allowed = sum(color_matrix[i])
        if (allowed == min_color and assigned[i] == -1):
            ans.append(i)
    
    if len(ans) == 1:
        return ans[0]
    
    for i in range(0, NODES):
        if max_value == len(graph.adjacency_list[i]) and assigned[i] == -1:
            return i


def select_color(graph, node, color, assigned):
    s = 0
    values = list()

    #* Check if node has any avaliable color choices
    if (sum(color_matrix[node]) == 0): return -1

    for i in range(0, COLORS):
        for adj in graph.adjacency_list[node]:

            if assigned[adj] == -1:
                s += sum(color_matrix[adj])
            
            if color_matrix[adj][i] == 1 and assigned[adj] == -1:
                s = s - 1
        values.append([s, i])
        s = 0
    values = sorted(values)

    if color < len(values):
        return values[color][1]
    
    return -1

def add_forward(graph, node, color_value):
    for neigh in graph.adjacency_list[node]:
        color_matrix[neigh][color_value] = 0

def revert_forward(color_value, temp):
    for i in range(0, NODES):
        color_matrix[i][color_value] = temp[i]

def check_forward(graph, node, color_value):
    for neigh in graph.adjacency_list[node]:
        color_matrix[neigh][color_value] = 0
        if (sum(color_matrix[neigh]) == 0): return False
    return True

def check_consistency(graph, node, color_value, assigned):
    for neigh in graph.adjacency_list[node]:
        if assigned[neigh] == color_value:
            return False
    return True

def revise(xi, xj):
    revisied = False
    remove = True

    for i in range(0, COLORS):
        if color_matrix[xi][i] == 1:
            for j in range(0, COLORS):
                if color_matrix[xj][j] == 1 and i != j:
                    remove = False
                    break
            if remove:
                color_matrix[xi][i] = 0
                revisied = True
    return revisied

def AC3(graph, assigned, node):
    ac3_queue = list()

    for neigh in graph.adjacency_list[node]:
        ac3_queue.append((neigh, node))
    
    while (len(ac3_queue) != 0):
        popped = ac3_queue.pop(0)

        xi = popped[0]
        xj = popped[1]

        if (revise(xi, xj)):
            if sum(color_matrix[xi]) == 0:
                return False
            
            for neigh in graph.adjacency_list[xi]:
                if assigned[neigh] == -1 and neigh != xj:
                    ac3_queue.append((neigh, xi))
    return True

def revert_inference_ac3(temp):
    for i in range(0, NODES):
        color_matrix[i] = temp[i]


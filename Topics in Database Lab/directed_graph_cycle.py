import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import planar_drawing
from networkx.drawing.layout import planar_layout

class DiGraph:
    def __init__(self, vertices):
        self.adj_list = [set() for i in range(vertices)]
        self.vertices = vertices
    
    def add_edge(self, a, b):
        self.adj_list[a].add(b)
    
    def V(self):
        return self.vertices
    
    def adj(self, vertex):
        return list(self.adj_list[vertex])
    
    def create_graph(self, instrus_cnt, instrus):
        for i in range(instrus_cnt):
            for j in range(i + 1, instrus_cnt):
                t1 = instrus[i];
                t2 = instrus[j];

                if (t1[1] == t2[1]): continue
                if t1[-1] == t2[-1] and (t1[-2] == 'W' or t2[-2] == 'W'):
                    self.add_edge(int(t1[1]), int(t2[1]));
    
    def view_graph(self):
        for vertex in range(self.V()):
            print(vertex, ' = ', self.adj(vertex))


class DirectedCycle:
    def __init__(self, graph):
        self.visited = [False for i in range(graph.V())]
        self.on_stack = [False for i in range(graph.V())]
        self.cycle = None
        self.edge_to =  [-1 for i in range(graph.V())]

        for vertex in range(graph.V()):
            if (not self.visited[vertex]): 
                self.dfs(graph, vertex)
    
    def dfs(self, graph, v):
        self.on_stack[v] = True
        self.visited[v] = True

        for w in graph.adj(v):
            if (self.cycle): return
            if (not self.visited[w]):
                self.edge_to[w] = v
                self.dfs(graph, w)
            elif (self.on_stack[w]):
                self.cycle = list()
                x = v
                while (x != w):
                    self.cycle.append(x)
                    x = self.edge_to[x]
                self.cycle.append(w)
                self.cycle.append(v)
        self.on_stack[v] = False

    def has_cycle(self):
        return self.cycle != None
    
    def get_cycle(self):
        return self.cycle

def show_graph(cycle, graph, flag):
    G = nx.DiGraph()
    edges = []
    for v in range(graph.V()):
        neighbs = graph.adj(v)
        for w in neighbs:
            temp = (v, w)
            edges.append(temp)
    # print(edges)

    G.add_edges_from(edges)
    pos = nx.circular_layout(G)
    plt.figure(figsize=(7, 7))

    #* Normal Nodes
    nx.draw_networkx_nodes(G, pos, nodelist=[v for v in range(graph.V())], node_size=500, node_color='orange')

    #* Cycle Nodes
    if (flag):
        nx.draw_networkx_nodes(G, pos, nodelist=cycle, node_size=500, node_color='green')

    if (flag):
        start = 1
        N = len(cycle)
        cycle_edges = []

        while start > 0:
            cycle_edges.append((cycle[start - 1], cycle[start]))
            start = (start + 1) % N
    
    #* Normal Edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), connectionstyle='arc3, rad=0.09', edge_color='black', arrowstyle='-|>')

    #* Cycle Edges
    if (flag):
        nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, connectionstyle='arc3, rad=0.09', edge_color='blue', arrowstyle='-|>')

    node_labels = dict()

    for node in range(graph.V()):
        node_labels[node] = 'T'+str(node)
    
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

    if (flag):
        cycle_labels = dict()
        for edge in cycle_edges:
            cycle_labels[edge] = 'LOOP'
    
    # print(cycle_labels)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=cycle_labels)
    plt.show()


file = open("transaction_input.txt", "r");
data = []
for line in file:
    data.append(line.strip());

[transactionCnt, instructionCnt] = [int(data[0][0]), int(data[0][2])];
instructions = data[1:];

graph = DiGraph(transactionCnt);
graph.create_graph(instructionCnt, instructions);

# graph.view_graph()

di_cycle = DirectedCycle(graph)

if (di_cycle.has_cycle()):
    cycle = di_cycle.get_cycle()[::-1]
    show_graph(cycle, graph, True)
    print("Not Conflict Serializable");
else:
    show_graph([], graph, False)
    print("Conflict Serializable");


# 3 8
# T0RA
# T1WA
# T2RB
# T1WB
# T0WB
# T1RB
# T0RA
# T2RA

# 3 9
# T0RX
# T2RZ
# T2WZ
# T1RY
# T0RY
# T1WY
# T2WX
# T1WZ
# T0WX

# 3 8
# T0RX
# T1RY
# T2RY
# T1WY
# T0WX
# T2WX
# T1RX
# T1WX

# 3 6
# T0RA
# T1WA
# T1RA
# T2RA
# T2WB
# T0RB

# 4 7
# T3RA
# T1RA
# T2RA
# T0WB
# T1WA
# T2RB
# T1WB

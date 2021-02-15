import networkx as nx
import matplotlib.pyplot as plt

class DiGraph:
    def __init__(self, vertices):
        self.adjList = [set() for i in range(vertices)]
        self.visited = [False for i in range(vertices)]
        self.vertices = vertices
        self.hasCycle = False
    
    def addEdge(self, a, b):
        self.adjList[a].add(b)
    
    def adj(self, v):
        return list(self.adjList[v]);
    
    def V(self):
        return self.vertices;
    
    def generateGraph(self, instruCnt, instrus):
        for i in range(instruCnt):
            for j in range(i + 1, instruCnt):
                t1 = instrus[i];
                t2 = instrus[j];

                if (t1[1] == t2[1]): continue
                if t1[-1] == t2[-1] and (t1[-2] == 'W' or t2[-2] == 'W'):
                    self.addEdge(int(t1[1]), int(t2[1]));
    
    def dfs(self, vertex, source):
        self.visited[vertex] = True;
        neighbours = self.adj(vertex);

        for v in neighbours:
            if (not self.visited[v]):
                self.dfs(v, source);
            elif v == source: self.hasCycle = True;
            
    def detectCycle(self):
        for i in range(self.vertices):
            if (not self.visited[i]):
                self.dfs(i, i);
        return self.hasCycle;
    
    def createEdgeList(self, graph):
        edgeList = [];
        cnt = 0;
        for i in range(self.vertices):
            adj = self.adj(i);
            for j in adj:
                # edgeList.append(tuple([i, j]));
                graph.add_edge(i, j, key = cnt);
                cnt = cnt + 1;
        return graph;


file = open("transaction_input.txt", "r");
data = []
for line in file:
    data.append(line.strip());

[transactionCnt, instructionCnt] = [int(data[0][0]), int(data[0][2])];
instructions = data[1:];

print(instructions);
g = DiGraph(transactionCnt);
g.generateGraph(instructionCnt, instructions);

if g.detectCycle() == True:
    print("Not Conflict Serializable");
else:
    print("Conflict Serializable");


graph = nx.DiGraph();
graph.add_nodes_from([i for i in range(g.V())]);

# graph.add_edges_from(g.createEdgeList());
# print(g.createEdgeList());

graph = g.createEdgeList(graph);

plt.figure(figsize =(7, 4)) 
# nx.draw_networkx(graph, with_label = True, arrows = True, node_color ='orange')
nx.draw(graph, with_labels=True, arrows = True, connectionstyle='arc3, rad = 0.12', node_color='orange');

plt.show()



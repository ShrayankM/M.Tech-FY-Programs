
import helper as h
import simple_backtracking as sb
import forwardCheck_backtracking as fb
import local_search as ls
import ac_backtrack as ac
import networkx as nx
import matplotlib.pyplot as plt


def CSP_Search(graph, choice):
    assigned = [-1 for i in range(0, h.NODES)]
    if (choice == 0):
        #* Simple Backtracking
        return sb.simple_backtracking(graph, assigned)
    elif (choice == 1):
        #* Backtracking with forward checking
        return fb.forwardCheck_backtracking(graph, assigned)
    elif (choice  == 2):
        #* Simple Local Search
        max_steps = 100
        return ls.local_search(graph, assigned, max_steps) 
    elif (choice == 3):
        #* AC3 constraint check
        return ac.backtrack(graph, assigned)

if __name__ == "__main__":
    edges = [h.Edge(0, 1), h.Edge(0, 2), h.Edge(0, 3), 
             h.Edge(0, 4), h.Edge(0, 5), h.Edge(1, 2), 
             h.Edge(2, 3), h.Edge(3, 4), h.Edge(4, 5),
             h.Edge(4, 6)
    ]
    graph = h.Graph(edges)

    colors = CSP_Search(graph, 3)

    G = nx.DiGraph()

    edgeList = [(edge.source, edge.destination) for edge in edges]
    # for edge in edges:
    #     edgeList.append((edge.source, edge.destination))
    
    G.add_edges_from(edgeList)
    pos = nx.circular_layout(G)
    plt.figure(figsize = (7, 7))

    color_red = list()
    color_green = list()
    color_blue = list()

    for i in range(0, h.NODES):
        if colors[i] == 0: color_red.append(i)
        if colors[i] == 1: color_green.append(i)
        if colors[i] == 2: color_blue.append(i)

    nx.draw_networkx_nodes(G, pos, nodelist=color_red, node_size=500, node_color='red', node_shape='o')
    nx.draw_networkx_nodes(G, pos, nodelist=color_green, node_size=500, node_color='green', node_shape='o')
    nx.draw_networkx_nodes(G, pos, nodelist=color_blue, node_size=500, node_color='blue', node_shape='o')
    nx.draw_networkx_edges(G, pos, edgelist=list(G.edges()), edge_color='black', arrowstyle="-")
    nx.draw_networkx_labels(G, pos)
    plt.show()
    

    
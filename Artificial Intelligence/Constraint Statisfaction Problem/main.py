
import helper as h
import simple_backtracking as sb
import forwardCheck_backtracking as fb

def CSP_Search(graph, choice):
    assigned = [-1 for i in range(0, h.NODES)]
    if (choice == 0):
        #* Simple Backtracking
        return sb.simple_backtracking(graph, assigned)
    elif (choice == 1):
        #* Backtracking with forward checking
        return fb.forwardCheck_backtracking(graph, assigned)

if __name__ == "__main__":
    edges = [h.Edge(0, 1), h.Edge(0, 2), h.Edge(0, 3), 
             h.Edge(0, 4), h.Edge(0, 5), h.Edge(1, 2), 
             h.Edge(2, 3), h.Edge(3, 4), h.Edge(4, 5)
    ]
    graph = h.Graph(edges)

    colors = CSP_Search(graph, 1)
    print(colors)
    
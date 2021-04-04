from math import sqrt
import queue as q

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.fcost = 0
        self.parent = None
        self.hcost = 0
        self.gcost = 0
    
    def find_heuristic(self, goal):
        self.hcost = sqrt((goal.x - self.x) * (goal.x - self.x) + (goal.y - self.y) * (goal.y - self.y))
    
    def __gt__(self, other):
        return self.fcost > other.fcost
    
    def get_cost(self):
        return self.fcost
    
    def __str__(self):
        return self.id + " " + str(self.fcost) + " " + str(self.parent)

class Graph:
    def __init__(self, V):
        self.V = V
        self.edges = {}

        for i in range(1, V + 1):
            self.edges[str(i)] = list()
    
    def add_edge(self, i, j, cost):
        self.edges[i].append((j, cost))
        self.edges[j].append((i, cost))
    
    def get_neighbors(self, i):
        return self.edges[i]
    
    def show_graph(self):
        for i in range(1, self.V + 1):
            print("Node = " + str(i) + " List = " + str(self.edges[str(i)]))


def find_shortest_path(source, goal, graph, nodes):
    open_list = q.PriorityQueue()

    closed_check = {}
    open_check = {}
    
    open_list.put(source)
    open_check[source.id] = source.id

    while not open_list.empty():

        # print(open_check, closed_check)
        current_state = open_list.get()
        open_check.pop(current_state.id)
        if current_state.id == goal.id:
            print("Destination Reached")
            return  
        
        closed_check[current_state.id] = current_state.id 
        print("For Node = " + str(current_state.id))
        neighbors = graph.get_neighbors(current_state.id)
        for neigh in neighbors:
            id, cost = neigh
            if closed_check.get(id) != None:
                continue
            if open_check.get(id) == None:
                nodes[id].gcost = cost + nodes[current_state.id].gcost
                nodes[id].fcost = nodes[id].hcost + nodes[id].gcost
                nodes[id].parent = current_state.id
                open_check[id] = id
                open_list.put(nodes[id])
                print(nodes[id])
            else:
                if nodes[id].gcost > cost + nodes[current_state.id].gcost:
                    nodes[id].gcost = cost + nodes[current_state.id].gcost
                    nodes[id].fcost = nodes[id].hcost + nodes[id].gcost
                    nodes[id].parent = current_state.id
                    print(nodes[id])


    # while not open_list.empty():
    #     current_state = open_list.get()
    #     if current_state.id == goal.id:
    #         print("Destination Reached")
    #         return
        
    #     closed_check[current_state.id] = current_state.id
    #     print("For Node = " + str(current_state.id))
    #     neighbors = graph.get_neighbors(current_state.id)
    #     for neigh in neighbors:
    #         id, cost = neigh
    #         if closed_check.get(id) == None:
    #             nodes[id].gcost = cost + nodes[current_state.id].gcost
    #             nodes[id].fcost = nodes[id].hcost + nodes[id].gcost
    #             nodes[id].parent = current_state.id
    #             open_list.put(nodes[id])
    #             print(nodes[id])


if __name__ == "__main__":
    source = Node('1', 1, 1)
    goal = Node('8', 5, 5)

    nodes = {
        '1': Node('1', 1, 1),
        '2': Node('2', 2, 1),
        '3': Node('3', 3, 3),
        '4': Node('4', 1, 4),
        '5': Node('5', 4, 2),
        '6': Node('6', 3, 5),
        '7': Node('7', 5, 3),
        '8': Node('8', 5, 5),
    }

    for nid, node in nodes.items():
        node.find_heuristic(goal)
        # print(node.hcost)
    
    g = Graph(len(nodes))
    g.add_edge('1', '2', 3)
    g.add_edge('1', '3', 4)
    g.add_edge('1', '4', 2)
    g.add_edge('3', '5', 2)
    g.add_edge('3', '6', 5)
    g.add_edge('4', '6', 6)
    g.add_edge('5', '7', 6)
    # g.add_edge('5', '7', 1)
    g.add_edge('6', '7', 3)
    g.add_edge('7', '8', 4)

    # g.show_graph()

    source.gcost = 0
    source.fcost = source.gcost + source.hcost
    find_shortest_path(source, goal, g, nodes)

    start = goal.id
    cost = 0
    path = ''
    while start != source.id:
        path += start + " --> "
        start = nodes[start].parent
    path += source.id
    print(path)
        

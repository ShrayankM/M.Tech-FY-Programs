import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edges_from([ (0, 1), (0, 2), (2, 1), (3, 1)])

pos = nx.spring_layout(G)
plt.figure(figsize=(7, 7))

nx.draw_networkx_nodes(G, pos, nodelist=[0, 1], node_size=500, node_color='green', node_shape='h')
nx.draw_networkx_nodes(G, pos, nodelist=[2, 3], node_size=500, node_color='blue', node_shape='o')
nx.draw_networkx_edges(G, pos, edgelist=list(G.edges())[0:2], connectionstyle='arc3, rad=0.0', edge_color='black', arrowstyle='-|>')

nx.draw_networkx_edges(G, pos, edgelist=list(G.edges())[2:], connectionstyle='arc3, rad=0.0', edge_color='orange', arrowstyle='-|>')

nx.draw_networkx_edge_labels(G, pos, edge_labels={(0, 1): 'LOOP', (0, 2): 'LOOP'})
nx.draw_networkx_labels(G, pos)
plt.show()

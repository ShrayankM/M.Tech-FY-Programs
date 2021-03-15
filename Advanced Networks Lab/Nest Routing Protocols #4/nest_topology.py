import sys
from nest.experiment import *
from nest.topology import *
from nest.routing.ospf import *

#* Topology
#*  
#*  node_l_1 ----------|                                            | ------------------ node_r_1
#*                     |                                            |
#*  node_l_2 ----------|---- router_left ========= router_right ----|                                         
#*                     |                                            |
#*  node_l_3 ----------|                                            | ------------------ node_r_2
#*  


#********************* Creating Routers and Nodes ***********************#
nodes_left = []
nodes_right = []

router_left = Node("router_left")
router_right = Node("router_right")

router_left.enable_ip_forwarding()
router_right.enable_ip_forwarding()

#* Creating Left Nodes
for i in range(3):
    nodes_left.append(Node("node_l_" + str(i + 1)))

#* Creating Right Nodes
for i in range(2):
    nodes_right.append(Node("node_r_" + str(i + 1)))

#********************* Creating Interfaces(Connections) *****************#
left_interfaces = []
right_interfaces = []

#TODO Connecting left nodes to left router
for i in range(3):
    left_interfaces.append(connect(nodes_left[i], router_left))

#TODO Connecting right nodes to create ETHERNET
for i in range(2):
    right_interfaces.append(connect(nodes_right[i], router_right))

#TODO Connecting the routers
(router_left_connection, router_right_connection) = connect(router_left, router_right)

#********************* Assigning Addresses *****************#

left_subnet = Subnet("10.0.0.0/24")

#TODO For the left nodes
for i in range(3):
    left_interfaces[i][0].set_address(left_subnet.get_next_addr())
    left_interfaces[i][1].set_address(left_subnet.get_next_addr())

right_subnet = Subnet("10.0.1.0/24")

#TODO For the right nodes
for i in range(2):
    right_interfaces[i][0].set_address(right_subnet.get_next_addr())
    right_interfaces[i][1].set_address(right_subnet.get_next_addr())

router_subnet = Subnet("10.0.2.0/24")

router_left_connection.set_address(router_subnet.get_next_addr())
router_right_connection.set_address(router_subnet.get_next_addr())

#********************** Routing ****************************#

for i in range(3):
    nodes_left[i].add_route("DEFAULT", left_interfaces[i][0])
for i in range(3):
    router_left.add_route(left_interfaces[i][0].get_address(), left_interfaces[i][1])
router_left.add_route("DEFAULT", router_left_connection)

for i in range(2):
    nodes_right[i].add_route("DEFAULT", right_interfaces[i][0])
for i in range(2):
    router_right.add_route(right_interfaces[i][0].get_address(), right_interfaces[i][1])
router_right.add_route("DEFAULT", router_right_connection)

for i in range(3):
    left_interfaces[i][0].set_attributes("10mbit", "10ms")
    left_interfaces[i][1].set_attributes("10mbit", "10ms")

for i in range(2):
    right_interfaces[i][0].set_attributes("10mbit", "10ms")
    right_interfaces[i][1].set_attributes("10mbit", "10ms")

router_left_connection.set_attributes("50mbit", "10ms", "pie")
router_right_connection.set_attributes("50mbit", "10ms", "pie")

# print(router_left.id)
# print(router_right.id)

router_ids = [router_left.id, router_right.id]
router_interfaces = [router_left_connection, router_right_connection]

exp = Experiment("tcp-on-dumbell")

flow = Flow(nodes_left[0], nodes_right[1], right_interfaces[1][0].address, 0, 10, 2)

exp.add_tcp_flow(flow, "reno")

exp.require_qdisc_stats(router_left_connection)
exp.require_qdisc_stats(router_right_connection)

exp.run()






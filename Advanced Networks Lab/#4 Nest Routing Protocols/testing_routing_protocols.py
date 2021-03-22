
import unittest
from os.path import isfile
from nest import config
from nest.topology_map import TopologyMap
from nest.topology import Node, connect
from nest.routing.routing_helper import RoutingHelper
from nest.clean_up import delete_namespaces
from nest.experiment import *

#*    
#*     node-a                    node-c
#*      |                          |
#*      |                          |
#*   router_[r1] ------------- router_[r2]
#*      |                          |
#*      |                          |
#*     node-b                    node-d
#*    

@unittest.skipUnless(isfile("/usr/lib/frr/zebra"), "Frrouting is not installed")
class TestFrr(unittest.TestCase):

    def setUp(self):
        #* Creating Routers and Nodes
        self.nodes_Left = [Node('a'), Node('b')]
        self.nodes_Right = [Node('c'), Node('d')]

        self.routers = [Node('r1'), Node('r2')]
        for r in self.routers:
            r.enable_ip_forwarding()

        ###* Create interfaces and connect nodes and routers ###

        #* Left hand side connections
        (self.interface_node_a, self.interface_node_aRouter) = connect(self.nodes_Left[0], self.routers[0])
        (self.interface_node_bRouter, self.interface_node_b) = connect(self.routers[0], self.nodes_Left[1])

        #* Right hand side connections
        (self.interface_node_c, self.interface_node_cRouter) = connect(self.nodes_Right[0], self.routers[1])
        (self.interface_node_dRouter, self.interface_node_d) = connect(self.routers[1], self.nodes_Right[1])

        #* Connecting Routers
        (self.interface_router_r1, self.interface_router_r2) = connect(self.routers[0], self.routers[1])

        ### Assign addresses to interfaces ###

        #* Assigning Left side Addresses
        self.interface_node_a.set_address("10.0.1.1/24")
        self.interface_node_aRouter.set_address("10.0.1.2/24")

        self.interface_node_b.set_address("10.0.2.1/24")
        self.interface_node_bRouter.set_address("10.0.2.2/24")

        #* Assigning Right side Addresses
        self.interface_node_c.set_address("10.0.3.1/24")
        self.interface_node_cRouter.set_address("10.0.3.2/24")

        self.interface_node_d.set_address("10.0.4.1/24")
        self.interface_node_dRouter.set_address("10.0.4.2/24")

        self.interface_router_r1.set_address("10.0.5.1/24")
        self.interface_router_r2.set_address("10.0.5.2/24")

        #* Routing
        self.nodes_Left[0].add_route("DEFAULT", self.interface_node_a)
        self.nodes_Left[1].add_route("DEFAULT", self.interface_node_b)

        self.nodes_Right[0].add_route("DEFAULT", self.interface_node_c)
        self.nodes_Right[1].add_route("DEFAULT", self.interface_node_d)

        self.routers[0].add_route("DEFAULT", self.interface_router_r1)

        self.routers[0].add_route(self.interface_node_a.get_address(), self.interface_node_aRouter)
        self.routers[0].add_route(self.interface_node_b.get_address(), self.interface_node_bRouter)

        self.routers[1].add_route(self.interface_node_c.get_address(), self.interface_node_cRouter)
        self.routers[1].add_route(self.interface_node_d.get_address(), self.interface_node_dRouter)

        self.routers[1].add_route("DEFAULT", self.interface_router_r2)

        self.interface_node_a.set_attributes("100mbit", "5ms")
        self.interface_node_aRouter.set_attributes("100mbit", "5ms")
        self.interface_node_b.set_attributes("100mbit", "5ms")
        self.interface_node_bRouter.set_attributes("100mbit", "5ms")

        self.interface_node_c.set_attributes("100mbit", "5ms")
        self.interface_node_cRouter.set_attributes("100mbit", "5ms")
        self.interface_node_d.set_attributes("100mbit", "5ms")
        self.interface_node_dRouter.set_attributes("100mbit", "5ms")

        self.interface_router_r1.set_attributes("100mbit", "5ms")
        self.interface_router_r2.set_attributes("100mbit", "5ms")

        config.set_value("routing_suite", "frr") 

    def tearDown(self):
        delete_namespaces()
        TopologyMap.delete_all_mapping()

    def test_routing_helper(self):
        RoutingHelper("rip").populate_routing_tables()
        status = self.nodes_Left[0].ping("10.0.3.1", verbose=True)
        status = self.nodes_Right[1].ping("10.0.2.1", verbose=True)
        flowLeft = Flow(self.nodes_Left[0], self.nodes_Right[1], self.interface_node_d.address, 0, 30, 3)

        exp = Experiment("rip_routing_protocal")
        exp.add_tcp_flow(flowLeft)
        exp.run()


    def test_ospf(self):
        RoutingHelper("ospf").populate_routing_tables()
        status = self.nodes_Left[0].ping("10.0.3.1", verbose=True)
        status = self.nodes_Right[1].ping("10.0.2.1", verbose=True)
        flowLeft = Flow(self.nodes_Left[0], self.nodes_Right[1], self.interface_node_d.address, 0, 30, 3)

        exp = Experiment("ospf_routing_protocal")
        exp.add_tcp_flow(flowLeft)
        exp.run()

    
    def test_isis(self):
        RoutingHelper("isis").populate_routing_tables()
        status = self.nodes_Left[0].ping("10.0.3.1", verbose=True)
        status = self.nodes_Right[1].ping("10.0.2.1", verbose=True)

        flowLeft = Flow(self.nodes_Left[0], self.nodes_Right[1], self.interface_node_d.address, 0, 30, 3)

        exp = Experiment("isis_routing_protocal")
        exp.add_tcp_flow(flowLeft)
        exp.run()

if __name__ == "__main__":
    unittest.main()

# jackson@ubuntu:~/COEP/Courses Sem 1/ACN Lab/nest$ sudo python3 -m unittest -v
# [sudo] password for jackson: 
# test_isis (nest.tests.test_classed_based.TestFrr) ... [INFO] : Running zebra and isis on routers
# [INFO] : Waiting for isis to converge
# [INFO] : Routing completed
# SUCCESS: ping from a to 10.0.3.1
# SUCCESS: ping from d to 10.0.2.1

# [INFO] : Running experiment isis_routing_protocal 
# [INFO] : Running 3 netperf flows from a to 10.0.4.1...
# [INFO] : Running ss on nodes...
# [ERROR] : Collecting socket stats at a. /bin/bash: /home/jackson/COEP/Courses: No such file or directory

# [INFO] : Experiment complete!
# [INFO] : Parsing statistics...
# [INFO] : Output results as JSON dump
# [INFO] : Plotting results...
# [INFO] : Plotting complete!
# [INFO] : Cleaned up environment!
# ok
# test_ospf (nest.tests.test_classed_based.TestFrr) ... [INFO] : Running zebra and ospf on routers
# [INFO] : Waiting for ospf to converge
# [INFO] : Routing completed
# SUCCESS: ping from a to 10.0.3.1
# SUCCESS: ping from d to 10.0.2.1

# [INFO] : Running experiment ospf_routing_protocal 
# [ERROR] : Collecting socket stats at a. /bin/bash: /home/jackson/COEP/Courses: No such file or directory

# [INFO] : Cleaned up environment!
# ok
# test_routing_helper (nest.tests.test_classed_based.TestFrr) ... [INFO] : Running zebra and rip on routers
# [INFO] : Waiting for rip to converge
# [INFO] : Routing completed
# SUCCESS: ping from a to 10.0.3.1
# SUCCESS: ping from d to 10.0.2.1

# [INFO] : Running experiment rip_routing_protocal 
# [ERROR] : Collecting socket stats at a. /bin/bash: /home/jackson/COEP/Courses: No such file or directory

# [INFO] : Cleaned up environment!
# ok

# ----------------------------------------------------------------------
# Ran 3 tests in 105.877s

# OK
# [INFO] : Cleaned up environment!
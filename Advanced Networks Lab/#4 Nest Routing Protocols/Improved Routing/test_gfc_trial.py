import unittest
from os.path import isfile
from nest import config
from nest.topology_map import TopologyMap
from nest.topology import Node, connect
from nest.routing.routing_helper import RoutingHelper
from nest.clean_up import delete_namespaces
from nest.experiment import *

#*
#*
#*
#*
#*                   node-1          node-3
#*                     |               |
#*                     |               |
#*                     |               |                  
#*    node-0 ------ router(0) ----- router(1) ----- router(2) ----- node-5
#*                     |                               |
#*                     |                               |
#*                     |                               |
#*                   node-2                          node-4
#*

N = 6
R = 3

@unittest.skipUnless(isfile("/usr/lib/frr/zebra"), "Frrouting is not installed")
class TestFrr(unittest.TestCase):
    def setUp(self):
        #* Creating Nodes
        self.nodes = []
        for i in range(N):
            self.nodes.append(Node('node-' + str(i)))

        #* Creating Routers
        self.routers = []
        for i in range(R):
            self.routers.append(Node('router-' + str(i)))
            self.routers[-1].enable_ip_forwarding()
        
        #* Making Connections
        (self.r1_r0, self.r0_r1) = connect(self.routers[1], self.routers[0])
        (self.r2_r1, self.r1_r2) = connect(self.routers[2], self.routers[1])

        (self.r0_n0, self.n0_r0) = connect(self.routers[0], self.nodes[0])
        (self.r0_n1, self.n1_r0) = connect(self.routers[0], self.nodes[1])
        (self.r0_n2, self.n2_r0) = connect(self.routers[0], self.nodes[2])

        (self.r1_n3, self.n3_r1) = connect(self.routers[1], self.nodes[3])

        (self.r2_n4, self.n4_r2) = connect(self.routers[2], self.nodes[4])
        (self.r2_n5, self.n5_r2) = connect(self.routers[2], self.nodes[5])

        #* Setting Address for the nodes and routers
        self.r0_r1.set_address("10.0.2.2/24")
        self.r1_r0.set_address("10.0.2.3/24")
        self.r1_r2.set_address("10.0.3.2/24")
        self.r2_r1.set_address("10.0.3.3/24")

        self.n0_r0.set_address("10.0.1.1/24")
        self.r0_n0.set_address("10.0.1.2/24")
        self.n1_r0.set_address("10.0.4.1/24")
        self.r0_n1.set_address("10.0.4.2/24")
        self.n2_r0.set_address("10.0.5.1/24")
        self.r0_n2.set_address("10.0.5.2/24")

        self.n3_r1.set_address("10.0.6.1/24")
        self.r1_n3.set_address("10.0.6.2/24")

        self.n4_r2.set_address("10.0.7.1/24")
        self.r2_n4.set_address("10.0.7.2/24")
        self.n5_r2.set_address("10.0.8.1/24")
        self.r2_n5.set_address("10.0.8.2/24")

        #* Adding routes in Routing Tables
        self.nodes[0].add_route('DEFAULT', self.n0_r0)
        self.nodes[1].add_route('DEFAULT', self.n1_r0)
        self.nodes[2].add_route('DEFAULT', self.n2_r0)

        self.nodes[3].add_route('DEFAULT', self.n3_r1)

        self.nodes[4].add_route('DEFAULT', self.n4_r2)
        self.nodes[5].add_route('DEFAULT', self.n5_r2)

        self.routers[0].add_route(self.n0_r0.subnet, self.r0_n0)
        self.routers[0].add_route(self.n1_r0.subnet, self.r0_n1)
        self.routers[0].add_route(self.n2_r0.subnet, self.r0_n2)
        self.routers[0].add_route('DEFAULT', self.r0_r1)

        self.routers[1].add_route(self.n0_r0.subnet, self.r1_r0)
        self.routers[1].add_route(self.n1_r0.subnet, self.r1_r0)
        self.routers[1].add_route(self.n2_r0.subnet, self.r1_r0)
        self.routers[1].add_route(self.r0_r1.subnet, self.r1_r0)
        self.routers[1].add_route(self.n3_r1.subnet, self.r1_n3)
        self.routers[1].add_route(self.r2_r1.subnet, self.r1_r2)
        self.routers[1].add_route('DEFAULT', self.r1_r2)

        self.routers[2].add_route(self.n0_r0.subnet, self.r2_r1)
        self.routers[2].add_route(self.n1_r0.subnet, self.r2_r1)
        self.routers[2].add_route(self.n2_r0.subnet, self.r2_r1)
        self.routers[2].add_route(self.r0_r1.subnet, self.r2_r1)
        self.routers[2].add_route(self.n3_r1.subnet, self.r2_r1)
        self.routers[2].add_route(self.r2_r1.subnet, self.r2_r1)
        self.routers[2].add_route(self.n4_r2.subnet, self.r2_n4)
        self.routers[2].add_route(self.n5_r2.subnet, self.r2_n5)
        self.routers[2].add_route('DEFAULT', self.r2_r1)

        #* Setting Connection Attributes
        self.r0_r1.set_attributes("20mbit", "50ms")
        self.r1_r0.set_attributes("20mbit", "50ms")
        self.r1_r2.set_attributes("20mbit", "50ms")
        self.r2_r1.set_attributes("20mbit", "50ms")

        for n in self.nodes:
            for i in n.interfaces:
                i.set_attributes("100mbit", "10ms")
                i.pair.set_attributes("100mbit", "10ms")
        
        config.set_value("routing_suite", "frr") 

    def tearDown(self):
        delete_namespaces()
        TopologyMap.delete_all_mapping()
        
    def test_routing_helper(self):
        RoutingHelper("rip").populate_routing_tables()
        self.nodes[0].ping(self.n5_r2.get_address(), verbose = True)

        flow = Flow(self.nodes[0], self.nodes[5], self.n5_r2.address, 0, 30, 2)

        exp = Experiment("rip_routing_protocal")
        exp.add_tcp_flow(flow)
        exp.run()


    def test_ospf(self):
        RoutingHelper("ospf").populate_routing_tables()
        self.nodes[0].ping(self.n5_r2.get_address(), verbose = True)

        flow = Flow(self.nodes[0], self.nodes[5], self.n5_r2.address, 0, 30, 2)

        exp = Experiment("ospf_routing_protocal")
        exp.add_tcp_flow(flow)
        exp.run()

    
    def test_isis(self):
        RoutingHelper("isis").populate_routing_tables()
        self.nodes[0].ping(self.n5_r2.get_address(), verbose = True)

        flow = Flow(self.nodes[0], self.nodes[5], self.n5_r2.address, 0, 30, 2)

        exp = Experiment("isis_routing_protocal")
        exp.add_tcp_flow(flow)
        exp.run()

if __name__ == "__main__":
    unittest.main()


#* jackson@ubuntu:~/COEP/Courses Sem 1/ACN Lab/nest$ sudo python3 -m unittest -v
#* test_isis (nest.tests.test_gfc_trial.TestFrr) ... [INFO] : Running zebra and isis on routers
#* [INFO] : Waiting for isis to converge
#* [INFO] : Routing completed
#* SUCCESS: ping from node-0 to 10.0.8.1

#* [INFO] : Running experiment isis_routing_protocal 
#* [INFO] : Running 2 netperf flows from node-0 to 10.0.8.1...
#* [INFO] : Running ss on nodes...
#* [ERROR] : Collecting socket stats at node-0. /bin/bash: /home/jackson/COEP/Courses: No such file or directory

#* [INFO] : Experiment complete!
#* [INFO] : Parsing statistics...
#* [INFO] : Output results as JSON dump
#* [INFO] : Plotting results...
#* [INFO] : Plotting complete!
#* [INFO] : Cleaned up environment!
#* ok
#* test_ospf (nest.tests.test_gfc_trial.TestFrr) ... [INFO] : Running zebra and ospf on routers
#* [INFO] : Waiting for ospf to converge
#* [INFO] : Routing completed
#* SUCCESS: ping from node-0 to 10.0.8.1

#* [INFO] : Running experiment ospf_routing_protocal 
#* [ERROR] : Collecting socket stats at node-0. /bin/bash: /home/jackson/COEP/Courses: No such file or directory

#* [INFO] : Cleaned up environment!
#* ok
#* test_routing_helper (nest.tests.test_gfc_trial.TestFrr) ... [INFO] : Running zebra and rip on routers
#* [INFO] : Waiting for rip to converge
#* [INFO] : Routing completed
#* SUCCESS: ping from node-0 to 10.0.8.1

#* [INFO] : Running experiment rip_routing_protocal 
#* [ERROR] : Collecting socket stats at node-0. /bin/bash: /home/jackson/COEP/Courses: No such file or directory

#* [INFO] : Cleaned up environment!
#* ok

#* ----------------------------------------------------------------------
#* Ran 3 tests in 123.953s

#* OK
#* [INFO] : Cleaned up environment!
//* 122022010 Shrayank Jai Mistry

//*
//*                                      
//*                                          *    *                
//*                                          |    |   Wifi 15.0.4.0 
//*                                         n8   n9                
//*                                                        AP       
//*                                                        * 
//*                          15.0.1.0                      |
//*  n7   n6   n5   n0 ------------------- n1   n2   n3   n4  
//*   |    |    |    |    point-to-point    |    |    |    |
//*  ==================                    ==================
//*  LAN 15.0.3.0 (Two)                    LAN 15.0.2.0 (One)

#include "ns3/core-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/network-module.h"
#include "ns3/applications-module.h"
#include "ns3/mobility-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/ssid.h"

using namespace ns3;


int main(int argc, char *argv[]) {

    LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
    LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);

    //* ---------- [n0 to n1 Point-to-Point] ---------- *//
    NodeContainer p2pNodes;
    p2pNodes.Create(2);

    PointToPointHelper pointToPoint;
    pointToPoint.SetDeviceAttribute("DataRate", StringValue("10Mbps"));
    pointToPoint.SetChannelAttribute("Delay", StringValue("2ms"));

    NetDeviceContainer p2pDevices;
    p2pDevices = pointToPoint.Install(p2pNodes);

    InternetStackHelper stack;
    stack.Install(p2pNodes);

    Ipv4AddressHelper address;
    address.SetBase("15.0.1.0", "255.255.255.0");

    Ipv4InterfaceContainer p2pInterfaces;
    p2pInterfaces = address.Assign(p2pDevices);

    //* ---------- [n1 to n4 CSMA (Ethernet)] ---------- *//
    NodeContainer csmaNodes_One;
    csmaNodes_One.Add (p2pNodes.Get(1));
    csmaNodes_One.Create(3);

    CsmaHelper csma_One;
    csma_One.SetChannelAttribute ("DataRate", StringValue ("100Mbps"));
    csma_One.SetChannelAttribute ("Delay", TimeValue (NanoSeconds (6560)));

    NetDeviceContainer csmaDevices_One;
    csmaDevices_One = csma_One.Install(csmaNodes_One);

    for (int i = 1; i < 4; i++) stack.Install(csmaNodes_One.Get(i));

    address.SetBase("15.0.2.0", "255.255.255.0");
    
    Ipv4InterfaceContainer csmaInterfaces_One;
    csmaInterfaces_One = address.Assign(csmaDevices_One);

    //* ---------- [n0 to n7 CSMA (Ethernet)] ---------- *//
    NodeContainer csmaNodes_Two;
    csmaNodes_Two.Add (p2pNodes.Get(0));
    csmaNodes_Two.Create(3);

    CsmaHelper csma_Two;
    csma_Two.SetChannelAttribute ("DataRate", StringValue ("50Mbps"));
    csma_Two.SetChannelAttribute ("Delay", TimeValue (NanoSeconds (8560)));

    NetDeviceContainer csmaDevices_Two;
    csmaDevices_Two = csma_Two.Install(csmaNodes_Two);

    for (int i = 1; i < 4; i++) stack.Install(csmaNodes_Two.Get(i));

    address.SetBase("15.0.3.0", "255.255.255.0");

    Ipv4InterfaceContainer csmaInterfaces_Two;
    csmaInterfaces_Two = address.Assign(csmaDevices_Two); 

    //* ---------- [n4 to n9 Wifi Network (Wireless)] ---------- *//
    NodeContainer wifiStaNodes;
    wifiStaNodes.Create(2);

    NodeContainer wifiApNode = csmaNodes_One.Get(3);

    YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
    YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
    phy.SetChannel (channel.Create ());

    WifiHelper wifi;
    wifi.SetRemoteStationManager ("ns3::AarfWifiManager");

    WifiMacHelper mac;
    Ssid ssid = Ssid ("wireless-network");
    mac.SetType ("ns3::StaWifiMac",
               "Ssid", SsidValue (ssid),
               "ActiveProbing", BooleanValue (false));
    
    NetDeviceContainer staDevices;
    staDevices = wifi.Install (phy, mac, wifiStaNodes);

    mac.SetType ("ns3::ApWifiMac",
               "Ssid", SsidValue (ssid));
        
    NetDeviceContainer apDevices;
    apDevices = wifi.Install (phy, mac, wifiApNode);

    MobilityHelper mobility;
    mobility.SetPositionAllocator ("ns3::GridPositionAllocator",
                                 "MinX", DoubleValue (0.0),
                                 "MinY", DoubleValue (0.0),
                                 "DeltaX", DoubleValue (5.0),
                                 "DeltaY", DoubleValue (10.0),
                                 "GridWidth", UintegerValue (3),
                                 "LayoutType", StringValue ("RowFirst"));

    mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
                             "Bounds", RectangleValue (Rectangle (-50, 50, -50, 50)));
    mobility.Install (wifiStaNodes);

    mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
    mobility.Install (wifiApNode);

    stack.Install (wifiStaNodes);

    address.SetBase("15.0.4.0", "255.255.255.0");
    address.Assign (staDevices);
    address.Assign (apDevices);

    //* ---------- Setting Server and Client ---------- *//
    int server_port = 9;
    UdpEchoServerHelper server (server_port);

    ApplicationContainer serverApps = server.Install(csmaNodes_Two.Get(3));
    serverApps.Start(Seconds(1.0));
    serverApps.Stop(Seconds(10.0)); 

    UdpEchoClientHelper client (csmaInterfaces_Two.GetAddress(3), server_port);
    client.SetAttribute ("MaxPackets", UintegerValue (2));
    client.SetAttribute ("Interval", TimeValue (Seconds (3.0)));
    client.SetAttribute ("PacketSize", UintegerValue (1024));

    ApplicationContainer clientApps = client.Install(wifiStaNodes.Get(1));
    clientApps.Start(Seconds(1.0));
    clientApps.Stop(Seconds(10.0)); 


    //* ---------- Setting Server and Client ---------- *//
    UdpEchoServerHelper server2 (10);

    ApplicationContainer serverApps2 = server2.Install(csmaNodes_One.Get(2));
    serverApps2.Start(Seconds(10.0));
    serverApps2.Stop(Seconds(20.0)); 

    UdpEchoClientHelper client2 (csmaInterfaces_One.GetAddress(2), 10);
    client2.SetAttribute ("MaxPackets", UintegerValue (1));
    client2.SetAttribute ("Interval", TimeValue (Seconds (2.0)));
    client2.SetAttribute ("PacketSize", UintegerValue (2048));

    ApplicationContainer clientApps2 = client2.Install(csmaNodes_Two.Get(3));
    clientApps2.Start(Seconds(10.0));
    clientApps2.Stop(Seconds(20.0)); 

    Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

    Simulator::Stop (Seconds (20.0));

    csma_Two.EnablePcap("server-S1", csmaDevices_Two.Get(3), true);
    phy.EnablePcap("client-S1", staDevices.Get(1));

    csma_One.EnablePcap("server-S2", csmaDevices_One.Get(2), true);
    csma_Two.EnablePcap("client-S2", csmaDevices_Two.Get(3), true);

    Simulator::Run ();
    Simulator::Destroy ();
    return 0;
}


//* Command to Run cc
//* cp examples/tutorial/first.cc scratch/myfirst.cc
//* ./waf
//* ./waf --run scratch/myfirst


//* Command to Run Python
//* ./waf --pyrun examples/tutorial/first.py
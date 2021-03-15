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
#include "ns3/packet-sink.h"

using namespace ns3;

void StartFlow (Ptr<Socket>, Ipv4Address, uint16_t);

int main(int argc, char *argv[]) {

    // LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
    // LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);

    bool tracing = true;
    // uint32_t maxBytes = 2147483642;
    // uint32_t maxBytes = 2147483;

    //* ---------- [n0 to n1 Point-to-Point] ---------- *//
    NodeContainer p2pNodes;
    p2pNodes.Create(2);

    PointToPointHelper pointToPoint;
    pointToPoint.SetDeviceAttribute("DataRate", StringValue("500Kbps"));
    pointToPoint.SetChannelAttribute("Delay", StringValue("5ms"));

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
    csma_One.SetChannelAttribute ("DataRate", StringValue ("500Kbps"));
    csma_One.SetChannelAttribute ("Delay", TimeValue (MilliSeconds (5)));

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

    //* Configuring the Tcp Congestion Window size (default = 10)
    uint32_t cwnd_size = 1;
    Config::SetDefault("ns3::TcpSocket::InitialCwnd", UintegerValue(cwnd_size));

    //* Configuring the Tcp Window Scaling 
    bool wnd_scaling = true;
    Config::SetDefault("ns3::TcpSocketBase::WindowScaling", BooleanValue(wnd_scaling));

    Config::SetDefault("ns3::TcpSocket::InitialSlowStartThreshold", UintegerValue(4294967295 - 1000000));

    //* Setting Up Server and Client Tcp Connection
    uint16_t port = 9;

    PacketSinkHelper sink ("ns3::TcpSocketFactory",InetSocketAddress (Ipv4Address::GetAny (), port));
    ApplicationContainer sinkApps = sink.Install (p2pNodes.Get (0));
    sinkApps.Start (Seconds (0.0));
    sinkApps.Stop (Seconds (10.0));

    // TypeId tid = TypeId::LookupByName ("ns3::TcpNewReno");
    // Config::Set ("/NodeList/*/$ns3::TcpL4Protocol/SocketType", TypeIdValue (tid));

    Ptr<Socket> source = Socket::CreateSocket(p2pNodes.Get(1), TcpSocketFactory::GetTypeId());

    // source->SetAttribute("InitialCwnd", ns3::UintegerValue(100));
    source->Bind();

    Simulator::Schedule (Seconds (0.0), &StartFlow, source, p2pInterfaces.GetAddress (0), port);

    if (tracing) {
        pointToPoint.EnablePcap("p2p-node(0)", p2pDevices.Get(0), true);
        pointToPoint.EnablePcap("p2p-node(1)", p2pDevices.Get(1), true);

        // csma_Two.EnablePcap("sender-bulk", csmaDevices_Two.Get(2), true);
        // csma_One.EnablePcap("receiver-bulk", csmaDevices_One.Get(1), true);
    }

    Simulator::Stop (Seconds (1000.0));
    Simulator::Run ();
    Simulator::Destroy ();

    Ptr<PacketSink> sink1 = DynamicCast<PacketSink> (sinkApps.Get (0));
    std::cout << "Total Bytes Received: [Socket Sender] " << sink1->GetTotalRx () << " Bytes" << std::endl;

    return 0;
}

void StartFlow (Ptr<Socket> localSocket, Ipv4Address servAddress, uint16_t servPort){

    localSocket->Connect(InetSocketAddress (servAddress, servPort));

    int packet_cnt = 100;
    int packet_size = 10240; //* Bytes
    // int data_sent = packet_cnt * packet_size;

    for (int i = 0; i < packet_cnt; i++) {
        Ptr<Packet> pac = Create<Packet>(packet_size);
        localSocket->Send(pac);
    }
    localSocket->Close();

    // localSocket->Send(Create<Packet>(102400));
    localSocket->Close();
}

//TODO OUTPUT
//* Congestion Window Size = 1
//* 351	2.212271	15.0.1.2	15.0.1.1	TCP	54	49153 → 9 [ACK] Seq=122882 Ack=2 Win=65535 Len=0 TSval=2212 TSecr=2205

//* Congestion Window Size = 10
//* 351	2.189119	15.0.1.2	15.0.1.1	TCP	54	49153 → 9 [ACK] Seq=122882 Ack=2 Win=65535 Len=0 TSval=2189 TSecr=2182

//* Window Scaling (false)
//* 351	2.189119	15.0.1.2	15.0.1.1	TCP	54	49153 → 9 [ACK] Seq=122882 Ack=2 Win=65535 Len=0 TSval=2189 TSecr=2182

//* Window Scaling (true)
//* 351	2.189247	15.0.1.2	15.0.1.1	TCP	54	49153 → 9 [ACK] Seq=122882 Ack=2 Win=131072 Len=0 TSval=2189 TSecr=2182
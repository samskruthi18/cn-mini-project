# CN Mini Project: SDN Bandwidth Reservation

This project combines a TCP bandwidth-reservation service with Mininet and Open vSwitch traffic control.

## Topology and behavior

Three hosts, h1, h2 and h3, connect to switch s1. Hosts h1 and h2 send reservation requests to the server on h3. The reservation service tracks a logical capacity of 100 Mbps.

Static OpenFlow 1.3 rules forward traffic and mark matching client traffic with DSCP 46. The policy bridge applies a shared 5 Mbps TBF limiter on s1-eth3 while reservations are active. This limiter is shared across clients; requested bandwidth is not shaped separately per client.

## Requirements

Ubuntu with Mininet, Open vSwitch, Python 3, iperf3 and the project files.

## Run the integrated Mininet setup

Use two Ubuntu terminals. In both, go to the project folder:

    cd ~/cn-mini-project-p3

Terminal 1 — start the policy bridge and leave it running:

    sudo python3 policy_bridge.py

Terminal 2 — start Mininet:

    sudo mn --custom topology.py --topo reservation --switch ovsk,protocols=OpenFlow13 --controller=none

At the mininet> prompt, install the forwarding rules and start the integrated reservation server and iperf3 server:

    sh bash install_flows.sh
    h3 python3 -u p1-socket-reservation/server_integrated.py > /tmp/sdn-server.log 2>&1 &
    h3 iperf3 -s -D

Check that the reservation server started:

    h3 cat /tmp/sdn-server.log

## Run traffic tests

From the mininet> prompt:

    h1 iperf3 -c 10.0.0.3 -t 10 -i 1
    h1 ping -c 10 10.0.0.3

Reservation client programs are in p1-socket-reservation/client1.py and client2.py. The integrated server accepts TCP requests on port 5000.

## Stop Mininet

At the mininet> prompt, type:

    exit

## Evaluation and evidence

See results/evaluation.md for the recorded comparison and limitations. Test outputs and check records are stored in results/evidence/.

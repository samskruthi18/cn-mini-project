
#!/bin/bash
set -e

SWITCH="s1"
OF="sudo ovs-ofctl -O OpenFlow13"

$OF add-flow "$SWITCH" "priority=200,arp,actions=flood"
$OF add-flow "$SWITCH" "priority=100,ip,nw_dst=10.0.0.1,actions=output:1"
$OF add-flow "$SWITCH" "priority=100,ip,nw_dst=10.0.0.2,actions=output:2"
$OF add-flow "$SWITCH" "priority=100,ip,nw_dst=10.0.0.3,actions=output:3"
$OF add-flow "$SWITCH" "priority=0,actions=drop"

echo "OpenFlow rules installed successfully."

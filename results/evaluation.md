# Performance Evaluation

## Test setup

- Date: 13 November 2026
- Topology: Mininet hosts h1, h2 and h3 connected to switch s1
- Forwarding: Static OpenFlow 1.3 rules on Open vSwitch; no external controller
- Logical reservation capacity: 100 Mbps
- Baseline: Original reservation server; no traffic shaper on s1-eth3
- SDN-enabled: Integrated reservation server and policy bridge; shared TBF limiter at 5 Mbps on s1-eth3
- Traffic tests: `iperf3` TCP for 10 seconds and `ping -c 10`
- Runs: One run per condition; results are observations, not repeated-run averages

Reservation loads refer to the requested logical bandwidth. The 5 Mbps SDN limiter is shared across clients; it does not enforce each reservation separately.

## Results

| Mode | Load | Reservation requests | Throughput (iperf3 receiver) | Ping average RTT | Packet loss | Notes |
|---|---:|---|---:|---:|---:|---|
| Baseline | Low: 20 Mbps | C1 20 Mbps accepted | 38.0 Gbit/s | 0.062 ms | 0% | No traffic shaper |
| SDN-enabled | Low: 20 Mbps | C1 20 Mbps accepted | 4.73 Mbps | 0.226 ms | 0% | Shared 5 Mbps TBF active; cleared after release |
| Baseline | Medium: 50 Mbps | C1 50 Mbps accepted | 43.8 Gbit/s | 0.242 ms | 0% | The iperf3 run lasted 20.27 seconds despite `-t 10`; treat as anomalous |
| SDN-enabled | Medium: 50 Mbps | C1 50 Mbps accepted | 2.67 Mbps | 0.223 ms | 0% | Shared 5 Mbps TBF active; cleared after release |
| Baseline | High: 90 Mbps | C1 60 Mbps and C2 30 Mbps accepted | 38.4 Gbit/s | 0.085 ms | 0% | No traffic shaper |
| SDN-enabled | High: 90 Mbps | C1 60 Mbps and C2 30 Mbps accepted | 4.73 Mbps | 0.117 ms | 0% | Shared 5 Mbps TBF active; cleared after both releases |

Each row is from a single run. Mininet throughput can vary substantially between runs. The baseline and SDN results are not direct measurements of individually allocated bandwidth: the baseline is unshaped, while SDN applies one shared 5 Mbps limiter.

## Reservation and policy checks

- The reservation server enforced a logical total capacity of 100 Mbps.
- A 60 Mbps reservation was accepted and a subsequent 50 Mbps request was rejected when only 40 Mbps remained.
- High-load testing accepted 60 Mbps for C1 and 30 Mbps for C2.
- Reservation IDs matched between acceptance and release responses.
- A short-duration reservation expired and returned capacity; the limiter was removed after the final active reservation ended.
- The SDN policy marked matching client traffic with DSCP 46 and applied the shared TBF limiter on s1-eth3.

## Limitations

- Only one throughput and ping run was recorded for each load and mode.
- The shared 5 Mbps limiter is not per-client bandwidth allocation.
- The unshaped baseline has much higher throughput than the shaped SDN mode, so the figures describe these test configurations and should not be interpreted as an equal-capacity comparison.
- The baseline medium iperf3 run exceeded its requested duration.
- Reservation response-time samples were collected separately and are not included in the throughput/ping table.

## Evidence

Raw test outputs and check records are stored in `results/evidence/`.

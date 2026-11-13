# Low/Medium/High Comparison Checkpoint — Partial

Date: 2026-11-13
Branch: person3-sdn-integration

## Method so far

- Reservation load means aggregate logical reservation requests: low 20 Mbps, medium 50 Mbps, high 90 Mbps.
- Traffic command: `h1 iperf3 -c 10.0.0.3 -t 10 -i 1` (TCP), and `h1 ping -c 10 10.0.0.3`.
- Baseline used `server.py` with no traffic shaper (`noqueue`).
- SDN used `server_integrated.py` and the policy bridge, with a shared TBF limiter at 5 Mbit, burst 4 KB, latency 400 ms.
- Each condition has one run so far.

## Results collected

| Mode | Reservation load | iperf3 result | Ping average | Packet loss | Notes |
|---|---:|---|---:|---:|---|
| Baseline | 20 Mbps | 38.0 Gbit/s over 10.00 s; 1,685 sender retransmissions | 0.062 ms | 0% | C1 reservation accepted |
| Baseline | 50 Mbps | 43.8 Gbit/s over 20.27 s; 4 sender retransmissions | 0.242 ms | 0% | Requested `-t 10`, but actual summary duration was 20.27 s |
| Baseline | 90 Mbps | 38.4 Gbit/s over 10.00 s; 837 sender retransmissions | 0.085 ms | 0% | C1 60 Mbps and C2 30 Mbps accepted |
| SDN | 20 Mbps | Sender 5.56 Mbps; receiver 4.73 Mbps over 10.20 s | 0.226 ms | 0% | C1 reserve/release ID matched; qdisc returned to `noqueue` |
| SDN | 50 Mbps | Sender 3.35 Mbps; receiver 2.67 Mbps over 10.20 s | 0.223 ms | 0% | C1 reserve/release ID matched; qdisc returned to `noqueue` |
| SDN | 90 Mbps | Pending | Pending | Pending | C1 60 Mbps and C2 30 Mbps accepted; 5 Mbit TBF active |

These are single-run observations, not averages across repeated runs. The baseline medium run lasted longer than requested, and baseline throughput varied considerably. Person 1’s separate baseline screenshots show 17.7 Gbit/s and 0.639 ms; retain those as a separate run.

## Saved evidence

- Individual SDN low- and medium-load outputs and the high-load reservation/qdisc setup are saved in this folder.
- Person 1’s screenshots are in this folder after the latest `git pull`.
- The high-load SDN `iperf3` and ping measurements are still to be run.
- The README and evaluation report still need consolidation after measurements are complete.

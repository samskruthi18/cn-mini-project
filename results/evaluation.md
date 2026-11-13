# Performance Evaluation
# Performance Evaluation
# Performance Evaluation

## Test Setup
- Date: 13/11/2026
- Mininet topology: h1, h2, h3 connected through switch s1
- Controller: None; static OpenFlow rules installed using Open vSwitch
- Reservation capacity: 100 Mbps
- Traffic shaping: 5 Mbps shared TBF limiter
- Testing tool: iperf3 and ping
- Number of runs per condition: 1

## Reservation Validation

| Test | Request | Result |
|---|---|---|
| Client 1 | 40 Mbps | Accepted |
| Client 2 | 50 Mbps | Accepted |
| Additional request | 20 Mbps | Rejected |
| Manual release | C1 | Successful |
| Automatic expiry | C1/C2 | Verified |
| Final status | USED=0 | Successful |

## Performance Results

| Metric | Baseline | SDN-enabled |
|---|---:|---:|
| Throughput | 11.4 Gbps | 4.73 Mbps |
| Average latency | 0.240 ms | 0.383 ms |
| Packet loss | 0% | 0% |

## Observations

- The server successfully enforced the logical reservation capacity of 100 Mbps.
- Requests exceeding available capacity were rejected.
- The SDN policy installed a shared 5 Mbps traffic limiter.
- Measured SDN-enabled receiver throughput was 4.73 Mbps.
- The limiter was removed after the final reservation was released.
- Base OpenFlow forwarding rules remained active after policy cleanup.
- All tested ping packets were successfully delivered.

## Limitations

- The 5 Mbps limiter is shared across clients rather than allocated individually.
- The baseline throughput is measured without traffic shaping and is not directly comparable to a shaped physical network.
- Only one throughput and latency run per condition was recorded.
- The experiment uses a small Mininet topology.

## Conclusion

The experiment demonstrates successful integration of TCP-based bandwidth reservation with SDN-based traffic control. Reservation validation, capacity management, policy installation, release and expiry were verified. The traffic shaper successfully limited network throughput to approximately 5 Mbps.

## Test setup

- Date: 10/10/2026
- Mininet topology: reservation topology with h1, h2, h3 and switch s1
- Controller: none; static OpenFlow rules installed on OVS
- Link capacity:
- Workload/tool:reservation requests and iperf3
- Number of runs per condition: Not Measured
- Load: 60 Mbps reservation request, followed by 50 Mbps request
- Reservation Capacity: 100 Mbps

## Results

| Mode | Load | Requests sent | Accepted | Rejected | Avg response time (ms) | Throughput (Mbps) | Reserved (Mbps) | Utilization (%) | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|


## Calculations

- Acceptance/rejection counts: count the actual server responses.
- Average response time: average time from sending a request to receiving its response.
- Utilization: reserved bandwidth ÷ total link capacity × 100.
- Throughput: record the measured traffic rate and the tool used.

## Observation Checks
- Reservation capacity: 100 Mbps.
- Capacity test: a 60 Mbps request was accepted; a subsequent 50 Mbps request was rejected because capacity was insufficient.
- Throughput: iperf3 receiver measured 3.45 Mbps in a 10-second run and 4.04 Mbps in a separate 5-second run. The configured traffic shaper was 5 Mbps.
- Response time: one STATUS request took 0.804 ms (single sample; not an average).
- Shared limiter: it remained active after one client released its reservation and was removed after the final client released.

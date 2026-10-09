# Performance Evaluation

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

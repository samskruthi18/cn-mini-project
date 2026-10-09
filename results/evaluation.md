# Performance Evaluation

## Test setup

- Date:
- Mininet topology:
- Controller:
- Link capacity:
- Workload/tool:
- Number of runs per condition:

## Results

| Mode | Load | Requests sent | Accepted | Rejected | Avg response time (ms) | Throughput (Mbps) | Reserved (Mbps) | Utilization (%) | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Static baseline | Low | | | | | | | | |
| SDN controlled | Low | | | | | | | | |
| Static baseline | Medium | | | | | | | | |
| SDN controlled | Medium | | | | | | | | |
| Static baseline | High | | | | | | | | |
| SDN controlled | High | | | | | | | | |

## Calculations

- Acceptance/rejection counts: count the actual server responses.
- Average response time: average time from sending a request to receiving its response.
- Utilization: reserved bandwidth ÷ total link capacity × 100.
- Throughput: record the measured traffic rate and the tool used.
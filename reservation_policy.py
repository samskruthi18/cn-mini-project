
#!/usr/bin/env python3
import subprocess
import sys

SWITCH = "s1"
SERVER_IP = "10.0.0.3"
SERVER_PORT = "s1-eth3"
BANDWIDTH_LIMIT = "5mbit"

CLIENT_PORTS = {
    "10.0.0.1": 1,
    "10.0.0.2": 2,
}


def run_flow(command, rule):
    subprocess.run(
        ["sudo", "ovs-ofctl", "-O", "OpenFlow13",
         command, SWITCH, rule],
        check=True,
    )


def reserve(client_ip):
    rule = (
        f"priority=200,ip,nw_src={client_ip},"
        f"nw_dst={SERVER_IP},"
        f"actions=set_field:46->ip_dscp,output:3"
    )

    run_flow("add-flow", rule)

    subprocess.run(
        ["sudo", "tc", "qdisc", "replace",
         "dev", SERVER_PORT, "root", "tbf",
         "rate", BANDWIDTH_LIMIT, "burst", "32kbit",
         "latency", "400ms"],
        check=True,
    )

    print(f"Reservation policy installed for {client_ip}")
    print(f"Bandwidth limit enabled: {BANDWIDTH_LIMIT}")


def release(client_ip):
    rule = f"ip,nw_src={client_ip},nw_dst={SERVER_IP}"
    run_flow("del-flows", rule)

    subprocess.run(
        ["sudo", "tc", "qdisc", "del",
         "dev", SERVER_PORT, "root"],
        check=True,
    )

    print(f"Reservation policy removed for {client_ip}")
    print("Bandwidth limit disabled")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(
            "Usage: python3 reservation_policy.py "
            "reserve|release CLIENT_IP"
        )

    action, client_ip = sys.argv[1], sys.argv[2]

    if action not in {"reserve", "release"}:
        sys.exit("Action must be reserve or release")

    if client_ip not in CLIENT_PORTS:
        sys.exit("Client IP must be 10.0.0.1 or 10.0.0.2")

    if action == "reserve":
        reserve(client_ip)
    else:
        release(client_ip)

#!/usr/bin/env python3
import json
import os
from pathlib import Path
import socket
import subprocess
import sys

SOCKET_PATH = "/tmp/cn-mini-policy.sock"
SWITCH = "s1"
SERVER_IP = "10.0.0.3"
POLICY_SCRIPT = Path(__file__).with_name("reservation_policy.py")
ALLOWED_CLIENTS = {"10.0.0.1", "10.0.0.2"}

# Keep the shared limiter active until the final client releases its reservation.
active_clients = set()


def run_policy(action, client_ip):
    result = subprocess.run(
        [sys.executable, str(POLICY_SCRIPT), action, client_ip],
        capture_output=True,
        text=True,
    )
    details = (result.stdout + result.stderr).strip()
    return result.returncode == 0, details


def remove_client_flow(client_ip):
    match = f"ip,nw_src={client_ip},nw_dst={SERVER_IP}"
    result = subprocess.run(
        ["ovs-ofctl", "-O", "OpenFlow13", "del-flows", SWITCH, match],
        capture_output=True,
        text=True,
    )
    details = (result.stdout + result.stderr).strip()
    return result.returncode == 0, details


def handle_request(request):
    action = request.get("action")
    client_ip = request.get("client_ip")

    if client_ip not in ALLOWED_CLIENTS:
        return {"ok": False, "message": "Client IP is not allowed"}

    if action == "reserve":
        if client_ip in active_clients:
            return {"ok": True, "message": "Policy already active for this client"}

        ok, details = run_policy("reserve", client_ip)
        if ok:
            active_clients.add(client_ip)
        else:
            # Clean up a possible partial flow installation.
            remove_client_flow(client_ip)

        return {"ok": ok, "message": details or "Policy command completed"}

    if action == "release":
        if client_ip not in active_clients:
            return {"ok": False, "message": "No active policy for this client"}

        if len(active_clients) > 1:
            # Remove this client's flow but keep the shared bandwidth limiter.
            ok, details = remove_client_flow(client_ip)
        else:
            # The final client can remove its flow and the shared limiter.
            ok, details = run_policy("release", client_ip)

        if ok:
            active_clients.remove(client_ip)

        return {"ok": ok, "message": details or "Policy command completed"}

    return {"ok": False, "message": "Unknown action"}


def main():
    if os.geteuid() != 0:
        sys.exit("Start this bridge with sudo from the Ubuntu project folder.")

    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    os.chmod(SOCKET_PATH, 0o600)
    server.listen()

    print(f"Policy bridge listening at {SOCKET_PATH}")
    try:
        while True:
            connection, _ = server.accept()
            with connection:
                stream = connection.makefile("rwb")
                try:
                    request = json.loads(stream.readline().decode())
                    response = handle_request(request)
                except Exception as error:
                    response = {"ok": False, "message": str(error)}

                stream.write((json.dumps(response) + "\n").encode())
                stream.flush()
    finally:
        server.close()
        if os.path.exists(SOCKET_PATH):
            os.unlink(SOCKET_PATH)


if __name__ == "__main__":
    main()

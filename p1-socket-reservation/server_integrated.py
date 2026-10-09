#!/usr/bin/env python3
import json
import socket
import threading
import uuid

HOST = "0.0.0.0"
PORT = 5000
TOTAL_BANDWIDTH = 100
POLICY_SOCKET = "/tmp/cn-mini-policy.sock"

CLIENT_IPS = {
    "C1": "10.0.0.1",
    "C2": "10.0.0.2",
}

# One active reservation per client, matching the original server behavior.
reservations = {}
timers = {}
lock = threading.Lock()


def call_policy(action, client_ip):
    request = {"action": action, "client_ip": client_ip}

    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as policy_socket:
            policy_socket.settimeout(15)
            policy_socket.connect(POLICY_SOCKET)
            policy_socket.sendall((json.dumps(request) + "\n").encode())

            with policy_socket.makefile("rb") as response_stream:
                response = json.loads(response_stream.readline().decode())

        return response.get("ok") is True, response.get("message", "")
    except Exception as error:
        return False, str(error)


def expire_reservation(client_id, reservation_id):
    with lock:
        current = reservations.get(client_id)
        if not current or current["reservation_id"] != reservation_id:
            return

        client_ip = CLIENT_IPS[client_id]
        ok, message = call_policy("release", client_ip)

        if ok:
            del reservations[client_id]
            timers.pop(client_id, None)
            print(f"Reservation expired: {client_id} ({reservation_id})")
        else:
            print(f"Expiry policy removal failed for {client_id}: {message}")
            retry = threading.Timer(
                5,
                expire_reservation,
                args=(client_id, reservation_id),
            )
            timers[client_id] = retry
            retry.start()


def handle_client(connection, address):
    client_ip = address[0]

    try:
        data = connection.recv(1024).decode().strip()
        if not data:
            return

        parts = data.split("|")
        command = parts[0]

        if client_ip not in CLIENT_IPS.values():
            response = "REJECTED|Client IP is not allowed"

        elif command == "RESERVE":
            if len(parts) != 4:
                response = "REJECTED|Invalid request format"
            else:
                client_id = parts[1]

                if client_id not in CLIENT_IPS:
                    response = "REJECTED|Unknown client ID"
                elif CLIENT_IPS[client_id] != client_ip:
                    response = "REJECTED|Client ID does not match source IP"
                else:
                    try:
                        bandwidth = int(parts[2])
                        duration = int(parts[3])
                    except ValueError:
                        bandwidth = 0
                        duration = 0

                    with lock:
                        used = sum(
                            reservation["bandwidth"]
                            for reservation in reservations.values()
                        )
                        available = TOTAL_BANDWIDTH - used

                        if client_id in reservations:
                            response = "REJECTED|Client already has a reservation"
                        elif bandwidth <= 0 or duration <= 0:
                            response = "REJECTED|Invalid bandwidth or duration"
                        elif bandwidth > available:
                            response = "REJECTED|Insufficient bandwidth"
                        else:
                            ok, message = call_policy("reserve", client_ip)

                            if not ok:
                                response = f"REJECTED|Policy installation failed|{message}"
                            else:
                                reservation_id = uuid.uuid4().hex[:12]
                                reservations[client_id] = {
                                    "bandwidth": bandwidth,
                                    "reservation_id": reservation_id,
                                }

                                timer = threading.Timer(
                                    duration,
                                    expire_reservation,
                                    args=(client_id, reservation_id),
                                )
                                timers[client_id] = timer
                                timer.start()

                                response = (
                                    f"ACCEPTED|{client_id}|{bandwidth}|{reservation_id}"
                                )

        elif command == "RELEASE":
            if len(parts) != 2:
                response = "REJECTED|Invalid request format"
            else:
                client_id = parts[1]

                if client_id not in CLIENT_IPS:
                    response = "REJECTED|Unknown client ID"
                elif CLIENT_IPS[client_id] != client_ip:
                    response = "REJECTED|Client ID does not match source IP"
                else:
                    with lock:
                        reservation = reservations.get(client_id)

                        if reservation is None:
                            response = "REJECTED|No active reservation"
                        else:
                            ok, message = call_policy("release", client_ip)

                            if not ok:
                                response = f"REJECTED|Policy removal failed|{message}"
                            else:
                                timer = timers.pop(client_id, None)
                                if timer:
                                    timer.cancel()

                                del reservations[client_id]
                                response = (
                                    f"RELEASED|{client_id}|"
                                    f"{reservation['reservation_id']}"
                                )

        elif command == "STATUS":
            with lock:
                used = sum(
                    reservation["bandwidth"]
                    for reservation in reservations.values()
                )
                available = TOTAL_BANDWIDTH - used

            response = (
                f"TOTAL={TOTAL_BANDWIDTH}|USED={used}|AVAILABLE={available}"
            )

        else:
            response = "REJECTED|Unknown command"

        connection.sendall(response.encode())

    except (ConnectionResetError, BrokenPipeError):
        print(f"Connection lost: {address}")
    except Exception as error:
        print(f"Request error from {address}: {error}")
    finally:
        connection.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Reservation server running on {HOST}:{PORT}")
        print(f"Total reservation capacity: {TOTAL_BANDWIDTH} Mbps")

        while True:
            connection, address = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(connection, address),
                daemon=True,
            )
            thread.start()


if __name__ == "__main__":
    main()

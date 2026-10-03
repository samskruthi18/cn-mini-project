import socket
import threading

HOST = "0.0.0.0"
PORT = 5000
TOTAL_BANDWIDTH = 100

reservations = {}
timers = {}
lock = threading.Lock()


def expire_reservation(client_id):
    with lock:
        if client_id in reservations:
            del reservations[client_id]
            timers.pop(client_id, None)
            print(f"Reservation expired: {client_id}")


def handle_client(conn, addr):
    print(f"Connected: {addr}")

    try:
        while True:
            data = conn.recv(1024).decode().strip()

            if not data:
                break

            print(f"Request from {addr}: {data}")

            parts = data.split("|")
            command = parts[0]

            if command == "RESERVE":
                if len(parts) != 4:
                    conn.sendall(b"REJECTED|Invalid request format")
                    continue

                client_id = parts[1]

                try:
                    bandwidth = int(parts[2])
                    duration = int(parts[3])
                except ValueError:
                    conn.sendall(b"REJECTED|Invalid bandwidth or duration")
                    continue

                with lock:
                    used_bandwidth = sum(reservations.values())
                    available_bandwidth = TOTAL_BANDWIDTH - used_bandwidth

                    if client_id in reservations:
                        response = "REJECTED|Client already has a reservation"

                    elif bandwidth <= 0 or duration <= 0:
                        response = "REJECTED|Invalid bandwidth or duration"

                    elif bandwidth <= available_bandwidth:
                        reservations[client_id] = bandwidth

                        timer = threading.Timer(
                            duration,
                            expire_reservation,
                            args=(client_id,)
                        )

                        timers[client_id] = timer
                        timer.start()

                        response = f"ACCEPTED|{client_id}|{bandwidth}"

                    else:
                        response = "REJECTED|Insufficient bandwidth"

                conn.sendall(response.encode())

            elif command == "RELEASE":
                if len(parts) != 2:
                    conn.sendall(b"REJECTED|Invalid request format")
                    continue

                client_id = parts[1]

                with lock:
                    if client_id in reservations:
                        del reservations[client_id]

                        if client_id in timers:
                            timers[client_id].cancel()
                            del timers[client_id]

                        response = f"RELEASED|{client_id}"

                    else:
                        response = "REJECTED|No active reservation"

                conn.sendall(response.encode())

            elif command == "STATUS":
                with lock:
                    used_bandwidth = sum(reservations.values())
                    available_bandwidth = TOTAL_BANDWIDTH - used_bandwidth

                response = (
                    f"TOTAL={TOTAL_BANDWIDTH}|"
                    f"USED={used_bandwidth}|"
                    f"AVAILABLE={available_bandwidth}"
                )

                conn.sendall(response.encode())

            else:
                conn.sendall(b"REJECTED|Unknown command")

    except ConnectionResetError:
        print(f"Connection lost: {addr}")

    finally:
        conn.close()
        print(f"Disconnected: {addr}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()

print(f"Server running on {HOST}:{PORT}")
print(f"Total bandwidth: {TOTAL_BANDWIDTH} Mbps")

while True:
    conn, addr = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )

    thread.start()
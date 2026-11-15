import socket

SERVER_HOST = "10.0.0.3"
SERVER_PORT = 5000
CLIENT_ID = "C2"


def send_request(request):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    client.sendall(request.encode())

    response = client.recv(1024).decode()
    print("Server:", response)

    client.close()


while True:
    print("\n1. Reserve bandwidth")
    print("2. Release reservation")
    print("3. Check status")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        bandwidth = input("Enter bandwidth (Mbps): ")
        duration = input("Enter duration (seconds): ")

        request = f"RESERVE|{CLIENT_ID}|{bandwidth}|{duration}"
        send_request(request)

    elif choice == "2":
        request = f"RELEASE|{CLIENT_ID}"
        send_request(request)

    elif choice == "3":
        send_request("STATUS")

    elif choice == "4":
        break

    else:
        print("Invalid choice")
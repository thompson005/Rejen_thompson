import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(1)

    print("Server listening on port 12345...")

    client_socket, client_address = server_socket.accept()
    print("Connection from:", client_address)

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print("Received:", data)

        if "malicious" in data.lower():
            response = "Malicious activity detected. Disconnecting..."
            client_socket.send(response.encode('utf-8'))
            client_socket.close()
            break
        else:
            response = f"Server received: {data}"
            client_socket.send(response.encode('utf-8'))

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()


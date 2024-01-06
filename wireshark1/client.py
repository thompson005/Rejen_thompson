import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        client_socket.send(message.encode('utf-8'))

        if message.lower() == 'exit':
            break

        response = client_socket.recv(1024).decode('utf-8')
        print("Server response:", response)

    client_socket.close()

if __name__ == "__main__":
    start_client()


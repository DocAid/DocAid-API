import socket


if __name__ == '__main__':
    host = socket.gethostname()
    port = 5500

    client = socket.socket()
    client.connect((host, port))
    while True:
        client.send("Hello".encode())
        data = client.recv(2048).decode()

        if data:
            print(data)
            client.close()
            break

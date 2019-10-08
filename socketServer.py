import socket
import _thread


def new_client(client, addr, clientID):
    while True:
        data = client.recv(2048)
        if data:
            print(data.decode())
        if clientID != 1:
            client.send("Hello".encode())
    client.close()


def main():
    clientID = 0
    # get the hostname
    host = socket.gethostname()
    port = 5500

    server = socket.socket()
    server.bind((host, port))
    server.listen(3)
    print("Server started. Listening on port: ", port)

    while True:
        c, addr = server.accept()
        clientID += 1
        if clientID == 1:
            print("Connected to API: ", addr)
        _thread.start_new_thread(new_client, (c, addr, clientID))
    server.close()


if __name__ == '__main__':
    while True:
        main()

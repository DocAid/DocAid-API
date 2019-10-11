import socket
import _thread
import pickle


def new_client(client, addr, clientID, clients):
    while True:
        try:
            data = pickle.loads(client.recv(2048))
        except EOFError:
            pass
        else:
            print(data, " : ", clientID)
            if clientID == 1:
                c = clients[-1][0]
                c.send(pickle.dumps(data))
                del clients[-1]
    client.close()


def main():
    clients = []
    clientID = -1
    # get the hostname
    # host = socket.gethostname()
    host = "34.93.126.224"

    port = 5500

    server = socket.socket()
    server.bind((host, port))
    server.listen(3)
    print("Server started. Listening on port: ", port)

    while True:
        c, addr = server.accept()

        clientID += 1
        if clientID != 0:
            clients.append((c, addr))

        print("Length: ", len(clients))
        if clientID == 1:
            print("Connected to API: ", addr)
        _thread.start_new_thread(new_client, (c, addr, clientID, clients))
    server.close()


if __name__ == '__main__':
    while True:
        main()

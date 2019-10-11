import socket
import pickle

if __name__ == '__main__':
    # host = "34.93.231.96"
    host = socket.gethostname()
    port = 5500

    client = socket.socket()
    client.connect((host, port))
    while True:
        client.send(pickle.dumps({"Hello": "World"}))
        data = pickle.loads(client.recv(2048))

        if data:
            print(data)
            client.close()
            break

import socket


def connect_to_client(data):
    pass  # Send data to client


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5500  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(3)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if data:
            print("from connected user: ", str(data))

            # This function will do the socket server to socket client task
            connect_to_client(data)

            conn.close()
            break  # close the connection


if __name__ == '__main__':
    while True:
        server_program()

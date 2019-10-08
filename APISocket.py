from flask import Flask, request
import socket


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    data = request.json
    data = data['uid']
    print(data)
    # data = "HELLO"
    client.send(data.encode())

    return "Hello World"


if __name__ == '__main__':
    host = socket.gethostname()
    port = 5500

    client = socket.socket()
    client.connect((host, port))
    app.run(host='127.0.0.1', port=5000, debug=True)

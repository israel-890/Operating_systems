import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 12345

def send_to_server(query, client_socket):
    client_socket.sendall(query.encode('utf-8'))
    print(f"Your request {query} is being printed right now in the server terminal. Go there and see the result print!")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        while True:
            query = input("Enter your query: ")
            t = Thread(target=send_to_server, args=(query, client_socket,))
            t.start()
            # data = client_socket.recv(1024)
            # print(data.decode('utf-8'))

if __name__ == '__main__':
    main()

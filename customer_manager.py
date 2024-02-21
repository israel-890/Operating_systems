import socket

HOST = '127.0.0.1'
PORT = 12345

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
    while True:
        query = input("Enter your query: ")
        client_socket.sendall(query.encode('utf-8'))
        data = client_socket.recv(1024)
        print(data.decode('utf-8'))

if __name__ == '__main__':
    main()

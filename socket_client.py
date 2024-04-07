
import socket

UDP_HOST = '127.0.0.1'
UDP_PORT = 5000

def client_socket(host, port):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.connect((host, port))
    message = input('>>> ')

    while message.lower().strip() != 'quit':
        client_sock.send(message.encode())
        msg = client_sock.recv(1024).decode()
        print(f"Received message {msg}")
        message = input('>>> ')

    client_sock.close()



if __name__ == '__main__':
    client_socket(UDP_HOST, UDP_PORT)




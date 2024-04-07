import socket
import json
import urllib.parse

from datetime import datetime

UDP_HOST = '127.0.0.1'
UDP_PORT = 5000
def run_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f'Received data: {data.decode()} from: {address}')
            date_parse = urllib.parse.unquote_plus(data.decode())
            print(date_parse)
            date_now = datetime.now()
            with open('storage/data.json', 'r') as file:
                current_data = json.loads(file.read())
            data_dict = {key: value for key, value in [el.split('=') for el in date_parse.split('&')]}
            current_data[date_now.strftime("%Y-%m-%d %H:%M:%S")] = data_dict
            with open('storage/data.json', 'w', encoding='utf-8') as file:
                json.dump(current_data, file, ensure_ascii=False, indent=4)
            sock.sendto(data, address)
            print(f'Send data: {data.decode()} to: {address}')

    except KeyboardInterrupt:
        print(f'Close server')
    finally:
        sock.close()


if __name__ == '__main__':
    run_server(UDP_HOST, UDP_PORT)

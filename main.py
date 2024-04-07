
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from pathlib import Path
import mimetypes
import socket
import threading
import logging
from datetime import datetime
import json

BASE_DIR = Path()
UDP_HOST = 'localhost'
UDP_PORT = 5000
HTTP_HOST = 'localhost'
HTTP_PORT = 3000


class ServerMain(BaseHTTPRequestHandler):

    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:#if
            case '/':
                self.send_html('index.html')
            case '/message':
                self.send_html('message.html')
            case _: 
                file = BASE_DIR.joinpath(route.path[1:]) 
                if file.exists(): 
                    self.send_static(file)
                else:
                    self.send_html('error.html', 404)

    def do_POST(self):
        size = self.headers.get('Content-Length')
        data = self.rfile.read(int(size))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (UDP_HOST, UDP_PORT))
        sock.close()
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-Type', mime_type)
        else:  
            self.send_header('Content-Type', 'text/plaine')  
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())        

def run_server(host, port):
    address = (host, port)
    http_server = HTTPServer(address, ServerMain)
    logging.info("Starting http server")
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        http_server.server_close()

def save_data(data):
    data_parse = data.decode()
    current_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open('storage/data.json', 'r', encoding='utf-8') as file:
            data_dict = json.loads(file.read())
    except FileNotFoundError:
        data_dict = {}
    result_dict = {current_data: {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}}
    data_dict.update(result_dict)
    with open('storage/data.json', 'w', encoding='utf-8') as file:
        json.dump(data_dict, file, ensure_ascii=False, indent=4)
    print(data_dict)

def run_udp_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    logging.info("Starting socket server")
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"Received UDP data: {data.decode()} from: {addr}")
            save_data(data)
    except KeyboardInterrupt:
        sock.close()

if __name__== '__main__':
    #run_server()
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    server = threading.Thread(target=run_server, args=(HTTP_HOST, HTTP_PORT))
    server_upd = threading.Thread(target=run_udp_server, args=(UDP_HOST, UDP_PORT))

    server.start()
    server_upd.start()

    # server.join()
    # server_upd.join()

    print('Done!')
import socket
import os
import subprocess
import threading
import json

class SocketServer():
    def __init__(self):
        self.host = '192.168.1.146'  # Server IP address
        self.socket_port = 8000  # Port number
        self.server_socket = None
        self.client_socket = None
        self.addr = None
        self.frame_width = None
        self.frame_height = None
        self.framerate = None
        self.tcp_port = 8888
        self.tcp_path = f'tcp://127.0.0.1:{self.tcp_port}'
        self.key = None
        
    def Open_TCP_server(self) -> None:
        command = f"libcamera-vid -n -t 0 --width {self.frame_width} --height {self.frame_height} --framerate {self.framerate} --inline --listen -o {self.tcp_path}"
        print(command)
        subprocess.call(command, shell=True)
    
    def handle_client(self):
        while True:
            # Receive data from the client
            data = self.client_socket.recv(1024)
            if not data:
                break

            # Print the received data
            decode = json.loads(data.decode())
            print('Received data:', decode)
            self.key = decode['key']
            # Check if the received data is 'q'
            if self.key.strip() == 'q':
                # Call your specific function here
                self.frame_width = int(decode['width'])
                self.frame_height = int(decode['height'])
                self.framerate = int(decode['framerate'])
                tcp_thread = threading.Thread(target=self.Open_TCP_server)
                tcp_thread.start()
                self.client_socket.sendall('TCP_Server started.'.encode())
            # Send a response to the client
            else:
                self.client_socket.sendall('Done.'.encode())

        self.client_socket.close()
        print('Connection with the client has been terminated:', self.addr)
        self.server_socket.close()
        print('Server is shutting down')
        self.release_port()
        self.restart_server()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.socket_port))
        self.server_socket.listen(1)  # Maximum number of waiting clients
        print('Server has started.')
        while True:
            self.client_socket, self.addr = self.server_socket.accept()
            print('Client has connected:', self.addr)
            self.handle_client()

    def restart_server(self):
        # Function to restart the server after it's shut down
        print('Restarting the server')
        self.start_server()

    def release_port(self):
        command = f"lsof -ti:{self.socket_port} | xargs kill"
        os.system(command)

if __name__ == '__main__':
    socket_server = SocketServer()
    socket_server.start_server()

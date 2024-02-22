import socket
import threading
import subprocess

class SocketServer():
    def __init__(self):
        self.host = '192.168.1.146'  # Server IP address
        self.socket_port = 8000  # Port number
        self.server_socket = None
        self.client_socket = None
        self.addr = None
        self.frame_width = 720
        self.frame_height = 640
        self.framerate = 30
        self.tcp_port = 8888
        self.tcp_path = f'tcp://127.0.0.1:{self.tcp_port}'

    def handle_client(self):
        # Receive data from the client
        data = self.client_socket.recv(1024)
        if not data:
            self.client_socket.close()
            print('Connection with the client has been terminated.')
            return

        # Print the received data
        print('Received data:', data.decode())

        # Check if the received data is 'q'
        if data.decode().strip() == 'q':
            # Call your specific function here
            self.start_tcp_server()
            self.client_socket.sendall('TCP Server started.'.encode())
        # Send a response to the client
        else:
            self.client_socket.sendall('Done.'.encode())

        self.client_socket.close()

    def start_tcp_server(self):
        # Start your TCP server here
        command = f"libcamera-vid -n -t 0 --width {self.frame_width} --height {self.frame_height} --framerate {self.framerate} --inline --listen -o {self.tcp_path}"
        print(command)
        subprocess.call(command, shell=True)

    def start_socket_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.socket_port))
        self.server_socket.listen(1)  # Maximum number of waiting clients
        print('Socket server has started.')

        while True:
            self.client_socket, addr = self.server_socket.accept()
            print('Client has connected:', addr)

            # Create a separate thread for each client
            client_thread = threading.Thread(target=self.handle_client)
            client_thread.start()

    def start_server(self):
        # Start the socket server in the main thread
        self.start_socket_server()

if __name__ == '__main__':
    socket_server = SocketServer()
    socket_server.start_server()

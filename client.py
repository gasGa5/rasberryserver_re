import socket

HOST = '192.168.1.121'  
PORT = 8888  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    message = input('input message: ')
    s.sendall(message.encode())
    data = s.recv(1024)
    print('server_data:', data.decode())

s.close()

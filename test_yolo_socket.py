import socket
from ultralytics import YOLO
import cv2

HOST = '192.168.1.121'  
PORT = 8888  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

model = YOLO('yolov8n.pt')
results = model.predict('tcp://127.0.0.1:8888', stream=True)

while True:
    for result in results:
        #box = result.boxes
        data = result.plot()
        s.sendall(data.encode())
        server_data = s.recv(1024)
        print('server_data:', server_data.decode())
        #cv2.imshow('Detection', plot)
        
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
#cv2.destroyAllWindows()

s.close()

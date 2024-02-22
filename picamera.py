from ultralytics import YOLO
import cv2
import subprocess
import json
import threading

class TCP_stream():
    def __init__(self, tcp_path, model_path, frame_width, frame_height, framerate, conf_thre, frame) -> None:
        self.tcp_path = tcp_path
        self.model_path = model_path
        self.model = YOLO(model_path)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.framerate = framerate
        self.conf_thre = conf_thre
        self.frame = frame
        
    def Open_TCP_server(self,) -> None:
        command = f"libcamera-vid -n -t 0 --width {self.frame_width} --height {self.frame_height} --framerate {self.framerate} --inline --listen -o {self.tcp_path}"
        subprocess.call(command, shell=True)
    
    def stream(self,):
        results = self.model.predict(self.tcp_path, imgsz = (self.frame_width,self.frame_height),
                                                   conf = self.conf_thre, stream=True)
        
        while True:
            for detection in results:
                plot = detection.plot()
                if self.detection_check(detection):
                    for objects in detection.boxes.data.tolist():
                            xmin, ymin, xmax, ymax, label, conf = self.data_extract(objects)                      
                            json_data = self.create_json(xmin, ymin, xmax, ymax, label, conf)
                            print(json_data)
                # 영상 보여주기
                cv2.imshow('Object Detection', plot)

                # 'q' 키를 누르면 종료
            if self.stop_key('q'):
                break

        cv2.destroyAllWindows()
    
    def detection_check(self, detection) -> bool:
        if detection.boxes.conf.numel() > 0:
            return True
        else:
            return False
        
    def data_extract(self, object):        
        xmin, ymin, xmax, ymax = int(object[0]), int(object[1]), int(object[2]), int(object[3])
        conf = float(object[4])
        label = int(object[5])
        return xmin, ymin, xmax, ymax, label, conf 
    
    def stop_key(self,key):
        if cv2.waitKey(self.frame) & 0xff == ord(key):
            return True
    
    def create_json(self, xmin, ymin, xmax, ymax, label, conf):
        data = {
        'label': label,
        'conf': conf,
        'box': [xmin, ymin, xmax, ymax]
    }   
        json_data = json.dumps(data)   
         
        return json_data     
    
if __name__ == "__main__":
    WEIGHT_PATH = './yolov8n.pt'
    VEDIO_PATH = 0
    CONFIDENCE_THRESHOLD = 0.3
    FRAME_WIDTH = 364
    FRAME_HEIGHT = 320
    FRAME_RATE = 2
    FRAME = 2
    WAIT_TIME = 0.1
    TCP_PATH = 'tcp://127.0.0.1:8888'
    
    TCP_server = TCP_stream(tcp_path=TCP_PATH, model_path=WEIGHT_PATH, frame_width=FRAME_WIDTH, 
                            frame_height=FRAME_HEIGHT, framerate=FRAME_RATE, 
                            conf_thre=CONFIDENCE_THRESHOLD, frame = FRAME)
    
    # Open_TCP_server() 함수를 스레드로 실행
    tcp_thread = threading.Thread(target=TCP_server.Open_TCP_server)
    tcp_thread.start()
    
    # stream() 함수를 메인 스레드에서 실행
    TCP_server.stream()

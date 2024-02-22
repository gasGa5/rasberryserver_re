from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
results = model.predict('tcp://127.0.0.1:8888', imgsz = (192,256), stream=True)

while True:
    for result in results:
        box = result.boxes
        plot = result.plot()
        cv2.imshow('Detection', plot)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()

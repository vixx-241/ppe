import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import cvzone
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)  # Relay 1
GPIO.setup(24, GPIO.OUT)  # Relay 2
GPIO.setup(17, GPIO.OUT)  # Buzzer
GPIO.setup(27, GPIO.OUT)  # Red LED
GPIO.setup(22, GPIO.OUT)  # Green LED

model=YOLO('/home/ppe/Documents/best.pt')

GPIO.output(17, GPIO.HIGH)
time.sleep(0.125)
GPIO.output(17, GPIO.LOW)
time.sleep(0.125)
GPIO.output(17, GPIO.HIGH)
time.sleep(0.125)
GPIO.output(17, GPIO.LOW)
time.sleep(0.125)
GPIO.output(17, GPIO.HIGH)
time.sleep(0.125)
GPIO.output(17, GPIO.LOW)
time.sleep(0.125)
GPIO.output(17, GPIO.HIGH)
time.sleep(0.125)
GPIO.output(17, GPIO.LOW)


#def RGB(event, x, y, flags, param):
#    if event == cv2.EVENT_MOUSEMOVE :  
#        colorsBGR = [x, y]
        #print(colorsBGR)
        

#cv2.namedWindow('RGB')
#cv2.setMouseCallback('RGB', RGB)

cap=cv2.VideoCapture(0)


my_file = open("/home/ppe/Documents/classes.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)

count=0




while True:
#    time.sleep(5)
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(500,480))
   

    results=model.predict(frame)
#    print(results)
    a=results[0].boxes.boxes
    px=pd.DataFrame(a).astype("float")
#    print(px)
    list=[]         
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if c == 'hat':

#            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),1)
#            cvzone.putTextRect(frame, f'{c}', (x1,y1),1,1)
            
            #Turn on green LED
            GPIO.output(22, GPIO.HIGH)
            
            #2 short beeps
            GPIO.output(17, GPIO.HIGH)
            time.sleep(0.125)
            GPIO.output(17, GPIO.LOW)
            time.sleep(0.125)
            GPIO.output(17, GPIO.HIGH)
            time.sleep(0.125)
            GPIO.output(17, GPIO.LOW)
            
             # Turn on the relays
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(23, GPIO.HIGH)
            
            time.sleep(5)
            
            GPIO.output(24, GPIO.LOW)
            GPIO.output(23, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            print('Helmet Detected')
            time.sleep(5)
        else:
            if c == 'person':
                
#                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),1)
#                cvzone.putTextRect(frame, f'{c}', (x1,y1),1,1)
                
                # Turn on the buzzer
                GPIO.output(17, GPIO.HIGH)
                # Turn on the red LED
                GPIO.output(27, GPIO.HIGH)
                time.sleep(5)
                GPIO.output(17, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)
                print('No Helmet Detected')
                time.sleep(5)
            else:
                # The object is not a face or a helmet
                # Do nothing
                print('Just passing by')
                pass


#    cv2.imshow("RGB", frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()


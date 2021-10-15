import numpy as np
import cv2
import datetime

cap = cv2.VideoCapture('video.avi')

#verificar codecs http://fourcc.org/codecs.php
fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter('output.avi', fourcc, 30.0, (240,320))

print(cap.isOpened)

def click_event(event, x, y, flags, param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print(x,' , ',y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x) + ' , '+str(y)
        cv2.putText(img, strXY, (x,y), font, 1, (255, 255, 0), 2)
        cv2.imshow('image', img)
        
img = np.zeros((512,512,3), np.uint8)
cv2.imshow('image', img)

cv2.setMouseCallback('image', click_event)


while (cap.isOpened()):
    ret, frame = cap.read()
    #verifica se o frame é true or false
    if ret==True :
        text = 'Width: '+ str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) + ' Height: '+str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        datet = str(datetime.datetime.now())
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, datet, (100,20), font, 0.2, (0,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame, text, (10,20), font, 0.2, (0,255,255), 1, cv2.LINE_AA)
        out.write(frame)
        
        #frame = cv2.line(frame, (0,0), (255,255), (255, 0 ,0), 10)
    
        cv2.imshow('frame', frame) 
        cv2.setMouseCallback('frame', click_event)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        cv2.waitKey(0)
        break
        
cap.release()
out.release()

cv2.destroyAllWindows()
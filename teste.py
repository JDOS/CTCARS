# OpenCV Python program to detect cars in video frame
# import libraries of python OpenCV 
import cv2
import numpy as np

largura_min = 20
altura_min = 20
#pos_linha=160
pos_linha=420
offset=4 #Erro permitido entre pixel 
carros= 0
carros2= 0

detec = []
detec2 = []

# capture frames from a video
cap = cv2.VideoCapture('video.avi')
 
# Trained XML classifiers describes some features of some object we want to detect
car_cascade = cv2.CascadeClassifier('cars.xml')
frame_count = 0
history_cars = {}
poligono = []

def click_event(event, x, y, flags, param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print(x,' , ',y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x) + ' , '+str(y)
        cv2.putText(frames, strXY, (x,y), font, 1, (255, 255, 0), 2)
        cv2.imshow('video', frames)
        
 
def click_event_poligono(event, x, y, flags, param):
    if event==cv2.EVENT_LBUTTONDOWN:
        cv2.circle(frames, (x,y), 3, (0,0,255), -1)
        points.append((x,y))
        if len(points) >= 2:
            cv2.line(frames, points[-1], points[-2], (255,0,0), 5)
        cv2.imshow('video', frames)

def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy
    
def nothing(x):
    print(x)
    
#subtrai imagem que está em movimento
subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()

# loop runs if capturing has been initialized.
while (cap.isOpened()):
    # reads frames from a video
    ret, frames = cap.read()
    if ret == True: 
        #contagem de frames
        frame_count+=1
        
        text_count = 'Frame: '+str(frame_count)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frames, text_count, (10,20), font, 0.5, (0,255,255), 1, cv2.LINE_AA)
        
        #linha de contagem
        
        cv2.line(frames, (0, pos_linha), (1200, pos_linha), (153, 50, 168), 3) 
        
        
        # convert to gray scale of each frames
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
        img_sub = subtracao.apply(frames)
        dilat = cv2.dilate(img_sub,np.ones((5,5)))
        #cria uma matriz 5x5 dentro forma uma elipse
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        #tenta preencher os buracos dos carros x2 (tentativa e erro)
        dilatada = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
        #pega todos os contornos da dilatação
        contorno,img = cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        #enumera todos os contornos
        for(i,c) in enumerate(contorno):
            if poligono:
                #cria um retangulo em cada contorno detectado
                (x,y,w,h) = cv2.boundingRect(c) 
                #como o objeto dilatado pode ter buracos utiliza/verifica a dimenção do quadrado é de um carro
                validar_contorno = (w >= largura_min) and (h >= altura_min)
                if not validar_contorno:
                    continue
                    
                #pega o centro do retangulo
                centro = pega_centro(x, y, w, h)
                result = cv2.pointPolygonTest(np.mat(poligono), centro, False)
                
                if(result>=0):
                    cv2.circle(frames, centro, 4, (255, 0,0), -1)
                    #desenha um retangulo no frame
                    cv2.rectangle(frames,(x,y),(x+w,y+h),(0,255,0),1)    

                    #concatena
                    detec.append(centro)
                    #desenha um circulo vermelho no cento
                    cv2.circle(frames, centro, 4, (0, 0,255), -1)
        
        #verifica se o circulo vermelho passo pela linha definida
        for (x,y) in detec:
            #verifica se passou da linha com uma margem de erro offset
            if y<(pos_linha+offset) and y>(pos_linha-offset):
                carros+=1
                #muda a cor da linha para demonstrar a contagem
                cv2.line(frames, (0, pos_linha), (1200, pos_linha), (0,127,255), 3)  
                #remove para não contar duas vezes
                detec.remove((x,y))
                print("Carros detectados até o momento: "+str(carros))
        
        #posta na tela quantidade de veiculos
        cv2.putText(frames, "VEICULOS: "+str(carros), (10, 90), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255),2)
        
        cv2.imshow("Detectar",dilatada)
        cv2.setMouseCallback('video', click_event) 
        
        #desenha poligono salvo
        if len(poligono)>=5:
            pts = np.array([poligono], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frames, [pts], True, (0,255,255), 2)

        # Detects cars of different sizes in the input image
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)
         
        # To draw a rectangle in each cars
        i=0
        for i,(x,y,w,h) in enumerate(cars):
            if poligono:
                centro = pega_centro(x,y,w,h)
                result = cv2.pointPolygonTest(np.mat(poligono), centro, False)
                if(result>=0):
                    cv2.circle(frames, centro, 4, (255, 0,0), -1)
                    #concatena
                    detec2.append(centro)
            else:
                cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)
            
        text_carros = 'Cars: '+ str(len(cars))   
        cv2.putText(frames, text_carros, (10,40), font, 0.5, (0,255,255), 1, cv2.LINE_AA)        

      
        #verifica se o circulo azul passo pela linha definida
        for (x,y) in detec2:
            #verifica se passou da linha com uma margem de erro offset
            if y<(pos_linha+offset) and y>(pos_linha-offset):
                carros2+=1
                #muda a cor da linha para demonstrar a contagem
                cv2.line(frames, (0, pos_linha), (1200, pos_linha), (0,127,255), 3)  
                #remove para não contar duas vezes
                detec2.remove((x,y))
                print("Carros detectados até o momento: "+str(carros))
      
        #posta na tela quantidade de veiculos
        cv2.putText(frames, "VEICULOS: "+str(carros2), (10, 70), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 0),2)
      
      
        # Display frames in a window 
        cv2.imshow('video', frames)
        
        #line 'l'
        if cv2.waitKey(33) == ord('l'):
            cv2.putText(frames, '||', (300,20), font, 1, (0,255,255), 2, cv2.LINE_AA)
            cv2.createTrackbar('lineCount', 'video', 0, int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),nothing)
            print('pause')
         
            while(cv2.waitKey(20)!= ord('l')):
                
                line = cv2.getTrackbarPos('lineCount', 'video')
                cv2.line(frames, (0, line), (1200, line), (0,127,255), 3)  
                cv2.imshow('video', frames)
                #press esc to scape
                if cv2.waitKey(20) == 27:
                    break
                #press 's' to save
                if cv2.waitKey(20) == ord('s'):
                    pos_linha = cv2.getTrackbarPos('lineCount', 'video')
                    cv2.putText(frames, 'SALVO!',(100,30), font, 1, (0,255,255), 1, cv2.LINE_AA)
                    cv2.imshow('video', frames)
        
        
        
        #pause 'p' 
        if cv2.waitKey(33) == ord('p'):
            cv2.putText(frames, '||', (300,20), font, 1, (0,255,255), 2, cv2.LINE_AA)
            points =[]
            print('pause')
            cv2.imshow('video', frames)
            
            
            while(cv2.waitKey(20)!= ord('p')):
                cv2.setMouseCallback('video', click_event_poligono) 
                cv2.imshow('video', frames)
                #press esc to scape
                if cv2.waitKey(20) == 27:
                    break
                #press 's' to save
                if cv2.waitKey(20) == ord('s'):
                    print('salvo!')
                    poligono = points
                    cv2.putText(frames, 'SALVO!',(100,30), font, 1, (0,255,255), 1, cv2.LINE_AA)
                    cv2.imshow('video', frames)
                    
            #cv2.waitKey(0)
            
            
        # Wait for Esc key to stop
        if cv2.waitKey(33) == 27:
            break
    else:
        cv2.waitKey(0)
 
# De-allocate any associated memory usage
cv2.destroyAllWindows()
import cv2
import numpy as np
from time import sleep

largura_min=40 #Largura minima do retangulo
altura_min=40 #Altura minima do retangulo

offset=2 #Erro permitido entre pixel  

pos_linha=550 #Posição da linha de contagem 

delay= 60 #FPS do vídeo

detec = []
carros= 0

	
def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture('video.mp4')

#subtrai imagem que está em movimento
subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()

car_cascade = cv2.CascadeClassifier('cars.xml')
while True:
    #pega cada frame do video
    ret , frame1 = cap.read()
    #verifica exatamente a velocidade do video
    tempo = float(1/delay)
    sleep(tempo) 
    #transforma o frame em preto e branco
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    #tira as imperfeições da imagem
    blur = cv2.GaussianBlur(grey,(3,3),5)
    #subtrai a imagem em movimento e estática
    img_sub = subtracao.apply(blur)
    #aumenta o objeto subtraido 
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    #cria uma matriz 5x5 dentro forma uma elipse
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    #tenta preencher os buracos dos carros x2 (tentativa e erro)
    dilatada = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
    dilatada = cv2.morphologyEx (dilatada, cv2. MORPH_CLOSE , kernel)
    #pega todos os contornos da dilatação
    contorno,img = cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #linha de contagem
    cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255,127,0), 3) 
    
    #gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    #cars = car_cascade.detectMultiScale(dilatada, 1.1, 1)
    
    #for (x,y,w,h) in cars:
        #cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,0,255),2)
        #centro = pega_centro(x, y, w, h)
        #detec.append(centro)
        #cv2.circle(frame1, centro, 4, (0, 0,255), -1)
    
    #enumera todos os contornos
    for(i,c) in enumerate(contorno):
        #cria um retangulo em cada contorno detectado
        (x,y,w,h) = cv2.boundingRect(c) 
        #como o objeto dilatado pode ter buracos utiliza verifica a dimenção do quadrado é de um carro
        validar_contorno = (w >= largura_min) and (h >= altura_min)
        if not validar_contorno:
            continue
        #desenha um retangulo no frame
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),-1)    
        #pega o centro do retangulo
        centro = pega_centro(x, y, w, h)
        #concatena
        detec.append(centro)
        #desenha um circulo vermelho no cento
        cv2.circle(frame1, centro, 4, (0, 0,255), -1)

        #verifica se o circulo vermelho passo pela linha definida
        for (x,y) in detec:
            #verifica se passou da linha com uma margem de erro offset
            if y<(pos_linha+offset) and y>(pos_linha-offset):
                carros+=1
                #muda a cor da linha para demonstrar a contagem
                cv2.line(frame1, (0, pos_linha), (1200, pos_linha), (0,127,255), 3)  
                #remove para não contar duas vezes
                detec.remove((x,y))
                print("Carros detectados até o momento: "+str(carros))        
    #posta na tela quantidade de veiculos
    cv2.putText(frame1, "VEICULOS: "+str(carros), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    #Mostra video original
    cv2.imshow("Video Original" , frame1)
    #Mostra video dilatado
    cv2.imshow("Detectar",dilatada)

    #apertar 'ESC' finaliza o programa
    if cv2.waitKey(1) == 27:
        break
    
cv2.destroyAllWindows()
cap.release()
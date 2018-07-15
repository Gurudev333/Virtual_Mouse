# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:29:08 2018

@author: Gurudeo
"""
import cv2
import numpy as np
from pynput.mouse import Button, Controller
#for wx functionalities
import wx
#for mouse control 
mouse=Controller()
#
app=wx.App(False) 
#ti get size of monitor
(sx,sy)=wx.GetDisplaySize()
intial=np.array([0,125])
lb=np.array([0,100,100])
ub=np.array([20,255,255])
#create open and closing operation on frames for noise removal
open_mask=np.ones((5,5))
close_mask=np.ones((20,20))
camerax,cameray=(420,320)

#Lest read image from camera
cam=cv2.VideoCapture(0);
cam.set(3,camerax)
cam.set(4,cameray)

#Store the captured image as frame
while True: 
    rest,image=cam.read()
    #lets resize image to proper formate 
    #image=cv2.resize(image,(280,180))
    #convert image to HSV formate
    imgage_HSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    #creates fillter that detect the colour value in lower bound and upper bound
    fitr=cv2.inRange(imgage_HSV,lb,ub)
    #on such filter perform noise removal  using open and close operation
    filtOpen=cv2.morphologyEx(fitr,cv2.MORPH_OPEN,open_mask)
    filtOpenClose=cv2.morphologyEx(filtOpen,cv2.MORPH_CLOSE,close_mask)
    filtFinal=filtOpenClose
    _, contours, _=cv2.findContours(filtOpenClose.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    if(len(contours)>=2):
        mouse.release(Button.left)
        x1,y1,w1,h1=cv2.boundingRect(contours[0])
        x2,y2,w2,h2=cv2.boundingRect(contours[1])
        cv2.rectangle(image,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(image,(x2,y2),(x2+w2,y2+h2 ),(255,0,0),2)
        mlx1=int(x1+w1/2)
        mly1=int(y1+h1/2)
        mlx2=int(x2+w2/2)
        mly2=int(y2+h2/2)
        cv2.line(image,(mlx1,mly1),(mlx2,mly2),(255,0,0),2)
        mlx=int((mlx1+mlx2)/2)
        mly=int((mly1+mly2)/2)
        cv2.circle(image,(mlx,mly),5,(0,0,255))
        mouse.position=(sx-mlx,mly)
        while mouse.position!=(sx-mlx,mly):
            pass
   
    
    elif(len(contours)==1):
        x,y,w,h=cv2.boundingRect(contours[0])
        mlx=int(x+w/2)
        mly=int(y+h/2)
        cv2.circle(image,(mlx,mly),int((w+h)/4),(0,0,255),2)
        mouse.position=(sx-mlx,mly)
        while mouse.position!=(sx-mlx,mly):
            pass
        mouse.press(Button.left)
   
    
    cv2.imshow("original",image)   
    cv2.waitKey(10)

        
            

    
    

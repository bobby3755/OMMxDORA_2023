#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:43:49 2022

@author: RyanFantasia
"""
import numpy as np
from PIL import Image
import argparse
import cv2

def disp_hist(file,perCol,perRow):

    
    #Get file paths
    sets=file+'trdir/histsets'
    filename=file+'trdir/hist2d'
    infor=file+'trdir/histpar'
    
    #open files
    fileptr = open(filename+'.stack','rb')
    fileptrSets = open(sets+'.list','rb')
    fileptrInfo = open(infor+'.info','rb')
    

    #Get Infor from files 
    frame = np.fromfile(fileptr,dtype='int32')
    histlist=np.fromfile(fileptrSets,dtype='int32')
    histinfo=np.fromfile(fileptrInfo,dtype='int32')
    histsearch=np.reshape(histlist,[len(histlist)//3,3])
    #print(frame.shape)
    #print(histlist.shape)
    #print(histinfo.shape)

    histnum=histinfo[3]  #number of histograms
    histrow=int(histnum//perCol) #number of histograms / number of histograms per col to give number per row 
    
    res=histinfo[0]   #get the 'res' as defined in 2D hist this is the size of the histogram 30x30


    
    
    #Openining the Histogram and making an Image. 
    fileptr.seek(0) #Get the first frame 

    result = Image.new('F', (histrow*res,perCol*res)) #make a new image of correct size 
    for j in range (0,histrow):    
        for i in range (0,perCol):
        #print((i+(j*histpercol)))
            fileptr.seek((i+(j*perCol))*res*res*4)  #open frame poisiton x resolution *32/8 (8 bit vs 32 bit)
            frame2 = np.fromfile(fileptr,dtype='int32',count=res*res)
            frame2 = np.reshape(frame2,[res,res])
            frame2 = np.transpose(frame2)
            frame2 = np.rot90(np.rot90(np.rot90(frame2)))
            frame2=frame2
            im2 =Image.fromarray(frame2)
        #print(i)
            result.paste(im2, box=((j*res),(i*res))) #load each histogram into the total histogram image. 
       
    
   

    img = np.array(result) 

    #result.show(result)
    avgnonzero = img[np.nonzero(img)].mean() #this might be bad practice 
    img=np.array((img/avgnonzero)*255).astype('uint8')#but here i am sclaing my image based on avg non zero to gray scale 
                                                        # This is only for display and it works fairly well but may be something that we want to return to. 



    

    grayImage = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  #Converts image to gray scale
    heatmap = cv2.applyColorMap(grayImage, cv2.COLORMAP_HOT)  #converst grey scale to color map magma 
    
    refPt = []
    
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            #print(x+(k*histperrow*30),",",y)
            imgpkdisp=[((x+(k*perRow*30))//30*perCol),y//30] #Converting X and y of click to position on histogram as a grid. K s frame number. Scale by 30 because of size of histogram. 
            imgpkdisp=sum(imgpkdisp)  # This is the exact histogram number. based off frame, and which position
            imgpkdisp=histsearch[imgpkdisp] # now we use that info to find the hisgram in the  info file 
            imgpkdisp=str(imgpkdisp)
            print(imgpkdisp)
            refPt.append([x+(k*perRow*30),y]) #This stores the histograms selected. 
            font = cv2.FONT_HERSHEY_SIMPLEX
            strXY = str(x+(k*perRow*30) )+", "+str(y)
            cv2.putText(imgcrop, imgpkdisp, (x,y), font, 0.5, (255,0,0), 2) #Draw coordinates on image. 
            cv2.imshow('2D Histogram [PK# t1 t2]',imgcrop)
    
    savePt=[]
    testvar=0
    t=img.size//((perCol*30)*perRow*30)
    
    k=0
    
    #Load in frames for searching
    while k < t:
        imgcrop=heatmap[0:(perCol*30),k*perRow*30:(k+1)*30*perRow]  #Display each frame as a heat map. 
        scale_percent = 200 # percent of original size
        width = int(imgcrop.shape[1] * scale_percent / 100)
        height = int(imgcrop.shape[0] * scale_percent / 100)
        dim = (width, height)
  
        # resize image
        resized = cv2.resize(imgcrop, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow('2D Histogram [PK# t1 t2]',imgcrop )
        cv2.namedWindow('2D Histogram [PK# t1 t2]')
        cv2.setMouseCallback('2D Histogram [PK# t1 t2]', click_event)
        key=cv2.waitKey(0)
        if key == 27: #if escape key break the loop
            break
        elif key==98:  # if b go backwards
            if k == 0:
                k=k
            else:
                k=k-1  # any other key go forward
        else:
            k=k+1
        
   # for k in range (0,t):
       # print(k)
       # imgcrop=heatmap[0:(perCol*30),k*perRow*30:(k+1)*30*perRow]
       # cv2.imshow('heatmap',imgcrop )
       # cv2.namedWindow('heatmap')
       # cv2.setMouseCallback("heatmap", click_event)
       # key=cv2.waitKey(0)
        #if key == 27:
        #    break
        #elif key == 98:
            #print(k)
        
        
            
    cv2.destroyAllWindows()
    refptnp=np.array(refPt)  #stored histogram positions
    #print(refptnp)
    refsc=refptnp//30     # scale to histogram number per frame
    refcol=refsc*[perCol,1]  # Scale to be histogram number on right frame 
    sum_of_rows = np.sum(refcol, axis = 1)  #sum to get historgram number
    out=histsearch[sum_of_rows] #search  histogram info to get pk# and T1 T2. 
    return refptnp , refsc , refcol ,sum_of_rows , out   #Return Relevant vars. 

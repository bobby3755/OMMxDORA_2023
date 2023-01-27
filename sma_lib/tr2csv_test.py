# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 16:56:18 2021

@author: rfantasia
"""
from loadtrace import load_trace
import numpy as np
path='C:/Users/rfantasia/anacondaProjects/ffp/'
filename='2021-10-07_ORBIT_Cas9_Stem1_PreliminaryTests_Ex1_Cas9_ORBIT_100ms_10Hz_1000Frames-1_posXY0_channels_t0_posZ0trdir'
trdir=path+filename
listptr = open(trdir+'/trlist.txt','r')
peaklist = []
for line in listptr:
    peaklist.append(line[0:5])
    n_tr = len(peaklist)

for tr in range(0,n_tr):
        trdict=load_trace(trdir +'/'+peaklist[tr]  + '.tr')
        col=np.array([trdict['xx'],trdict['yy']]).T
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 12:14:30 2021

@author: rfantasia
"""

import numpy as np
from sma_lib.loadtrace import load_trace

def tr_2csv(filename): 
    trdir=filename+'trdir'
    trcsv=filename+'trcsv'
    

    listptr = open(trdir+'/trlist.txt','r')
    peaklist = []
    for line in listptr:
        peaklist.append(line[0:5])
        n_tr = len(peaklist)

    for tr in range(0,n_tr):
        trdict=load_trace(trdir +'/'+peaklist[tr]  + '.tr')
        col=np.array([trdict['xx'],trdict['yy'],trdict['c0int']]).T
        np.savetxt(trcsv +'/'+ peaklist[tr] + '.csv', col, delimiter=',')
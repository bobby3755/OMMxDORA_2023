# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 15:26:29 2021

@author: rfantasia
"""

import numpy as np 
from PIL import Image
from skimage import io
def load_tif(filename,frnum):
    frame = io.imread(filename+'.tif', img_num=frnum)
    #frame=np.array(fileptr)
    return frame
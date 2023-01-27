# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 16:19:51 2021

@author: rfantasia
"""

from ffpdax import ffp_dax
from ffptif import ffp_tif
f='C:/Users/rfantasia/anacondaProjects/ffp/movie_0001'
#f='C:/Users/rfantasia/anacondaProjects/ffp/2021-10-07_ORBIT_Cas9_Stem1_PreliminaryTests_Ex0_Only_ORBIT_10ms_100Hz_5000Frames_posXY0_channels_t0_posZ0_1'

x='C:/Users/rfantasia/anacondaProjects/ffp/ORBIT1024st'
r=ffp_dax(f,x)

#r=ffp_tif(f,x)


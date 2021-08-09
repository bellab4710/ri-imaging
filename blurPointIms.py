from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import ehtim as eh
from   ehtim.calibrating import self_cal as sc
import ehtim.io.load

def blurIm(im):
  eht = eh.array.load_txt('./arrays/EHT2017.txt')

  tint_sec = 30
  tadv_sec = 300
  tstart_hr = 0
  tstop_hr = 24
  bw_hz = 2e9

  obs = im.observe(eht, tint_sec, tadv_sec, tstart_hr, tstop_hr, bw_hz,
  sgrscat=False, ampcal=True, phasecal=True, gainp=0)
  
  obsdat = obs.fit_beam()
  newdat = (obsdat[0]*1/3,obsdat[1]*1/3,obsdat[2]*1/3)
  
  return im.blur_gauss(newdat)

def main():
  for i in range(10):
    im = ehtim.io.load.load_im_fits('../pointImages/scatPoint'+str(i+1)+'.fits',punit="uas")
    im2 = blurIm(im)
    im2.save_txt('blurScat'+str(i+1)+'.txt')
    
if __name__ == '__main__':
    main()

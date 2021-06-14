from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import ehtim as eh
from   ehtim.calibrating import self_cal as sc

im = eh.image.load_txt('./models/jason_mad_eofn.txt')
eht = eh.array.load_txt('./arrays/EHT2017.txt')

tint_sec = 30
tadv_sec = 300
tstart_hr = 0
tstop_hr = 24
bw_hz = 2e9

obs = im.observe(eht, tint_sec, tadv_sec, tstart_hr, tstop_hr, bw_hz,
sgrscat=False, ampcal=True, phasecal=True, gainp=0)

theta = np.radians(180)
c, s = np.cos(theta), np.sin(theta)
R = np.array(((c,-s), (s, c)))

coordsrot = np.array([np.dot(R,[obs.data['u'][i], obs.data['v'][i]]) for i in range(len(obs.data))])
obs.data['u'] = coordsrot[:,0]
obs.data['v'] = coordsrot[:,1]

npix = 128
#fov = 2
fov = 1*im.fovx()
zbl = im.total_flux()  #total flux
#zbl = 2
prior_fwhm = 60
#use these two lines only when making the first image (0% gain error)
emptyprior = eh.image.make_square(obs, npix, fov)
flatprior = emptyprior.add_flat(zbl)
#use this line when making images with >0% gain error. I chose
#to name my files SgrA*_img[num]_correct.txt', and num=1 is the 0% gain error,
#num=2 is the 5% gain error, etc. The prior image for the current image being
#created should be the previous image you made (assuming creation in ascending
#level of gain error)

#prior=eh.image.load_txt(‘SgrA*_img[priorimagenumber]_correct.txt’)
gaussprior = emptyprior.add_gauss(zbl, (prior_fwhm, prior_fwhm, 0, 0, 0))

avg_time=600
obs.add_amp(avg_time=avg_time)
obs.add_cphase(avg_time=avg_time)

flux=zbl
out = eh.imager_func(obs,gaussprior,gaussprior,flux,d1='vis',d2='amp',
alpha_d1=100,alpha_d2= 2,s1='simple',s2='tv2',s3='compact',alpha_s1=1,alpha_s2=1,alpha_s3=100,
alpha_flux=100,maxit=50,stop=10**-10)

outname = 'SgrA*_img1a_final.txt'
out.save_txt(outname)
 #.75*obs.res()
nextim=eh.image.load_txt('./SgrA*_img1a_final.txt')
nextprior = nextim.blur_circ(0.75*obs.res())

out = eh.imager_func(obs,nextprior,nextprior,flux,d1='vis',d2='amp',
alpha_d1=100,alpha_d2 = .75,s1='simple',s2='tv2',s3='compact',alpha_s1=1,alpha_s2=50,
alpha_s3=50,alpha_flux=50,maxit=150,stop=10**-10)
                                                                                        
outname='SgrA*_img1b_final.txt'
out.save_txt(outname)
                                                                                        
nextim=eh.image.load_txt('./SgrA*_img1b_final.txt')
nextprior = nextim.blur_circ(0.5*obs.res())
                                                                                        
out = eh.imager_func(obs,nextprior,nextprior,flux,d1='vis',d2='amp',
alpha_d1=100,alpha_d2 =.5,s1='simple',s2='tv2',s3='compact',alpha_s1=1,alpha_s2=100,
alpha_s3=10,alpha_flux=10,maxit=200,stop=10**-10)
                                                                                        
outname='SgrA*_img1c_final.txt'
out.save_txt(outname)
                                                                                        
nextim=eh.image.load_txt('./SgrA*_img1c_final.txt')
nextprior = nextim.blur_circ(0.33*obs.res())
                                                                                        
out = eh.imager_func(obs,nextprior,nextprior,flux,d1='vis',d2='amp',
alpha_d1=100,alpha_d2 = 1,s1='simple',s2='tv2',s3='compact',alpha_s1=1,alpha_s2=500,
alpha_s3=1,alpha_flux=1,maxit=200,stop=10**-10)
                                                                                        
outname='SgrA*_img1_final.txt'
out.save_txt(outname)

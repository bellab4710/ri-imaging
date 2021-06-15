from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import ehtim as eh
from   ehtim.calibrating import self_cal as sc

im = eh.image.load_txt('./models/jason_mad_eofn.txt')
eht = eh.array.load_txt('./arrays/EHT2017.txt')

im.display()

tint_sec = 30
tadv_sec = 300
tstart_hr = 0
tstop_hr = 24
bw_hz = 2e9
obs = im.observe(eht, tint_sec, tadv_sec, tstart_hr, tstop_hr, bw_hz,
                 sgrscat=False, ampcal=True, phasecal=False,ttype='nfft',gainp=0)

theta = np.radians(180)
c, s = np.cos(theta), np.sin(theta)
R = np.array(((c,-s), (s, c)))

coordsrot = np.array([np.dot(R,[obs.data['u'][i], obs.data['v'][i]]) for i in range(len(obs.data))])
obs.data['u'] = coordsrot[:,0]
obs.data['v'] = coordsrot[:,1]


npix = 128
fov = 1*im.fovx()
zbl = im.total_flux() #total flux
prior_fwhm = 60
#prior will be the previous image if this is not the first one.
emptyprior = eh.image.make_square(obs, npix, fov)
gaussprior = emptyprior.add_gauss(zbl, (prior_fwhm, prior_fwhm, 0, 0, 0))

avg_time = 600
obs.add_amp(avg_time=avg_time)
obs.add_cphase(avg_time=avg_time)

flux=zbl
imgr  = eh.imager.Imager(obs, gaussprior, gaussprior, flux,
                          data_term={'vis':100,'cphase':2}, show_updates=False,
                          reg_term={'simple':1,'flux':100,'tv2':1,'compact':100},
                          maxit=50, ttype='nfft')

imgr.make_image()

out = imgr.out_last()
imgr.init_next = out.blur_circ(.75*res)
imgr.prior_next = imgr.init_next
imgr.dat_term_next = {'vis':100, 'cphase':.75}
imgr.reg_term_next = {'simple':1, 'flux':50,'compact':50,'tv2':50}
imgr.maxi_next=150
imgr.make_image()


out = imgr.out_last()
imgr.init_next = out.blur_circ(0.5*res)

imgr.prior_next = imgr.init_next
imgr.dat_term_next = {'vis':100, 'cphase':0.5}
imgr.reg_term_next = {'simple':1, 'flux':10,'compact':10,'tv2':100}
imgr.maxi_next  = 200
imgr.make_image()


out = imgr.out_last()
imgr.init_next = out.blur_circ(0.33*res)

imgr.prior_next = imgr.init_next
imgr.dat_term_next = {'vis':100, 'cphase':1}
imgr.reg_term_next = {'simple':1, 'flux':1,'compact':1,'tv2':500}
imgr.maxi_next  = 200
imgr.make_image()

out=imgr.out_last()
outname="SgrA*_img1_final"
out.save_txt(outname+".txt")
out.display()

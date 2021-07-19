import numpy as np
from PIL import Image
import astropy.io.fits as fits
rng = np.random.default_rng(12345)
#determines the seeds for the following images so the outputs are reproducible
rints=rng.integers(low=1, high=10000, size=10)
for j in range(10):
    base=np.zeros((128,128,3),dtype=np.uint8)
    mean = [64,64]
    cov=[[64,0],[0,64]]
    #now will generate 5 different points per image but with a seed so that it can be reproduced
    rng2=np.random.default_rng(rints[j])
    x, y = rng2.multivariate_normal(mean, cov, 5).T
    for i in range(5):
        if x[i]<0:
            x[i]=-1*x[i]
        if y[i]<0:
            y[i]=-1*y[i]
        xcord=round(x[i])
        ycord=round(y[i])
        base[xcord][ycord] = [255,255,255]
    hdu=fits.PrimaryHDU(base)
    hdu.writeto('scatPoint'+str(j+1)+'.fits')
    img = Image.fromarray(base)
    img.show()

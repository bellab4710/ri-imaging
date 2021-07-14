import numpy as np
from PIL import Image
#rng = np.random.default_rng()
#xrints = rng.integers(low=10,high=245, size = 15)
#yrints = rng.integers(low=10,high=245, size = 15)
#baseimage = np.zeros((256,256,3),dtype=np.uint8)
#for i in range(15):
    #baseimage[xrints[i]][yrints[i]] = [255,255,255]
#img = Image.fromarray(baseimage)
#img.show()

#different method, works better I think
base2=np.zeros((256,256,3),dtype=np.uint8)
mean = [128,128]
cov=[[128,0],[0,128]]
x, y = np.random.multivariate_normal(mean, cov, 15).T
for i in range(15):
    if x[i]<0:
        x[i]=-1*x[i]
    if y[i]<0:
        y[i]=-1*y[i]
    xcord=round(x[i])
    ycord=round(y[i])
    base2[xcord][ycord] = [255,255,255]
img = Image.fromarray(base2)
img.show()

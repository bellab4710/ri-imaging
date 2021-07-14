import numpy as np
from scipy.misc import imshow
rng = np.random.default_rng()
xrints = rng.integers(low=0,high=127, size = 5)
yrints = rng.integers(low=0,high=127, size = 5)
baseimage = np.zeroes((128,128))
for i in range(5):
    baseimage[x[i]][y[i]] = 1
imshow(baseimage)

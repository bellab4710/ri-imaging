import numpy as np
from PIL import Image

def rmse(observed,expected):
  return np.sqrt(np.sum((observed - expected)**2 / len(observed)))

def main():
  file = open('rmse.txt','w')
  sum=0
  for i in range(10):
    img1 = np.loadtxt('./scat'+str(i+1)+'.txt')
    img2 = np.loadtxt('./blurScat'+str(i+1)+'.txt')
    imvec1 = img1.flatten()
    imvec2 = img2.flatten()
    val = rmse(imvec1, imvec2)
    file.write("RMSE for Image"+str(i+1)+": "+str(val)+"\n")
    sum += val
  file.write("Average RMSE: "+str(sum/10))
  file.close()
 
if __name__ == '__main__':
    main()
    
    
                    

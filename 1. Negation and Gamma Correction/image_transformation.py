import sys
from PIL import Image
import numpy as np

def main():
  # Windows style
  if len(sys.argv) < 2 or sys.argv[1] not in ['negation', 'gamma']:
    print 'Usage: %s %s' % (sys.argv[0], '<action>')
    print 'Available action:\n  %s\n  %s' % ('negation [optional:<image>]', 'gamma <gamma value>, [optional:<image>]')
    print '\n\n\n'
    sys.exit()
  if sys.argv[1] == 'gamma' and len(sys.argv) < 3:
    print 'Usage: %s %s %s %s' % (sys.argv[0], 'gamma', '<gamma value>', '<image target (optional)>')
    sys.exit()

  if sys.argv[1] == 'negation' and len(sys.argv) < 2:
    print 'Usage: %s %s %s' % (sys.argv[0], 'negation', '<image target (optional)>')
    sys.exit()


  if(sys.argv[1] == 'negation'):
    if(len(sys.argv) == 2):
      original_img = tryOpenImage('pic.jpg')
      new_img = negation()
    else:
      original_img = tryOpenImage(sys.argv[2])
      new_img = negation(sys.argv[2])
  else:
    if(len(sys.argv) == 3):
      original_img = tryOpenImage('pic.jpg')
      new_img = gamma(float(sys.argv[2]))
    else:
      original_img = tryOpenImage(sys.argv[3])
      new_img = gamma(float(sys.argv[2]), sys.argv[3])
  
  Image.fromarray(np.hstack((np.array(original_img),np.array(new_img)))).show()


def negation(imgFileName = 'pic.jpg'):
  img = negateImg(imgFileName)
  return img

def gamma(gammaValue = 1, imgFileName = 'pic.jpg'):
  img = gammaCorrection(gammaValue, imgFileName)
  return img

def negateImg(imgFileName):
  img = tryOpenImage(imgFileName)

  img = toGrayScale(img)
  mode = img.mode
  w,h = img.size
  for i in range(w):
    for j in range(h):
      original = img.getpixel((i,j))
      if mode == 'L':
        newPixels = 255 - original
      else:
        r = 255 - original[0]
        g = 255 - original[1]
        b = 255 - original[2]
        newPixels = (r,g,b)
      img.putpixel((i,j), newPixels)
  return img

def toGrayScale(img):
  w,h = img.size
  
  # test if rgb
  try:
    len(img.getpixel((0,0)))>1

    # Create new Image with mode L : gray scale
    grayScaleImage = Image.new('L', (w, h))
    for i in range(w):
      for j in range(h):
        pixelValue = int(sum(img.getpixel((i,j)))/3)
        grayScaleImage.putpixel((i, j), (pixelValue))
    return grayScaleImage
  except:
    return img

def gammaCorrection(gammaValue, imgFileName):
  img = tryOpenImage(imgFileName)
  img = toGrayScale(img)
  w,h = img.size
  mode = img.mode
  for i in range(w):
    for j in range(h):
      if mode == 'L':
        newPixel = int(((img.getpixel((i, j))/255.0) ** gammaValue) * 255) 
        img.putpixel((i,j), (newPixel))
      else:
        r = int(((img.getpixel((i, j))[0]/255.0) ** gammaValue) * 255) 
        g = int(((img.getpixel((i, j))[1]/255.0) ** gammaValue) * 255) 
        b = int(((img.getpixel((i, j))[2]/255.0) ** gammaValue) * 255) 
        newPixel = (r, g, b)
        img.putpixel((i,j), newPixel)
  return img

def tryOpenImage(imgFileName = 'pic.jpg'):
  try:
    return toGrayScale(Image.open(imgFileName))
  except:
    print "Unable to open image"
    sys.exit()

if __name__ == '__main__':
  main()

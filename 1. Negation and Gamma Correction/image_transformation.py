import sys
from PIL import Image

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
      negation()
    else:
      negation(sys.argv[1])
  else:
    if(len(sys.argv) == 3):
      gamma(float(sys.argv[2]))
    else:
      gamma(float(sys.argv[2]), sys.argv[3])


def negation(imgFileName = 'pic.jpg'):
  img = negateImg(imgFileName)
  img.show()

def gamma(gammaValue = 1, imgFileName = 'pic.jpg'):
  img = gammaCorrection(gammaValue, imgFileName)
  img.show()

def negateImg(imgFileName):
  try:
    img = Image.open(imgFileName)
  except:
    print "Error occured, unable to open file"
    sys.exit()

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
  # Create new Image with mode L : gray scale
  grayScaleImage = Image.new('L', (w, h))
  for i in range(w):
    for j in range(h):
      pixelValue = int(sum(img.getpixel((i,j)))/3)
      grayScaleImage.putpixel((i, j), (pixelValue))
  
  return grayScaleImage

def gammaCorrection(gammaValue, imgFileName):
  try:
    img = Image.open(imgFileName)
  except:
    print "Error occured, unable to open file"
    sys.exit()
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

if __name__ == '__main__':
  main()
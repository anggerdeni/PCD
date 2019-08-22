from PIL import Image

def toGrayScale(img):
  w,h = img.size
  # Create new Image with mode L : gray scale
  grayScaleImage = Image.new('L', (w, h))
  for i in range(w):
    for j in range(h):
      pixelValue = int(sum(img.getpixel((i,j)))/3)
      grayScaleImage.putpixel((i, j), (pixelValue))
  
  return grayScaleImage

def negateImg(img):
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


def gammaCorrection(img, gamma = 1):
  w,h = img.size
  mode = img.mode
  for i in range(w):
    for j in range(h):
      if mode == 'L':
        newPixel = int(((img.getpixel((i, j))/255.0) ** gamma) * 255) 
        img.putpixel((i,j), (newPixel))
      else:
        r = int(((img.getpixel((i, j))[0]/255.0) ** gamma) * 255) 
        g = int(((img.getpixel((i, j))[1]/255.0) ** gamma) * 255) 
        b = int(((img.getpixel((i, j))[2]/255.0) ** gamma) * 255) 
        newPixel = (r, g, b)
        img.putpixel((i,j), newPixel)


def main():
  # negate RGB image: save to negated.jpg
  img = Image.open('pic.jpg')
  negateImg(img)
  img.save('negated.jpg')

  # turn into grayscale then negate it: save to negated_grayscale.jpg
  grayScaleImage = toGrayScale(img)
  negateImg(grayScaleImage)
  grayScaleImage.save('negated_grayscale.jpg')

  # gamma correction
  gamma = float(input('Masukkan nilai gamma: '))

  img = Image.open('pic.jpg')
  grayScaleImage = toGrayScale(img)
  gammaCorrection(grayScaleImage, gamma)
  grayScaleImage.save('gammaed.jpg')

if __name__ == '__main__':
  main()
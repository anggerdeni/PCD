from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def open_image(num):
    img = Image.open('pic' + str(i+1) + '.jpg')
    if img.mode != 'L' : img = img.convert('L')
    return img

def generate_histogram(img):
    hist = [0]*256
    width, height = img.size
    for i in range(width):
        for j in range(height):
            pixel = img.getpixel((i,j))
            hist[pixel] += 1
    return hist

def generate_CDF(img):
    cdf = []
    hist = generate_histogram(img)
    width, height = img.size
    img_size = width * height
    current_sum = 0.0
    for i in range(256):
        current_sum += hist[i]
        cdf.append(current_sum / img_size)
    return cdf

def match(img1, img2):
    cdf = {
            'current_image': generate_CDF(img1),
            'reference_image': generate_CDF(img2)
          }
    hist_map = []
    
    for i in range(256):
        val = cdf['current_image'][i]
        index = -1
        minDist = 1e9
        for j in range(256):
            dist = abs(val - cdf['reference_image'][j])
            if dist < minDist:
                index = j
                minDist = dist
        hist_map.append(index)
    return hist_map

def histogram_matching(num, img):
    for current in range(num):
        for reference in range(num):
            if current == reference : continue
            map = match(img[current], img[reference])
            width, height = img[current].size
            newImage = Image.new('L', (width, height))
            for w in range(width):
                for h in range(height):
                    pixel = img[current].getpixel((w, h))
                    newImage.putpixel((w, h), map[pixel])
            newImage.save('image_' + str(current+1) + '_to_' + str(reference+1) + '.jpg')
"""
if __name__ == "__main__":
    imgs = []
    num_images = 3
    for i in range(num_images):
        imgs.append(open_image(num_images))
    histogram_matching(num_images, imgs)

imgs = []
hists = []
for i in range(7):
    imgs.append(open_image(i))
    hists.append(generate_histogram(imgs[i]))

for i in range(len(hists)):
    plt.plot(range(256), hists[i])
    plt.ylabel('Frequency')
    plt.xlabel('Pixel value')
    plt.savefig('pic{}_plot.jpg'.format(i+1))
    plt.clf()
"""

for current in range(3):
    for reference in range(3):
        if current == reference : continue
        name = 'image_' + str(current+1) + '_to_' + str(reference+1) + '.jpg'
        hist_name = 'hist_image_' + str(current+1) + '_to_' + str(reference+1) + '.jpg'
        im = Image.open(name)
        hist = generate_histogram(im)
        plt.plot(range(256), hist)
        plt.ylabel('Frequency')
        plt.xlabel('Pixel value')
        plt.savefig(hist_name)
        plt.clf()

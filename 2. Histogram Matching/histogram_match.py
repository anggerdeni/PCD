from PIL import Image
import matplotlib.pyplot as plt

def open_image(num):
    img = []
    for i in range(num):
        tmp = Image.open('image' + str(i+1) + '.jpg')
        if tmp.mode != 'L' : tmp = tmp.convert('L')
        img.append(tmp)
    return img

def generate_histogram(img):
    hist = [0 for i in range(256)]
    width, height = img.size
    for i in range(width):
        for j in range(height):
            pixel = img.getpixel((i, j))
            hist[pixel] += 1
    return hist

def generate_CDF(img):
    cdf = []
    hist = generate_histogram(img)
    width, height = img.size
    img_size = width * height
    sum = 0
    for i in range(256):
        sum += hist[i]
        cdf.append(sum / img_size)
    return cdf

def match(img1, img2):
    cdf = []
    map = []
    cdf.append(generate_CDF(img1))
    cdf.append(generate_CDF(img2))
    
    for reference in range(256):
        val = cdf[0][reference]
        index = -1
        minDist = 1e9
        for target in range(256):
            dist = abs(val - cdf[1][target])
            if dist < minDist:
                index = target
                minDist = dist
        map.append(index)
    return map

def histogram_matching(num, img):
    for reference in range(num):
        for target in range(num):
            if reference == target : continue
            map = match(img[reference], img[target])
            width, height = img[reference].size
            newImage = Image.new('L', (width, height))
            for w in range(width):
                for h in range(height):
                    pixel = img[reference].getpixel((w, h))
                    newImage.putpixel((w, h), map[pixel])
            newImage.save('image_' + str(reference+1) + '_to_' + str(target+1) + '.jpg')

if __name__ == "__main__":
    img = []
    number_of_input = 3
    img = open_image(number_of_input)
    histogram_matching(number_of_input, img)

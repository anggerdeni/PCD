from PIL import Image, ImageFilter
import numpy as np
import sys
import math
import operator

# Gaussian Filter
def gaussian_blur(img, radius = 2):
	return img.filter(ImageFilter.GaussianBlur(radius))


# Edge Detection
def edge_detection(img):
	return img.filter(ImageFilter.FIND_EDGES)

def calculate_r(i,j,theta):
	return i * math.cos(math.radians(theta)) + j * math.sin(math.radians(theta))

# Hough Transform
def preprocess(img):
	# img = gaussian_blur(img, 1)
	img = edge_detection(img)
	img = sharpen(img)
	# img.show()
	return img


def hough_transform(img):
	img = preprocess(img).crop((1,1, img.size[0]-1, img.size[1]-1))
	w,h = img.size
	freq = {}
	data = img.load()

	for i in range(w):
		for j in range(h):
			if data[i,j] == 255:
				for theta in range(-90, 91):
					r = int(calculate_r(i,j,theta))
					try:
						freq[(r, theta)] += 1
					except:
						freq[(r, theta)] = 1


	sorted_freq = sorted(freq.items(), key=operator.itemgetter(1))[::-1]

	return sorted_freq[:3]


# sharpen

def sharpen(img):
	count = 0
	data = img.load()
	threshold = list(set(img.getdata()))
	threshold = threshold[len(threshold)/15]

	for i in range(img.size[0]):
		for j in range(img.size[1]):
			if(data[i,j] > threshold):
				data[i,j] = 255
				count += 1
			else:
				data[i,j] = 0

	return img

# Helper functions 

def openImage(img):
	return Image.open(img), Image.open(img).convert('L')

def usage(program):
	return """[*] Usage: python {} <image_file> <image_file> ...""".format(program)

def main():
	if(len(sys.argv) < 2):
		print usage(sys.argv[0])
		sys.exit(0)

	images = sys.argv[1:]
	for i in images:
		text = 'Working on image {}'.format(i)
		print '--- {} {}'.format(text,'-'.rjust(100-5-len(text),'-'))
		try:
			img_asli,img = openImage(i)
			img_asli = img_asli.crop((1,1, img_asli.size[0]-1, img_asli.size[1]-1))
			data = img_asli.load()
			lines = hough_transform(img)
			width,height = img_asli.size
			for line in lines:
				count = 0
				for w in range(width):
					count +=1
					for h in range(height):
						theta = line[0][1]
						r = calculate_r(w,h,theta)
						if int(r) == int(line[0][0]):
							data[w,h] = (255,0,0)
					sys.stdout.write("\rWorking on line {}\t|{}".format(str(line).rjust(30,' '),str(count).rjust(8,' ')))
					sys.stdout.flush()
				print
			img_asli.show()	
		except Exception, e:
			print e
		print
	return


if __name__ == '__main__':
	main()
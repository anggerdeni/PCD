from PIL import Image

img = Image.open('pic.jpg')
w,h = img.size

for i in range(w):
    for j in range(h):
        original = img.getpixel((i,j))
        r = 255 - original[0]
        g = 255 - original[1]
        b = 255 - original[2]
        img.putpixel((i,j), (r,g,b))

img.save('negated.jpg')
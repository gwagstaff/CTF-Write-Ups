from PIL import Image

pixels = []
w = 100
h = 1000
filename = "stripped.txt"

file = open(filename,"r")

for lines in file:
	color = lines.strip().split('.')
	r = int(color[0])
	g = int(color[1])
	b = int(color[2])
	pixels.append([r,g,b])

size = w+1,h+1
img = Image.new("RGB",size)
data = img.load()
counter = 0
for y in range(0,h):
	for x in range(0,w):
		r,g,b = pixels[counter]
		data[x,y] = (r,g,b)
		counter += 1
		#print (x,y,":",counter)
			
img.save("flag.png")

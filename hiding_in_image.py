from PIL import Image

imgage_for_hiding = Image.open('image.png')
pixelmap = imgage_for_hiding.load()
file_to_hide = open("test.txt",'r')
print((pixelmap[1])



imgage_for_hiding.save('test.png')

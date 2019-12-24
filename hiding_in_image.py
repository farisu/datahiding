from PIL import Image
import binascii

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'



image_for_hiding = Image.open('image.png')
pixelmap = image_for_hiding.load()
width = (image_for_hiding.size[0])
hight = (image_for_hiding.size[1])
print("width: " + str(width),"hight: " + str(hight))
MAX_BITS = hight*width
print(MAX_BITS)

file_to_hide = open("test.txt",'r')
stringbinary = text_to_bits(file_to_hide.read())
print(len(stringbinary))

for i in range(len(stringbinary)):
    r,g,b = pixelmap[i%(width*3),i/(width*3)]
    #TODO: Finish Decoding here




file_to_hide.close()
image_for_hiding.save('test.png')

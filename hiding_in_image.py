from PIL import Image
import binascii

#TODO Praser

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def hide_data(data_to_hide, picture_as_stash):
    #TODO 1.Hide filename in the picture
    #TODO 3. Write filelenght after
    image_for_hiding = Image.open(picture_as_stash)
    original_pixelmap = image_for_hiding.load()
    width = (image_for_hiding.size[0])
    hight = (image_for_hiding.size[1])
    print("width: " + str(width),"hight: " + str(hight))
    MAX_BITS = hight*width*3
    print("Maximum Bits:  " + str(MAX_BITS))

    file_to_hide = open(data_to_hide,'r')
    stringbinary = text_to_bits(file_to_hide.read())
    print("Bits of input: " + str(len(stringbinary)))

    result_image = Image.new('RGB',(width,hight),color='white')
    pixelmap = result_image.load()
    for i in range(width*hight):
        pixelmap[int((i)%(width)),int(i/(width))] = original_pixelmap[int((i)%(width)),int(i/(width))]
    for i in range(len(stringbinary)):
        r,g,b = original_pixelmap[int((i/3)%(width)),int(i/(width*3))]
        if(i%3==0):
            if(r%2 != int(stringbinary[i])):
                if(r%2 == 0):
                    r+=1
                else:
                    r-=1
        if(i%3==0):
            if(g%2 != int(stringbinary[i])):
                if(g%2 == 0):
                    g+=1
                else:
                    g-=1
        if(i%3==0):
            if(b%2 != int(stringbinary[i])):
                if(b%2 == 0):
                    b+=1
                else:
                    b-=1
        pixelmap[int((i/3)%(width)),int(i/(width*3))] = r,g,b

    file_to_hide.close()
    result_image.save("result.png")

def seek_data(file_to_store,picture_to_seek):
    #TODO 2. If 1. is finished, remove the file_to_store parameter
    image_to_seek_opened = Image.open(picture_to_seek)
    width = image_to_seek_opened.size[0]
    hight = image_to_seek_opened.size[1]
    pixelmap = image_to_seek_opened.load()
    bitstring = ""
    for i in range(width*hight):
        bitstring += str(pixelmap[int((i/3)%(width)),int(i/(width*3))][i%3]%2)
    resultstring = print(bits_to_text(bitstring))     #TODO Fix UnicodeDecodeError
    resultfile = open(file_to_store,'w')
    resultfile.write(resultstring)
    resultfile.close()

print(bits_to_text("11111111"))
#hide_data("test.txt","image.png")
seek_data("result.txt","result.png")
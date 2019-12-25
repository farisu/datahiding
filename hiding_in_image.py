from PIL import Image
import binascii

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def hide_data(data_to_hide, picture_as_stash):
    image_for_hiding = Image.open(picture_as_stash)
    pixelmap = image_for_hiding.load()
    width = (image_for_hiding.size[0])
    hight = (image_for_hiding.size[1])
    print("width: " + str(width),"hight: " + str(hight))
    MAX_BITS = hight*width
    print(MAX_BITS)

    file_to_hide = open(data_to_hide,'r')
    stringbinary = text_to_bits(file_to_hide.read())
    print(len(stringbinary))

    for i in range(len(stringbinary)):
        r,g,b = pixelmap[int((i/3)%(width)),int(i/(width*3))]
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
    image_for_hiding.save(picture_as_stash)

def seek_data(file_to_store,picture_to_seek):
    #TODO
    pass

hide_data("test.txt","test.png")
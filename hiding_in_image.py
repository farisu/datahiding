from PIL import Image
import binascii

#TODO Praser

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def hide_data(data_to_hide: str, picture_as_stash: str) -> None:
    with Image.open(picture_as_stash) as image:
        width = image.size[0]
        height = image.size[1]
        pixelmap = image.getdata()

    print("width: " + str(width), "height: " + str(height))
    MAX_BITS = height*width*3
    MAX_BYTES = MAX_BITS / 8
    print("Maximum Bits:  " + str(MAX_BITS))
    print("Maximum Bytes:  " + str(MAX_BYTES))

    with open(data_to_hide, 'r') as message:
        stringbinary = text_to_bits(message.read()) + '0'
    
    print("Bits of input: " + str(len(stringbinary)))

    result_image = Image.new('RGB', (width, height), color='white')
    newpixelmap = []

    for pixel in pixelmap:
        newpixel = []
        for color in pixel:
            newcolor = color & 0xfe
            newcolor += 1 if stringbinary[0] == '1' else 0 
            newpixel.append(newcolor)
            if len(stringbinary) > 1:
                stringbinary = stringbinary[1:]
        newpixelmap.append(tuple(newpixel))
        newpixel = []
    
    result_image.putdata(newpixelmap)
    result_image.save("result.png")
    result_image.close()

def seek_data(file_to_store: str, picture_to_seek: str) -> None:
    with Image.open(picture_to_seek) as image: 
        width = image.size[0]
        height = image.size[1]
        pixelmap = image.getdata()

    bitstring = ""
    for pixel in pixelmap:
        for color in pixel:
            bitstring += str(color % 2)
        
    resultstring = bits_to_text(bitstring)     #TODO Fix UnicodeDecodeError

    with open(file_to_store,'w') as result:
        result.write(resultstring)

hide_data("test.txt","image.png")
seek_data("result.txt","result.png")
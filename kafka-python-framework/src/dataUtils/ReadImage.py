import base64


import PIL




def writeImageToDisk(base64Img,name):
    basemod = base64Img.replace("b'","'")
    img = bytes(basemod , encoding="UTF-8")
    filename = name+".jpg"
    print(img)
    with open(filename, "wb") as fh:
        fh.write(base64.decodebytes(img))

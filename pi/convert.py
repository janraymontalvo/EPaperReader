from PIL import Image
from array import *
import numpy as np


def downsampleTo8bitGrayScale(img):
    grayImage = img.convert('LA')
    grayImage.save('gray.png')
    return grayImage;


def toIntArray(img):
    width, height = img.size
    data = np.zeros(height * width)
    data = data.astype(dtype='int32')
    i = 0
    for y in range(0, height):
        for x in range(0, width):
            rgb,alpha = img.getpixel((x, y))
            data[i] = rgb
            i += 1
    return data


def downsampleTo1bitGrayScale(imgIntArray):
    for i in range(0, len(imgIntArray)):
        if imgIntArray[i] <= 127:
            imgIntArray[i] = 255
        else:
            imgIntArray[i] = 0
    return imgIntArray


def toByteArray(intArray):
    bytedata = np.zeros(len(intArray))
    bytedata = bytedata.astype(dtype='int8')
    for i in range(0, len(intArray)):
        bytedata[i] = bytes(intArray[i])
    return bytedata
	

def convertTo1bit_PixelFormatType4(picdata):
    newPicData = np.zeros(len(picdata))
    newPicData = newPicData.astype(dtype='int8')
    row = 30
    s = 1
    for i in range(0, (len(picdata))/8, 16):
        newPicData[row - s] = (
            ((picdata[i + 6] << 7) & 0x80) | ((picdata[i + 14] << 6) & 0x40) | ((picdata[i + 4] << 5) & 0x20) | (
                (picdata[i + 12] << 4) & 0x10) | ((picdata[i + 2] << 3) & 0x08) | ((picdata[i + 10] << 2) & 0x04) | (
                (picdata[i + 0] << 1) & 0x02) | ((picdata[i + 8] << 0) & 0x01))

        newPicData[row + 30 - s] = (
            ((picdata[i + 1] << 7) & 0x80) | ((picdata[i + 9] << 6) & 0x40) | ((picdata[i + 3] << 5) & 0x20) | (
                (picdata[i + 11] << 4) & 0x10) | ((picdata[i + 5] << 3) & 0x08) | ((picdata[i + 13] << 2) & 0x04) | (
                (picdata[i + 7] << 1) & 0x02) | ((picdata[i + 15] << 0) & 0x01))

        s = s + 1
        if s == 31:
            s = 1
            row = row + 60
    return newPicData


img = Image.open('test.png')
img = img.convert('RGB')
img = downsampleTo8bitGrayScale(img) #good
rawIntPixelData = toIntArray(img) #good
rawIntPixelData = downsampleTo1bitGrayScale(rawIntPixelData) #good
rawBytePixelData = toByteArray(rawIntPixelData)
rawBytePixelData = convertTo1bit_PixelFormatType4(rawBytePixelData)

#To iterate numpy array do, 
#for x in np.nditer(rawIntPixelData):
#    print x


import cv2 as cv
from numpy import base_repr, sqrt
from scipy import fft

from Settings import RESCALE_SIZE, HASH_BASE

BIT_LEN = int(sqrt(HASH_BASE)) - 1

sizePow = RESCALE_SIZE ** 2
sizeRange = range(RESCALE_SIZE)

def GetImageHash(path: str) -> str:
    img = cv.imread(path) #讀取圖片
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #將圖片轉成灰階
    imgMin = cv.resize(img, (RESCALE_SIZE, RESCALE_SIZE), cv.INTER_AREA) #將圖片縮小
    imgDct = fft.dct(fft.dct(imgMin, axis=0), axis=1) #計算DCT並將二維陣列轉成一維

    grayAvg = 0
    for i in sizeRange:
        for j in sizeRange:
            grayAvg += imgDct[i, j] #計算dct平均值
    grayAvg /= sizePow

    res = ""
    s = ""
    for i in sizeRange:
        for j in sizeRange:
            s += "0" if imgDct[i, j] < grayAvg else "1"
            if len(s) == BIT_LEN:
                res += base_repr(int(s, 2), HASH_BASE)
                s = ""

    if len(s) > 0:
        res += base_repr(int(s, 2), HASH_BASE)

    return res
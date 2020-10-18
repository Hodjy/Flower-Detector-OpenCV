import glob
import cv2
import numpy as np

# Declare variables.

# 1 for color, 0 for greyscale.
isColorImage = 1
pictureNewSize = (600, 400)
templatesNewSize = (200, 200)
negativeTemplateNewSize = (200,200)
images = glob.glob("ReferenceImages/ImagesToDetect/*.jpg")
PositiveTemplateNames = glob.glob("ReferenceImages/P/*.png")
NegativeTemplateNames = glob.glob("ReferenceImages/N/*.png")
imagesList = [cv2.imread(img, isColorImage) for img in images]
PTemplateList = [cv2.imread(img, isColorImage) for img in PositiveTemplateNames]
NTemplateList = [cv2.imread(img, isColorImage) for img in NegativeTemplateNames]
FilePathForProcessedImages = "ReferenceImages/ImagesToDetect/NewSize/{0}.png"
FilePathForProcessedPTemplates = "ReferenceImages/P/"
FilePathForProcessedNTemplates = "ReferenceImages/N/"
bigPath = "Big/{0}.png"
mediumPath = "Medium/{0}.png"
smallPath = "Small/{0}.png"
laplasian = np.array([[-1, -1, -1],
                      [-1, 9, -1],
                      [-1, -1, -1]], dtype=np.float32)


def __preprocessImage(img, newSize):
    # Take image, resize it, then apply filters. (not using padding on purpose, it may leave a
    # border even after unpadding).

    img = cv2.GaussianBlur(img, (3, 3), 0, img)
    #img = cv2.filter2D(img, 0, laplasian)
    img = cv2.resize(img, newSize)

    return img

def __preprocessImages(images, filePath, newSize):
    # loop over all given images, filter resize and save them.
    i = 1

    for img in images:
        img = __preprocessImage(img, newSize)
        cv2.imwrite(filePath.format(i), img)
        i += 1


def Preprocess():
    # Preprocess all images, for size, take the corresponding var and reduce its value by percent, and cast as int.
    __preprocessImages(imagesList, FilePathForProcessedImages, pictureNewSize)
    __preprocessImages(PTemplateList, FilePathForProcessedPTemplates + bigPath, templatesNewSize)
    __preprocessImages(PTemplateList, FilePathForProcessedPTemplates + mediumPath, (int(templatesNewSize[0] * 0.75), int(templatesNewSize[1] * 0.75)))
    __preprocessImages(PTemplateList, FilePathForProcessedPTemplates + smallPath, (int(templatesNewSize[0] * 0.50), int(templatesNewSize[1] * 0.50)))
    __preprocessImages(NTemplateList, FilePathForProcessedNTemplates + bigPath, negativeTemplateNewSize)
    __preprocessImages(NTemplateList, FilePathForProcessedNTemplates + mediumPath, (int(negativeTemplateNewSize[0] * 0.75), int(negativeTemplateNewSize[1] * 0.75)))
    __preprocessImages(NTemplateList, FilePathForProcessedNTemplates + smallPath, (int(negativeTemplateNewSize[0] * 0.50), int(negativeTemplateNewSize[1] * 0.50)))



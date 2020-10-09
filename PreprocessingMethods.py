import glob
import cv2

isColorImage = 1  # 1 for color, 0 for greyscale
pictureNewSize = (600, 400)
templatesNewSize = (200, 200)
images = glob.glob("ReferenceImages/ImagesToDetect/*.jpg")
PositiveTemplateNames = glob.glob("ReferenceImages/P/*.png")
NegetiveTemplateNames = glob.glob("ReferenceImages/N/*.png")
imagesList = [cv2.imread(img, isColorImage) for img in images]
PTemplateList = [cv2.imread(img, isColorImage) for img in PositiveTemplateNames]
NTemplateList = [cv2.imread(img, isColorImage) for img in NegetiveTemplateNames]
FilePathForProcessedImages = "ReferenceImages/ImagesToDetect/NewSize/{0}.png"
FilePathForProcessedPTemplates = "ReferenceImages/P/"
FilePathForProcessedNTemplates = "ReferenceImages/N/"
bigPath = "Big/{0}.png"
mediumPath = "Medium/{0}.png"
smallPath = "Small/{0}.png"


def __preprocessImage(img, newSize):
    img = cv2.resize(img, newSize)
    #cv2.Laplacian(img, cv2.CV_16U, img, 3)
    #cv2.GaussianBlur(img, (3, 3), 3, img)

    return img

def __preprocessImages(images, filePath, newSize):
    i = 1

    for img in images:
        img = __preprocessImage(img, newSize)
        cv2.imwrite(filePath.format(i), img)
        i += 1


def Preprocess():
    __preprocessImages(imagesList, FilePathForProcessedImages, pictureNewSize)
    __preprocessImages(PTemplateList, FilePathForProcessedPTemplates + bigPath, templatesNewSize)
    __preprocessImages(PTemplateList, FilePathForProcessedPTemplates + mediumPath, (templatesNewSize[0] // 2, templatesNewSize[1] // 2))
    __preprocessImages(PTemplateList, FilePathForProcessedPTemplates + smallPath, (templatesNewSize[0] // 4, templatesNewSize[1] // 4))
    __preprocessImages(NTemplateList, FilePathForProcessedNTemplates + bigPath, templatesNewSize)
    __preprocessImages(NTemplateList, FilePathForProcessedNTemplates + mediumPath, (templatesNewSize[0] // 2, templatesNewSize[1] // 2))
    __preprocessImages(NTemplateList, FilePathForProcessedNTemplates + smallPath, (templatesNewSize[0] // 4, templatesNewSize[1] // 4))

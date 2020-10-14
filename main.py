import glob
import cv2
import time
import ObjectDetectionMethods as ODM
import PreprocessingMethods as PM

isColorImage = 1 # 1 for color, 0 for greyscale
PositiveTemplateNames = glob.glob("ReferenceImages/P/*/*.png")
NegativeTemplateNames = glob.glob("ReferenceImages/N/*/*.png")
PTemplateList = [cv2.imread(img, isColorImage) for img in PositiveTemplateNames]
NTemplateList = [cv2.imread(img, isColorImage) for img in NegativeTemplateNames]
imgToDetect = cv2.imread("ReferenceImages/ImagesToDetect/NewSize/13.png", isColorImage)
rectangles = []
rectanglesEps = 0.3
positiveThreshold = 0.5
negativeThreshold = positiveThreshold

#PM.Preprocess() # Remove comment in order to preprocess all images.
startTime = time.time()
rectangles = ODM.DetectPositive(imgToDetect, PTemplateList, positiveThreshold, rectanglesEps)
if positiveThreshold < 0.2:
    negativeThreshold = 0.15

rectangles = ODM.DetectNegative(imgToDetect, NTemplateList, rectangles, negativeThreshold)
if len(rectangles):  # If matches still exists
    ODM.DrawRectanglesOnImage(rectangles, imgToDetect)

timeElapsed = time.time() - startTime
print("Time passed:", timeElapsed)
cv2.imshow("Final", imgToDetect)
cv2.waitKey()

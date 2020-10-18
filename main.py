import glob
import cv2
import time
import ObjectDetectionMethods as ODM
import PreprocessingMethods as PM

# Declare Variable

# 1 for color, 0 for greyscale
isColorImage = 1
PositiveTemplateNames = glob.glob("ReferenceImages/P/*/*.png")
NegativeTemplateNames = glob.glob("ReferenceImages/N/*/*.png")
PTemplateList = [cv2.imread(img, isColorImage) for img in PositiveTemplateNames]
NTemplateList = [cv2.imread(img, isColorImage) for img in NegativeTemplateNames]
imgToDetect = cv2.imread("ReferenceImages/ImagesToDetect/NewSize/1.png", isColorImage)
rectangles = []
rectanglesEps = 0.3
positiveThreshold = 0.3
negativeThreshold = positiveThreshold

# Will initiate preprocessing of all the images.
PM.Preprocess()
startTime = time.time()
# Detect positive and return rectangles.
rectangles = ODM.DetectPositive(imgToDetect, PTemplateList, positiveThreshold, rectanglesEps)
if positiveThreshold < 0.2:
    negativeThreshold = 0.15

# Detect false positive and return the rectangles.
rectangles = ODM.DetectNegative(imgToDetect, NTemplateList, rectangles, negativeThreshold)
if len(rectangles):  # If matches still exists.
    ODM.DrawRectanglesOnImage(rectangles, imgToDetect)

timeElapsed = time.time() - startTime
print("Time passed:", timeElapsed) # Print time elapsed.
cv2.imshow("Final", imgToDetect)
cv2.waitKey()

import glob
import cv2
import ObjectDetectionMethods as ODM
import PreprocessingMethods as PM

isColorImage = 1 # 1 for color, 0 for greyscale
PositiveTemplateNames = glob.glob("ReferenceImages/P/Medium/31.png")
NegetiveTemplateNames = glob.glob("ReferenceImages/N/Big/*.png")
PTemplateList = [cv2.imread(img, isColorImage) for img in PositiveTemplateNames]
NTemplateList = [cv2.imread(img, isColorImage) for img in NegetiveTemplateNames]
imgToDetect = cv2.imread("ReferenceImages/ImagesToDetect/NewSize/3.png", isColorImage)
rectangles = []
rectanglesEps = 0.4
positiveThreshold = 0.68
negetiveThreshold = 0.9


#PM.Preprocess() # Remove comment in order to preprocess all images.
ODM.DetectPositive(imgToDetect, PTemplateList, positiveThreshold, rectangles)
if len(rectangles):  # If found matches
    rectangles, weightsNotUsed = cv2.groupRectangles(rectangles, 1, rectanglesEps)

ODM.DetectNegative(imgToDetect, NTemplateList, rectangles, negetiveThreshold)
if len(rectangles):  # If matches still exists
    ODM.DrawRectanglesOnImage(rectangles, imgToDetect)

cv2.imshow("Final", imgToDetect)
cv2.waitKey()

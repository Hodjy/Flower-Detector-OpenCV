import glob
import cv2
import ObjectDetectionMethods as ODM
import PreprocessingMethods as PM

isColorImage = 1 # 1 for color, 0 for greyscale
PositiveTemplateNames = glob.glob("ReferenceImages/P/*/*.png")
NegetiveTemplateNames = glob.glob("ReferenceImages/N/*/*.png")
PTemplateList = [cv2.imread(img, isColorImage) for img in PositiveTemplateNames]
NTemplateList = [cv2.imread(img, isColorImage) for img in NegetiveTemplateNames]
imgToDetect = cv2.imread("ReferenceImages/ImagesToDetect/NewSize/4.png", isColorImage)
rectangles = []
rectanglesEps = 0.01
positiveThreshold = 0.3
negativeThreshold = 1


#PM.Preprocess() # Remove comment in order to preprocess all images.
rectangles = ODM.DetectPositive(imgToDetect, PTemplateList, positiveThreshold, rectanglesEps)

print("DoneGrouping")
rectangles = ODM.DetectNegative(imgToDetect, NTemplateList, rectangles, negativeThreshold)
if len(rectangles):  # If matches still exists
    ODM.DrawRectanglesOnImage(rectangles, imgToDetect)

cv2.imshow("Final", imgToDetect)
cv2.waitKey()

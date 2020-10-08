import glob
import cv2
import ObjectDetectionMethods as ODM


PositiveTemplateNames = glob.glob("ReferenceImages/P/4.png")
NegetiveTemplateNames = glob.glob("ReferenceImages/N/*.png")
PTemplateList = [cv2.imread(img, 0) for img in PositiveTemplateNames]
NTemplateList = [cv2.imread(img, 0) for img in NegetiveTemplateNames]
imgToDetect = cv2.imread("ReferenceImages/ImagesToDetect/4.jpg", 0)
rectangles = []
rectanglesEps = 0.4
positiveThreshold = 0.5
negetiveThreshold = 0.9


#cv2.Laplacian(imgToDetect, cv2.CV_16U, imgToDetect, 3)
ODM.DetectPositive(imgToDetect, PTemplateList, positiveThreshold, rectangles)
if len(rectangles):  # if found matches
    print(len(rectangles))
    rectangles, weightsNotUsed = cv2.groupRectangles(rectangles, 1, rectanglesEps)

ODM.DetectNegative(imgToDetect, NTemplateList, rectangles, negetiveThreshold)
if len(rectangles):  # if matches still exists
    ODM.DrawRectanglesOnImage(rectangles, imgToDetect)

cv2.imshow("Final", imgToDetect)
cv2.waitKey()

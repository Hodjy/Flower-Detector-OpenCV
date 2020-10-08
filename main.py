import glob
import cv2
import numpy as np


def CreateRectanglesFromLocations(rectangles, locations, w, h):
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), w, h]
        rectangles.append(rect)  # append two times in cause there is only one rectangle around an area so
        rectangles.append(rect)  # groupRectangles wont remove it.


def DrawRectanglesOnImage(rectangles, imgToDrawOn):
    lineColor = (255, 0, 0)
    lineType = cv2.LINE_4

    for (x, y, w, h) in rectangles:
        topLeft = (x, y)
        bottomRight = (x + w, y + h)
        cv2.rectangle(imgToDrawOn, topLeft, bottomRight, lineColor, lineType)


def DetectFalsePositiveByNegetiveTemplate(imgToDetect, rec, template, threshold):
    x = rec[0]
    y = rec[1]
    w = rec[2]
    h = rec[3]
    roi = imgToDetect[y:y + h, x:x + w]
    isFalsePositive = False
    isTemplateSmaller = roi.shape[0] > template.shape[0] and roi.shape[1] > template.shape[1]

    if isTemplateSmaller:  # check for false positive.
        matchResult = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)

        locations = np.where(matchResult >= threshold)  # get all the suspect points from the result by the threshold.
        locations = list(zip(*locations[::-1]))

        if len(locations):
            print("Locations:", len(locations))
            isFalsePositive = True

    return isFalsePositive


def DetectObjectByTemplate(imgToDetect, template, threshold, rectangles):  # inserts result values into rectangles.
    templateWidth = template.shape[1]
    templateHeight = template.shape[0]
    # template = cv2.resize(template, None, None, 0.9, 0.9, cv2.INTER_CUBIC)
    cv2.Laplacian(template, cv2.CV_16U, template, 3)  # sharpen template for more accuracy
    matchResult = cv2.matchTemplate(imgToDetect, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(matchResult >= threshold)  # get all the suspect points from the result by the threshold.
    locations = list(zip(*locations[::-1]))  # change the presentation type of the points into tuples.
    CreateRectanglesFromLocations(rectangles, locations, templateWidth, templateHeight)


PositiveTemplateNames = glob.glob("ReferenceImages/P/*.jpg")
NegetiveTemplateNames = glob.glob("ReferenceImages/N/*.png")
PTemplateList = [cv2.imread(img, 0) for img in PositiveTemplateNames]
NTemplateList = [cv2.imread(img, 0) for img in NegetiveTemplateNames]
imgToDetect = cv2.imread("ReferenceImages/ImagesToDetect/4.jpg", 0)
rectangles = []
rectanglesEps = 0.5
positiveThreshold = 0.4
negetiveThreshold = 0.45

cv2.Laplacian(imgToDetect, cv2.CV_16U, imgToDetect, 3)
# Detect flowers:
for template in PTemplateList:
    DetectObjectByTemplate(imgToDetect, template, positiveThreshold, rectangles)

rectangles, weightsNotUsed = cv2.groupRectangles(rectangles, 1, rectanglesEps)

# Detect false positives:
for template in NTemplateList:
    index = 0
    tempRectangles = []
    #   template = cv2.resize(template, None, None, 0.1, 0.1, cv2.INTER_CUBIC)
    #   cv2.Laplacian(template, cv2.CV_16U, template, 3)  # sharpen template for more accuracy
    print(len(rectangles))
    for rec in rectangles:
        isFalsePositive = DetectFalsePositiveByNegetiveTemplate(imgToDetect, rec, template, negetiveThreshold)
        if not isFalsePositive:
            tempRectangles.append(rec)


    rectangles = tempRectangles
    print(len(rectangles))

if len(rectangles):
    DrawRectanglesOnImage(rectangles, imgToDetect)

cv2.imshow("Final", imgToDetect)
cv2.waitKey()

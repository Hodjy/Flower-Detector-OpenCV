import cv2
import numpy as np


def __createRectanglesFromLocations(rectangles, locations, w, h):
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


def __detectFalsePositiveByNegetiveTemplate(imgToDetect, rec, template, threshold):
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


def __detectObjectByTemplate(imgToDetect, template, threshold, rectangles):  # inserts result values into rectangles.
    templateWidth = template.shape[1]
    templateHeight = template.shape[0]
    matchResult = cv2.matchTemplate(imgToDetect, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(matchResult >= threshold)  # get all the suspect points from the result by the threshold.
    locations = list(zip(*locations[::-1]))  # change the presentation type of the points into tuples.
    __createRectanglesFromLocations(rectangles, locations, templateWidth, templateHeight)

def DetectPositive(imgToDetect, PTemplateList, positiveThreshold, rectangles):
    for template in PTemplateList:
        __detectObjectByTemplate(imgToDetect, template, positiveThreshold, rectangles)


def DetectNegative(imgToDetect, NTemplateList, rectangles, negetiveThreshold):
    for template in NTemplateList:
        tempRectangles = []
        for rec in rectangles:
            isFalsePositive = __detectFalsePositiveByNegetiveTemplate(imgToDetect, rec, template,
                                                                    negetiveThreshold)
            if not isFalsePositive:
                tempRectangles.append(rec)

        rectangles = tempRectangles
        print(len(rectangles))

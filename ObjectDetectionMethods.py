import cv2
import numpy as np


def __mergeRectangleLists(firstList, secondList):
    newList = []
    for item in firstList:
        newList.append(item)

    for item in secondList:
        newList.append(item)

    return newList


def __createRectanglesFromLocations(rectangles, locations, w, h):
    for loc in locations:
        rec = [int(loc[0]), int(loc[1]), w, h]  # x, y, width, height
        rectangles.append(rec)  # append two times in cause there is only one rectangle around an area so
        rectangles.append(rec)  # groupRectangles wont remove it.


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
            isFalsePositive = True

    return isFalsePositive


def __detectObjectByTemplate(imgToDetect, template, threshold, rectangles):  # inserts result values into rectangles.
    templateWidth = template.shape[1]
    templateHeight = template.shape[0]
    matchResult = cv2.matchTemplate(imgToDetect, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(matchResult >= threshold)  # get all the suspect points from the result by the threshold.
    locations = list(zip(*locations[::-1]))  # change the presentation type of the points into tuples.
    __createRectanglesFromLocations(rectangles, locations, templateWidth, templateHeight)


def DetectPositive(imgToDetect, PTemplateList, positiveThreshold, rectanglesEps):
    rectanglesToReturn = []
    for template in PTemplateList:
        rectangles = []
        # print(i)
        __detectObjectByTemplate(imgToDetect, template, positiveThreshold, rectanglesToReturn)
    rectanglesToReturn = __makeBoxes(rectanglesToReturn)
    rectanglesToReturn = non_max_suppression_fast(rectanglesToReturn, rectanglesEps)
    rectanglesToReturn = __makeRectangelsFromBoxes(rectanglesToReturn)
    # rectanglesToReturn = __mergeRectangleLists(rectanglesToReturn, [])
    # rectanglesToReturn, weightsNotUsed = cv2.groupRectangles(rectanglesToReturn, 1, rectanglesEps)
    return rectanglesToReturn


def DetectNegative(imgToDetect, NTemplateList, rectangles, negetiveThreshold):
    print(len(rectangles))
    for template in NTemplateList:
        tempRectangles = []
        for rec in rectangles:
            isFalsePositive = __detectFalsePositiveByNegetiveTemplate(imgToDetect, rec, template,
                                                                      negetiveThreshold)
            if not isFalsePositive:
                tempRectangles.append(rec)

    print(len(tempRectangles))
    return tempRectangles

def __makeBoxes(rectangles):
    boxes = []
    for rec in rectangles:
        boxes.append((float(rec[0]), float(rec[1]), float(rec[2] + rec[0]), float(rec[3] + rec[1])))

    return np.array(boxes)

def __makeRectangelsFromBoxes(Boxes):
    rectangles = []
    for box in Boxes:
        rectangles.append((int(box[0]), int(box[1]), int(box[2] - box[0]), int(box[3] - box[1])))

    return rectangles

def non_max_suppression_fast(rectangles, overlapThresh):
    # if there are no rectangles, return an empty list
    if len(rectangles) == 0:
        return []

    if rectangles.dtype.kind == "i":
        rectangles = rectangles.astype("float")
    # initialize the list of picked indexes
    pick = []
    # grab the coordinates of the bounding rectangles
    x1 = rectangles[:, 0]
    y1 = rectangles[:, 1]
    x2 = rectangles[:, 2]
    y2 = rectangles[:, 3]
    # compute the area of the bounding rectangles and sort the bounding
    # rectangles by the bottom-right y-coordinate of the bounding rectangle
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]
        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
                                               np.where(overlap > overlapThresh)[0])))
    # return only the bounding boxes that were picked using the
    # integer data type
    return rectangles[pick].astype("int")

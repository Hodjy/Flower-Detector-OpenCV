import cv2
import numpy as np


def __mergeRectangleLists(firstList, secondList):
    newList = []
    for item in firstList:
        newList.append(item)

    for item in secondList:
        newList.append(item)

    return newList


def __detectFalsePositiveByNegetiveTemplate(imgToDetect, rec, template, threshold):
    x = rec[0] #Taking the top left and the bottom right points of the template
    y = rec[1] #And creating the region of interest (ROI) from the image.
    x2 = rec[2] #
    y2 = rec[3] #
    roi = imgToDetect[y:y2, x:x2]
    isFalsePositive = False
    isTemplateSizeEqualToRoi = roi.shape[0] == template.shape[0] and roi.shape[1] == template.shape[1]

    if isTemplateSizeEqualToRoi:  # If smaller check for false positive.
        matchResult = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED) # In the same way we found positives,
        locations = np.where(matchResult >= threshold)                       # we look for negative with the
        locations = list(zip(*locations[::-1]))                              # template on the ROI
        if len(locations): # If we have locations then it means we have a false positive.
            #cv2.imshow("1", roi)
            #cv2.imshow("2", template)
            #cv2.imshow("3", matchResult)
            #cv2.waitKey()
            isFalsePositive = True

    return isFalsePositive


def __createRectanglesFromLocations(rectangles, locations, w, h, confidance): # Gets (x,y,w,h) locations and builds a rectangle by
                                                                  # making a top left point and a botton right point.
                                                                  # getting the confidance for each proper location and
                                                                  # saving it in the rectangle for later use.
    i = 0
    for loc in locations:
        rec = [int(loc[0]), int(loc[1]), w + loc[0], h + loc[1], confidance[i]]  # x, y, width, height
        rectangles.append(rec)  # append two times in cause there is only one rectangle around an area so
        #rectangles.append(rec)  # groupRectangles wont remove it.
        i += 1


def __getDetectionConfidanceList(matchResult, locations): #By getting the value of the pixel, we can know our confidance
                                                          #in the possability of getting the correct object.
    confidance = []
    for y, x in locations:
        confidance.append(matchResult[x, y])

    return confidance


def __detectObjectByTemplate(imgToDetect, template, threshold, rectangles):  # inserts result values into rectangles.
    templateWidth = template.shape[1]
    templateHeight = template.shape[0]
    matchResult = cv2.matchTemplate(imgToDetect, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(matchResult >= threshold)  # get all the suspect points from the result by the threshold.
    locations = list(zip(*locations[::-1]))  # change the presentation type of the points into tuples.
    if len(locations):
        confidance = __getDetectionConfidanceList(matchResult, locations)
        __createRectanglesFromLocations(rectangles, locations, templateWidth, templateHeight, confidance)



def __groupOverlappingRectangles(rectangles, overlapThresh):  # merging overlapping rectangles by a given
                                                              # threshold, using "max_suppression_fast" way.
    # if there are no rectangles, return an empty list
    if len(rectangles) == 0:
        return []

    # Turnes "rectangles" from list to numpy type array.
    rectangles = np.array(rectangles)
    # If it is not float type, turn it into float in order to perform division.
    if rectangles.dtype.kind == "i":
        rectangles = rectangles.astype("float")
    # initialize the list of picked indexes
    pick = []
    # take the coordinates of the bounding rectangles
    x1 = rectangles[:, 0]
    y1 = rectangles[:, 1]
    x2 = rectangles[:, 2]
    y2 = rectangles[:, 3]
    # take the confidence of the bounding rectangles
    confidence = rectangles[:, 4]
    # compute the area of the bounding rectangles and sort the bounding
    # rectangles by the bottom-right y-coordinate of the bounding rectangle
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    indexs = np.argsort(confidence)
    # keep looping while some indexes still remain in the indexes
    # list
    while len(indexs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(indexs) - 1
        i = indexs[last]
        pick.append(i)
        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[indexs[:last]])
        yy1 = np.maximum(y1[i], y1[indexs[:last]])
        xx2 = np.minimum(x2[i], x2[indexs[:last]])
        yy2 = np.minimum(y2[i], y2[indexs[:last]])
        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / area[indexs[:last]]
        # delete all indexes from the index list that have
        indexs = np.delete(indexs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))
    # return only the bounding boxes that were picked using the
    # integer data type
    return rectangles[pick].astype("int")  # returns the rectangles as int for later calculations.


def DetectPositive(imgToDetect, PTemplateList, positiveThreshold, rectanglesEps): # returns detected ROI's in the rectangles
    rectanglesToReturn = []
    for template in PTemplateList: # Every loop, detect the object with the current template, and update "rectanglesToReturn"
        __detectObjectByTemplate(imgToDetect, template, positiveThreshold, rectanglesToReturn)

    rectanglesToReturn = __groupOverlappingRectangles(rectanglesToReturn, rectanglesEps)
    rectanglesToReturn = __groupOverlappingRectangles(rectanglesToReturn, rectanglesEps)

    return rectanglesToReturn


def DetectNegative(imgToDetect, NTemplateList, rectangles, negativeThreshold): #Detects false positive by using matchTemplate
                                                                               #on every rectangle for every negative template by a negativeThreshold.
                                                                               #If it does find, it will remove the rectangle from the rectangle list.
    for template in NTemplateList:
        tempRectangles = []
        for rec in rectangles:
            isFalsePositive = __detectFalsePositiveByNegetiveTemplate(imgToDetect, rec, template,
                                                                      negativeThreshold)
            if not isFalsePositive:
                tempRectangles.append(rec)

        rectangles = tempRectangles

    return rectangles


def DrawRectanglesOnImage(rectangles, imgToDrawOn):
    lineColor = (255, 0, 0)
    lineType = cv2.LINE_4

    for (x, y, x2, y2, confidanceNotUsed) in rectangles:
        topLeft = (x, y)
        bottomRight = (x2, y2)
        cv2.rectangle(imgToDrawOn, topLeft, bottomRight, lineColor, lineType)


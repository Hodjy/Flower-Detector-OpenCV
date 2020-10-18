import cv2
import numpy as np


def __detectFalsePositiveByNegetiveTemplate(imgToDetect, rec, template, threshold):
    # Taking the top left and the bottom right points of the template
    # and creating the region of interest (ROI) from the image.
    x = rec[0]
    y = rec[1]
    x2 = rec[2]
    y2 = rec[3]
    roi = imgToDetect[y:y2, x:x2]
    isFalsePositive = False
    #Check if template is equal to roi.
    isTemplateSizeEqualToRoi = roi.shape[0] == template.shape[0] and roi.shape[1] == template.shape[1]
    # If smaller check for false positive.
    if isTemplateSizeEqualToRoi:
        # In the same way we found positives, we look for negative with the template on the ROI
        matchResult = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(matchResult >= threshold)
        locations = list(zip(*locations[::-1]))
        # If we have data in locations then it means we have a false positive.
        if len(locations):
            isFalsePositive = True

    return isFalsePositive


def __createRectanglesFromLocations(rectangles, locations, w, h, confidence):
    # Gets (x,y,w,h) locations and builds a rectangle by making a top left point and a botton right point.
    # getting the proper confidence for each proper location and saving it in the rectangle for later use.
    i = 0
    for loc in locations:
        rec = [int(loc[0]), int(loc[1]), w + loc[0], h + loc[1], confidence[i]]  # x, y, width, height
        rectangles.append(rec)
        i += 1


def __getDetectionConfidenceList(matchResult, locations):
    # By getting the value of the pixel, we can know our confidence in the possibility of getting the correct object.
    # We make a confidence list by using the positions that locations list, and takeing the value at that position
    # from the matchResult. the confidence list will be in the same order as the locations list so merging everything
    # into rectangles wont be a problem.
    confidence = []
    for y, x in locations:
        confidence.append(matchResult[x, y])

    return confidence


def __detectObjectByTemplate(imgToDetect, template, threshold, rectangles):
    #Detects the object by using matchTemplate and a threshold, will get locations, and confidance rating for each
    #detection and convert everything to rectangels, then update the given rectangles list.

    #Inserts result values into rectangles.
    templateWidth = template.shape[1]
    templateHeight = template.shape[0]
    matchResult = cv2.matchTemplate(imgToDetect, template, cv2.TM_CCOEFF_NORMED)
    # Get all the suspect points from the result by the threshold.
    locations = np.where(matchResult >= threshold)
    # Convert the type of the points into tuples.
    locations = list(zip(*locations[::-1]))
    if len(locations): #If we got detections
        #Get confidance list, that its order is the same as the locations list order.
        confidance = __getDetectionConfidenceList(matchResult, locations)
        #Update rectangles with new rectangels
        __createRectanglesFromLocations(rectangles, locations, templateWidth, templateHeight, confidance)



def __groupOverlappingRectangles(rectangles, overlapThresh):
    # merging overlapping rectangles by a given
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


def DetectPositive(imgToDetect, PTemplateList, positiveThreshold, rectanglesEps):
    # returns detected ROI's in the rectangles
    rectanglesToReturn = []
    # Every loop, detect the object with the current template, and update "rectanglesToReturn"
    for template in PTemplateList:
        __detectObjectByTemplate(imgToDetect, template, positiveThreshold, rectanglesToReturn)

    # Remove overlapping rectangles with the FNMS method.
    rectanglesToReturn = __groupOverlappingRectangles(rectanglesToReturn, rectanglesEps)

    return rectanglesToReturn


def DetectNegative(imgToDetect, NTemplateList, rectangles, negativeThreshold):
    # Detects false positive by using matchTemplate
    # on every rectangle for every negative template by a negativeThreshold.
    # If it does find, it will remove the rectangle from the rectangle list.
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
    # Define line color and type, then loop over all rectangles and draw them on the image.
    lineColor = (255, 0, 0)
    lineType = cv2.LINE_4

    for (x, y, x2, y2, confidanceNotUsed) in rectangles:
        topLeft = (x, y)
        bottomRight = (x2, y2)
        cv2.rectangle(imgToDrawOn, topLeft, bottomRight, lineColor, lineType)


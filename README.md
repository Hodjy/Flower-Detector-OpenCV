# Flower-Detector-OpenCV
A program that uses template matching in order to detect objects (in this case, flowers) in images.   

The program was made in a way that if the user would swap the positive template images to different image templates       
that focus on a different object (for example faces), the program would attempt to detect it.           

In order to run this program, simply download the files and run the main file with a python IDE.           

In order to increase the algorithm sensitivity for detection, decrease the positive threshold to the minimum of 1.0.          
To decrease the sensitivity, increase the positive threshold to the maximum of 1.0.       

By default, the algorithm compares the negative threshold (for false positive detection) to the positive threshold, unless its below 2.0.       

The following explenation is taken from my research file which i attached to the repository:        

## Introduction

I chose to use the OpenCV method “matchTemplate” in order to detect flowers on images.        

The reason for using “matchTemplate” is that it yields a correlation between a template to a target image,    
which makes implementing object detection possible by making the template the required object and the image the target to search it on.     

In order to get accurate results, I have used filters, positive and negative templates that were downloaded and edited from the internet.       

### Method:

Template matching is a method that is used to find locations that resemble a certain template in a bigger image.        
The method slides the given template on the target image and compares the template on the current area it overlaps.       

The method returns a grayscale image where the values of each pixel correlates to the similarity of his given area to the template. The higher the value for the pixel, the higher the correlation for that area, thus the match will be the best. (unless using, cv.TM_SQDIFF which will work in reverse.)       

For this project, I used matchTemplate with TM_CCOEFF_NORMED (Correlation coefficient Normalized) that performs this equation when sliding the template:        

![image](https://user-images.githubusercontent.com/62711261/109804557-0be61c80-7c2b-11eb-84fe-63500f9c67dc.png)

For example:      

Image(left) and One Template(right)     

![image](https://user-images.githubusercontent.com/62711261/109804683-320bbc80-7c2b-11eb-9e8e-603c48b92651.png)

The result:     

![image](https://user-images.githubusercontent.com/62711261/109804852-64b5b500-7c2b-11eb-9e36-004da37dfb25.png)

The higher value the pixel is, the higher the correlation for the template.


## The Algorithm

For positive detection the algorithm uses matchTemplate and a predefined threshold for every positive template on the image. Then it creates rectangles that contain their dimensions,and the corresponding pixel value from the result of the matchTemplate, which will be referred to as “confidence” rating.

After finishing positive detection, it groups all overlapping rectangles with a predefined threshold and uses each of their “confidence” ratings in the process.

After finishing grouping it initiates negative detection that uses template matching and a predefined negative threshold for every negative template on all the equal sized ROI’s, and will delete the ROI if the result was above the negative Threshold.

## Templates Examples

### Positive Templates
![image](https://user-images.githubusercontent.com/62711261/109805376-0806ca00-7c2c-11eb-902a-354370db1167.png)

### Negative Templates
![image](https://user-images.githubusercontent.com/62711261/109805464-22d93e80-7c2c-11eb-84ed-ba8d2c466bc4.png)


## Results

### Examples

Threshold 0.4, time elapsed 1.17~ seconds:         
![image](https://user-images.githubusercontent.com/62711261/109805182-cd9d2d00-7c2b-11eb-88ee-d930a83baf0c.png)

Threshold 0.4, time elapsed 1.31~ seconds:         
![image](https://user-images.githubusercontent.com/62711261/109805276-ead1fb80-7c2b-11eb-93db-f75151645549.png)

Threshold 0.4, time elapsed 1.13~ seconds:      
![image](https://user-images.githubusercontent.com/62711261/109805893-ac890c00-7c2c-11eb-811b-dedc50e1d08d.png)       


because the results were better for the lower amount of templates, I started with  the lower templates for the result phase.      

After passing the threshold of 0.5, the results were mostly false negatives, so the graphs are focused on the thresholds between 0.1-0.5.       

Success will be calculated by taking each true positive to flower ratio in every picture and averaging it across all pictures on that threshold.        

Because the algorithm groups small rectangles when they overlap in a bigger one, I will account for the bigger one as success for all the batched flowers.        

The amount of false positives for every picture across the threshold(positive threshold).         

For the negative threshold, it will be equal to the positive threshold unless the positive threshold is smaller than 0.2, then the negative threshold will be 0.15. 

### Graphs

The data was calculated with 18 positive, and 13 negative templates. 26 images where used for detection.

#### Success Graphs 

![image](https://user-images.githubusercontent.com/62711261/109806734-b7906c00-7c2d-11eb-94e9-86e00dabf5da.png)     

![image](https://user-images.githubusercontent.com/62711261/109806756-bf501080-7c2d-11eb-940c-055d64ac5cb0.png)     

![image](https://user-images.githubusercontent.com/62711261/109806791-c8d97880-7c2d-11eb-8e9d-9131b4429b04.png)

#### False Positive Graphs







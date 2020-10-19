# Flower-Detector-OpenCV
A program that uses template matching in order to detect objects (in this case, flowers) in images.   

The program was made in a way that if the user would swap the positive template images to different image templates     
that focus on a different object (for example faces), the program would attempt to detect it.     

In order to run this program, simply download the files and run them with a python IDE.   

In order to increase the algorithm sensitivity for detection, decrease the positive threshold to the minimum of 1.0.    
To decrease the sensitivity, increase the positive threshold to the maximum of 1.0.

By default, the algorithm compares the negative threshold (for false positive detection) to the positive threshold, unless its below 2.0.

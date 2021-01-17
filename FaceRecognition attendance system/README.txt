# Face Recognition

Face Recognition using OpenCV in Python

### Prerequisites

Numpy
OpenCV
xlrd
xlwrite
xlutils


### Installing

1.download anaconda3 with pycharm for anaconda
2.import libraries and modules in (settings/project interpreter/add) 



### Running the program

open video_to_img folder and run videotoimg.py
1.this program will capture every frame
2.the person should sit in front of camera and look directly at the camera
3.now he should turn his head slightly up and down then sideways
4.close the program when you have sufficient good images
5.now move these photos in a folder in trainingimages
6.If you want to train clasifier to recognize multiple people then add each persons folder in separate label markes as 0,1,2,etc 
7.make sure folder names are integers (starting from 0) and leave 0 folder empty
8.repeat these steps till every person is registered

run resizeimages.py
make sure there are empty folders with respective names as in tainingimages folder in resizedtrainingimages folder 

### make sure to make changes accordingly in class_strength and name variables in programs
### also check directory variable in final program

Run Tester.py script train recognizer on training images and also predict test_img:
1.Place some test images in TestImages folder that you want to predict  in tester.py file
2.To do test run via tester.py give the path of image in test_img variable
3.now a yml file will be saved which can be used to recognise faces without training database all over again

run make_basic_excel_template.py
1.an xlsx file named attendance will be saved

run final program 


## Acknowledgments
* http://www.toptechboy.com/raspberry-pi-with-linux-lessons/
* https://www.superdatascience.com/opencv-face-recognition/
* https://towardsdatascience.com/a-guide-to-face-detection-in-python-3eab0f6b9fc1
* https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/
* https://www.pyimagesearch.com/2018/07/19/opencv-tutorial-a-guide-to-learn-opencv/
* https://xlrd.readthedocs.io/en/latest/#
* https://xlsxwriter.readthedocs.io/

On Thu, 9 Jan 2020, 10:26 Mayank Vaishya, <mayank3290@gmail.com> wrote:


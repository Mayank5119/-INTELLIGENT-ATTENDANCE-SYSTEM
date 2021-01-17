import cv2
import os
import numpy as np
import faceRecognition as fr
import excel_templete_new as excel_template
import read_tt


# if error 'cv2.cv2' has no attribute 'face' shows up - install opencv-contrib-python

def train():

    # read time table and class names
    read_tt.read_tt_and_names()
    # making excel template
    excel_template.make_template()

    # This module takes images  stored in disk and performs face recognition
    test_img_name = str(input("image name : "))
    test_img = cv2.imread('TestImages/' + test_img_name + '.jpg')  # test_img path

    # detect all the faces in image
    faces_detected, gray_img = fr.faceDetection(test_img)
    print("faces_detected:", faces_detected)
    # counter for keeping face count
    face_count = len(faces_detected)
    print("face_count:", face_count)

    faces, faceID = fr.labels_for_training_data('trainingImages')
    face_recognizer = fr.train_classifier(faces, faceID)
    # have to store our trained data so we can use it later without going through the training process again
    face_recognizer.write('trainingData.yml')
    # use this .yml file in future to avoid training time

    # creating dictionary containing names for each label
    name = np.load("names.npy", allow_pickle=True, fix_imports=True)
    name = name.item()

    # id of students present in class
    present = []

    for face in faces_detected:
        (x, y, w, h) = face
        roi_gray = gray_img[y:y + h, x:x + h]
        label, confidence = face_recognizer.predict(roi_gray)  # predicting the label of given image
        present.append(label)
        fr.draw_rect(test_img, face)  # drawing rectangle on face
        predicted_name = name[label]
        fr.put_text(test_img, predicted_name, x, y)  # printing name of the person

    # # print ids of present students
    # present.sort()
    print(present)
    # cv2.imshow("test image", resized_img)
    cv2.waitKey(0)  # Waits indefinitely until a key is pressed
    cv2.destroyAllWindows()

# train()
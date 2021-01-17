import cv2
import os
import numpy as np

# This module contains all common functions that are called in train.py file
# function - faceDetection(test_img)               returns - faces, gray_img
# function - labels_for_training_data(directory)   returns - faces, faceID
# function - train_classifier(faces, faceID)       returns - face_recognizer
# function - draw_rect(test_img, face)             returns - NIL
# function - put_text(test_img, text, x, y)        returns - NIL



# Given an image below function returns rectangle for face detected along with gray scale image
def faceDetection(test_img):
    gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)  # convert color image to grayscale
    face_haar_cascade = cv2.CascadeClassifier('HaarCascade/haarcascade_frontalface_default.xml')  # Load haar classifier
    faces = face_haar_cascade.detectMultiScale(gray_img, scaleFactor=1.32, minNeighbors=5)  # detectMultiScale returns
    # rectangles
    return faces, gray_img


def FaceAligner(test_img):

    eye_haar_cascade = cv2.CascadeClassifier('HaarCascade/haarcascade_eye.xml')
    face, gray = faceDetection(test_img)

    if len(face) == 0:
        print("face not detected")
        return [], gray

    print(face[0])
    for (x, y, w, h) in face:

        print(x, y, w, h)

        roi_gray = gray[y:y + h, x:x + w]
        # cv2.imshow("window_name", roi_gray)
        # cv2.waitKey(0)
        # roi_color = test_img[y:y + h, x:x + w]
        eyes = eye_haar_cascade.detectMultiScale(roi_gray)
        left_eye = eyes[0]
        right_eye = eyes[1]

        (fx, fy, fw, fh) = (x, y, w, h)
        (lex, ley, lew, leh) = left_eye
        (rex, rey, rew, reh) = right_eye

        rx = lex - fx
        ry = fy + fh - (ley + leh)

        lx = rex - (fx + fw/2)
        ly = fy + fh - (rey + reh)

        eyeXdis = (lx + w / 2 + lew / 2) - (rx + rew / 2)
        eyeYdis = (ly + leh / 2) - (ry + reh / 2)
        angle_rad = np.arctan(eyeYdis / eyeXdis)
        # convert rad to degree
        angle_degree = angle_rad * 180 / np.pi

        # Find the center of the image
        image_center = tuple(np.array(roi_gray.shape) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle_degree, 1.0)
        rotated_image = cv2.warpAffine(roi_gray, rot_mat, roi_gray.shape, flags=cv2.INTER_LINEAR)

        return rotated_image

        # gray_img = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)  # convert color image to grayscale
        # face_haar_cascade = cv2.CascadeClassifier('HaarCascade/haarcascade_frontalface_default.xml')  # Load haar classifier
        # faces = face_haar_cascade.detectMultiScale(gray_img, scaleFactor=1.32, minNeighbors=5)  # detectMultiScale returns
        # rectangles

        # return (x, y, w, h), gray


# Given a directory below function returns part of gray_img which is face alongwith its label/ID
# directory --> folders/subdir --> files
def labels_for_training_data(directory):
    faces = []
    faceID = []

    for path, subdirnames, filenames in os.walk(directory):
        for filename in filenames:  # iterating on all the files in directory
            if filename.startswith("."):
                print("Skipping system file")  # Skipping files that startwith .
                continue

            id = os.path.basename(path)  # fetching subdirectory names
            img_path = os.path.join(path, filename)  # fetching image path
            print("img_path:", img_path)
            print("id:", id)
            test_img = cv2.imread(img_path)  # loading each image one by one
            if test_img is None:
                print("Image not loaded properly")
                continue
            faces_rect, gray_img = faceDetection(test_img)  # Calling faceDetection function to return faces detected in
            # particular image

            # during training only one face should be detected, otherwise training will be erroneous
            if len(faces_rect) != 1:
                continue  # Since we are assuming only single person images are being fed to classifier
            (x, y, w, h) = faces_rect[0]
            roi_gray = gray_img[y:y+w, x:x+h]  # cropping region of interest i.e. face area from grayscale image
            faces.append(roi_gray)
            faceID.append(int(id))
    return faces, faceID


# Below function trains haar classifier and takes faces,faceID returned by previous function as its arguments
def train_classifier(faces, faceID):
    print(dir(cv2.face))
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(faceID))
    return face_recognizer


# Below function draws bounding boxes around detected face in image
def draw_rect(test_img, face):
    (x, y, w, h) = face
    cv2.rectangle(test_img, (x, y), (x+w, y+h), (255, 0, 0), thickness=3)


# Below function writes name of person for detected label
def put_text(test_img, text, x, y):
    cv2.putText(test_img, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 4)












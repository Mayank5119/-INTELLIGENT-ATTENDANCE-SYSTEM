import faceRecognition as fr
import numpy as np
import cv2

def FaceAligner(test_img_path):

    test_img = cv2.imread(test_img_path)
    eye_haar_cascade = cv2.CascadeClassifier('HaarCascade/haarcascade_eye.xml')
    # face, gray = fr.faceDetection(test_img)

    gray = cv2.cvtColor(test_img, cv2.COLOR_RGB2GRAY)  # convert color image to grayscale
    face_haar_cascade = cv2.CascadeClassifier('HaarCascade/haarcascade_frontalface_default.xml')  # Load haar classifier
    face = face_haar_cascade.detectMultiScale(gray, scaleFactor=1.32, minNeighbors=5)  # detectMultiScale returns
    print(face)
    for (x, y, w, h) in face:
        roi_gray = gray[y:y + h, x:x + w]
        cv2.imshow("window_name", roi_gray)
        cv2.waitKey(0)
        roi_color = test_img[y:y + h, x:x + w]
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
        cv2.imshow("window_name", rotated_image)
        cv2.waitKey(0)
    return rotated_image

img2 = cv2.imread(r"D:\Study Material\csio project\FaceRecognition-mach4 (final)\TestImages\frame0.jpg")
cv2.imshow("", img2)
cv2.waitKey(0)
img = FaceAligner(r"D:\Study Material\csio project\FaceRecognition-mach4 (final)\TestImages\frame0.jpg")
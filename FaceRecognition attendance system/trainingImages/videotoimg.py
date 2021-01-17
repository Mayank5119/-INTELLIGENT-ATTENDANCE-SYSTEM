import cv2
import time
import faceRecognition as fr
import os

sid = input("enter your SID : ")
os.mkdir(sid)

# initialise webcam
cap = cv2.VideoCapture(0)

path = os.getcwd()

count = 0
while count < 50:

    os.chdir(path)

    # This code initiates an infinite loop (to be broken later by a break statement), where we have ret and frame being
    # defined as the cap.read(). Basically, ret is a boolean regarding whether or not there was a return at all, at the
    # frame is each frame that is returned. If there is no frame, you wont get an error, you will get None.
    ret, test_img = cap.read()
    if not ret:
        continue
    faces, gray_img = fr.faceDetection(test_img)
    if len(faces) == 1:
        resized_img = cv2.resize(test_img, (1000, 700))
        cv2.imshow('face detection Tutorial ', resized_img)

        os.chdir(sid)

        cv2.imwrite(r"frame%d.jpg" % count, test_img)  # save frame as JPG file
        # print("img written!")
        count += 1
        if count % 10:
            print(count)
        if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
            break



cap.release()
cv2.destroyAllWindows()


import PySimpleGUI as sg
from typing import Any
import cv2
import os
import numpy as np
import faceRecognition as fr
import xlrd
import xlutils
import datetime
import os
import pandas as pd
import copy
import time
import sys
import train as Train


def main(sid, name, status, curr_period):

    sg.theme('LightGreen')

    # define the window layout
    layout = [
        [sg.Text('OpenCV Demo', size=(60, 1), justification='center')],
        [sg.Image(filename='', key='-IMAGE-')],
        [sg.Text("SID here :" + str(sid), key='-SID-'), sg.Text("Name:" + str(name), key='-NAME-'),
         sg.Text("Attendance Status :" + str(status), key='-status-')],
        [sg.Text("Current Period :" + str(curr_period), key='-curr_period-')],
        [sg.Text("Current Date & time :" + str(sid), key='-TIME-'),
         sg.Text("Attendance End at :" + str(sid))],
        [sg.Text("Your temperature :" + str(sid), key='-curr_period-')],
        [sg.Button('Exit', size=(10, 1))],
    ]

    window = sg.Window('Attendance System', layout, location=(800, 400))

    cap = cv2.VideoCapture(0)

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        ret, frame = cap.read()

        imgbytes = cv2.imencode('.png', frame)[
            1].tobytes()  # address to te source iMAGE of screen display can be taken as face title from main proramme
        window['-IMAGE-'].update(data=imgbytes)

    window.close()






def comparetime(time):
    time = time.replace(":", "")
    time = int(time)
    return time

directory = os.getcwd()
test = os.listdir(directory)

flag = 0
for item in test:
    if item.endswith(".yml"):
        flag = 1

if flag == 0:
    Train.train()

else:

    curr_time = str(datetime.datetime.now().time())
    start_time = comparetime(curr_time[0: 5])

    weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    today_date = datetime.datetime.now()
    day = today_date.weekday()

    arr = np.load('starting_times.npy', allow_pickle=True, fix_imports=True)
    todays_time_table = arr[day]

    print(todays_time_table)

    name = np.load("names.npy", allow_pickle=True, fix_imports=True)
    # print(name.item()[1])  # dict.item() is the way to access the dictionary as name is now an object of class nparray

    m = 10000
    period = None
    period_start = 0
    for keys in todays_time_table:
        d = abs(start_time - comparetime(keys))
        if d < m:
            m = d
            period_start = comparetime(keys)
            period = todays_time_table[keys]

    curr_time = str(datetime.datetime.now().time())
    curr_time = curr_time[0: 5]

    while comparetime(str(curr_time)) - period_start <= 15 and comparetime(curr_time) - comparetime(str(period_start)) >= -55:

        curr_time = str(datetime.datetime.now().time())
        curr_time = curr_time[0: 5]

        face_cascade = cv2.CascadeClassifier('HaarCascade/haarcascade_frontalface_default.xml')

        cap = cv2.VideoCapture(0)


        face_count = 0
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for face in faces:
            face_count = face_count + 1

        if face_count:
            img_name = "opencv_frame_0.png"
            cv2.imwrite(img_name, img)  # save frame as JPG file
            print("img 0 written!")

        for (x, y, w, h) in faces:
            # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

        # cv2.imshow('img', img)

        cap.release()
        cv2.destroyAllWindows()

        # This module takes images  stored in disk and performs face recognition
        class_strength = len(name.item())

        face_count = 0
        test_img = cv2.imread("opencv_frame_0.png")
        faces_detected, gray_img = fr.faceDetection(test_img)
        # print("faces_detected:",faces_detected)
        for face in faces_detected:
            face_count = face_count + 1
        print("face_count:", face_count)

        try:
            # Get the user input and make it an integer
            condition = face_count
            # If a ValueError is raised, it means that the input was not a number
        except ValueError:
            # So, jump to the top of the loop and start-over
            continue
            # If we get here, then the input was a number.  So, see if it equals 1 or 2
        if condition == 0:
            # REMOVE THE PICTURE
            os.remove("opencv_frame_" + str(counter) + ".png")
            # If so, break the loop because we got valid input
            break

        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.read('trainingData.yml')  # use this to load training data for subsequent runs

        # creating list to store present SID
        present = []

        for face in faces_detected:
            (x, y, w, h) = face
            roi_gray = gray_img[y:y + h, x:x + h]
            label, surity = face_recognizer.predict(roi_gray)  # predicting the label of given image
            fr.draw_rect(test_img, face)
            print(label)
            predicted_name = name.item()[label]

            present.append(label)

        present.sort()
        print(present)

        today_date = datetime.date.today()

        wb = xlrd.open_workbook(period + ".xls")

        month = datetime.datetime.now().strftime("%m")

        # selecting correct worksheet
        for i in range(1, 13):

            if int(month) == i:
                w_sheet = wb.sheet_by_index(i - 1)

        # selecting correct column to input attendance
        row = 1
        col = 2

        for col in range(2, 34, 1):
            cell = w_sheet.cell(row, col)
            if str(today_date) == cell.value:
                break

        import xlsxwriter
        from xlutils.copy import copy

        new_wb = copy(wb)

        month = datetime.datetime.now().strftime("%m")
        # print(month)

        # selecting correct worksheet in new workbook
        for i in range(1, 13):
            if int(month) == i:
                w_sheet = new_wb.get_sheet(i - 1)

        # Start from the row and col obtained from above.
        row = row + 1
        # Iterate over the data and write it out row by row.
        for SID in range(1, class_strength + 1, 1):
            if SID in present:
                w_sheet.write(row, col, "p " + curr_time)
            row += 1

        new_wb.save(period + ".xls")

        main(present[0], predicted_name, "p", period)

        print(predicted_name)

        cv2.waitKey(0)  # Waits indefinitely until a key is pressed
        cv2.destroyAllWindows()


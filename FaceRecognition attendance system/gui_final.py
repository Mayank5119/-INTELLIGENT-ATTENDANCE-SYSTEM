import PySimpleGUI as sg
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


def gui(sid, name, status, curr_period, curr_time, start_time , temperature ,img):
    if len(sid) == 0:
        return
    else:
        sid = sid[0]
        sg.theme('LightGreen')

        # define the window layout
        layout = [
            [sg.Text('OpenCV Demo', size=(60, 1), justification='center')],
            [sg.Image(filename='', key='-IMAGE-')],
            [sg.Text("SID here :" + str(sid), key='-SID-'), sg.Text("Name:" + str(name), key='-NAME-'),
             sg.Text("Attendance Status :" + str(status), key='-status-')],
            [sg.Text("Current Period :" + str(curr_period), key='-curr_period-'),
            sg.Text("Time :" + str(curr_time) , key='-TIME-')],
             # sg.Text("Attendance started at :" + str(start_time))],
            [sg.Text("Your temperature :" + str(temperature), key='-your_temp-')],
           # [sg.Button('Exit', size=(10, 1))],
        ]

        window = sg.Window('Attendance System', layout, location=(800, 400), finalize=True)

        imgbytes = cv2.imencode('.png', img)[
            1].tobytes()  # address to te source iMAGE of screen display can be taken as face title from main proramme
        window['-IMAGE-'].update(data=imgbytes)

        time.sleep(4)

        window.close()


def comparetime(time):
    time = time.replace(":", "")
    time = int(time)
    return time


def is_data_trained():
    directory = os.getcwd()
    files = os.listdir(directory)
    for item in files:
        if item.endswith(".yml"):
            return 1
    return 0


def curr_period_and_period_start_time(todays_time_table, start_time):
    m = 10000
    period = None
    period_start = 0
    for keys in todays_time_table:
        d = abs(start_time - comparetime(keys))
        if d < m:
            m = d
            period_start = comparetime(keys)
            period = todays_time_table[keys]
    return period, period_start


def save_in_sheet(class_strength, present, curr_period, month, today_date):
    wb = xlrd.open_workbook(str(curr_period) + ".xls")
    # selecting correct worksheet
    w_sheet = None
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

    # selecting correct worksheet in new workbook
    for i in range(1, 13):
        if int(month) == i:
            w_sheet = new_wb.get_sheet(i - 1)

    # Start from the row and col obtained from above.
    row = row + 1
    # Iterate over the data and write it out row by row.
    for SID in range(18105001, 18105130, 1):
        if SID in present:
            w_sheet.write(row, col, "p")
        row += 1

    new_wb.save(str(curr_period) + ".xls")


if not is_data_trained():
    Train.train()

curr_time = str(datetime.datetime.now().time())
start_time = comparetime(curr_time[0: 5])

month = datetime.datetime.now().strftime("%m")
weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
today_date = datetime.date.today()

day = datetime.datetime.now().weekday()

arr = np.load('starting_times.npy', allow_pickle=True, fix_imports=True)
todays_time_table = arr[day]
print(todays_time_table)

name = np.load("names.npy", allow_pickle=True, fix_imports=True)
# print(name.item()[1])  # dict.item() is the way to access the dictionary as name is now an object of class nparray
class_strength = len(name.item())

# get current period and period start time
curr_period, curr_period_start_time = curr_period_and_period_start_time(todays_time_table, start_time)
curr_time = curr_time[0: 5]
print(curr_period)

# while comparetime(str(curr_time)) - curr_period_start_time <= 15 and comparetime(curr_time) - comparetime(
#         str(curr_period_start_time)) >= -55:
while 1:
    predicted_name = "none"
    curr_time = str(datetime.datetime.now().time())
    curr_time = curr_time[0: 5]

    face_cascade = cv2.CascadeClassifier('HaarCascade/haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    ret, img = cap.read()
    if not ret:
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    face_count = 0
    for face in faces:
        face_count = face_count + 1

    # if face_count:
    #     img_name = "opencv_frame_0.png"
    #     cv2.imwrite(img_name, img)  # save frame as JPG file
    #     print("img 0 written!")

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    # cv2.imshow('img', img)

    cap.release()
    cv2.destroyAllWindows()

    # This module takes images  stored in disk and performs face recognition
    faces_detected, gray_img = fr.faceDetection(img)
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('trainingData.yml')  # use this to load training data for subsequent runs
    # creating list to store present SID
    present = []

    for face in faces_detected:
        (x, y, w, h) = face
        roi_gray = gray_img[y:y + h, x:x + h]
        label, surity = face_recognizer.predict(roi_gray)  # predicting the label of given image
        # fr.draw_rect(test_img, face)
        # print(label, ":", surity)
        predicted_name = name.item()[label]
        present.append(label)

    print(label, ":", predicted_name)
    print("time :" ,curr_time)



    save_in_sheet(class_strength, present, curr_period, month, today_date)
    temperature = "NA"
    # gui(present, predicted_name, "p", curr_period, curr_time, start_time , temperature , img )
    # print(temperature)
    print("M")
    print("P")
    print()
    cv2.waitKey(0)  # Waits indefinitely until a key is pressed
    cv2.destroyAllWindows()

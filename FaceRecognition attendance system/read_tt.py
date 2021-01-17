import datetime
import xlrd
import xlutils
import os
import copy
import numpy
import pandas as pd
import numpy as np

def read_tt_and_names():
    df = pd.read_excel('names.xlsx')
    name = {}
    sid = df.SID
    names = df.name
    for i in range(len(sid)):
        name[sid[i]] = names[i]

    np.save("names.npy", name, allow_pickle=True, fix_imports=True)

    # print(name.item()[18105119])  # dict.item() is the way to access the dictionary as name is now an object of class nparray

    subjects = set()

    starting_times = [{}, {}, {}, {}, {}, {}, {}]
    wb = xlrd.open_workbook("tt.xlsx")
    w_sheet = wb.sheet_by_index(0)

    # print(w_sheet.cell(2, 4).value)

    col = 1
    while col < 10:
        start_time = str(w_sheet.cell(0, col)).split("-")[0][6:11].strip()
        for i in range(1, 8):
            cell = w_sheet.cell(i, col)
            if str(w_sheet.cell(i, col)) != "empty:''":
                subjects.add(cell.value)
                starting_times[i - 1][start_time] = cell.value
        col += 1

    subjects = [i for i in subjects]
    print(starting_times)  # check the stored arrays for each day
    print(subjects)

    numpy.save('starting_times', starting_times, allow_pickle=True, fix_imports=True)
    numpy.save('subjects', subjects, allow_pickle=True, fix_imports=True)



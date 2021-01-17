import xlutils
import xlrd
import xlsxwriter
import numpy as np
import pandas as pd

# creating dictionary containing names for each label
name = np.load("names.npy", allow_pickle=True, fix_imports=True)
name = name.item()
# df = pd.read_excel("names.xlsx")
# name = {}
# sid = df.SID
# names = df.name
# for i in range(len(sid)):
#     name[sid[i]] = names[i]

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december"]



def make_template():
    subjects = np.load('subjects.npy', allow_pickle=True, fix_imports=True)
    print(type(subjects))
    for i in range(len(subjects)):
        workbook = xlsxwriter.Workbook(str(subjects[i]) + '.xls')
        worksheets = []
        for i in months:
            worksheets.append(workbook.add_worksheet(i))

        # Add a bold format to use to highlight cells.
        cell_format_0 = workbook.add_format()
        cell_format_0.set_bold()
        cell_format_0.set_bg_color('gray')

        cell_format_1 = workbook.add_format()
        cell_format_1.set_bg_color('yellow')
        cell_format_1.set_right(1)

        for i in worksheets:
            i.write(1, 0, 'SID', cell_format_0)
            i.write(1, 1, 'Name', cell_format_0)

        for j in range(len(worksheets)):
            if j in [0, 2, 4, 6, 7, 9, 11]:
                date_counter = 1
                for d in range(1, 32, 1):
                    col = 1 + d
                    if date_counter < 10:
                        if j == 9 or j == 11:
                            date = "2020-" + str(j + 1) + "-" + '0' + str(date_counter)
                        else:
                            date = "2020-0" + str(j + 1) + "-" + '0' + str(date_counter)

                    else:
                        if j == 9 or j == 11:
                            date = "2020-" + str(j + 1) + "-" + str(date_counter)
                        else:
                            date = "2020-0" + str(j + 1) + "-" + str(date_counter)
                    worksheets[j].write(1, col, date, cell_format_0)
                    date_counter = date_counter + 1

            elif j == 1:
                # february
                date_counter = 1
                for d in range(1, 30, 1):
                    col = 1 + d
                    if date_counter < 10:
                        date = "2020-02-" + '0' + str(date_counter)
                    else:
                        date = "2020-02-" + str(date_counter)
                    worksheets[j].write(1, col, date, cell_format_0)
                    date_counter = date_counter + 1

            else:
                date_counter = 1
                for d in range(1, 31, 1):
                    col = 1 + d
                    if date_counter < 10:
                        if j == 10:
                            date = "2020-" + str(j + 1) + "-" + '0' + str(date_counter)
                        else:
                            date = "2020-0" + str(j + 1) + "-" + '0' + str(date_counter)
                    else:
                        if j == 10:
                            date = "2020-" + str(j + 1) + "-" + str(date_counter)
                        else:
                            date = "2020-0" + str(j + 1) + "-" + str(date_counter)
                    worksheets[j].write(1, col, date, cell_format_0)
                    date_counter = date_counter + 1


        for i in worksheets:
            # Start from the first cell. Rows and columns are indexed.
            row = 2
            col = 0
            # Iterate over the data and write it out row by row.
            SIDs = name.keys()
            for SID in SIDs:
                i.write(row, col, SID, cell_format_1)
                predicted_name = name[SID]
                i.write(row, col + 1, predicted_name, cell_format_1)
                row += 1

        workbook.close()

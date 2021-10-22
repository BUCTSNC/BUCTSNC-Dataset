# IMPORT

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from datetime import timedelta

import os
import string
import random

# READ FILENAME AND PRE-PRODUCER

filename_raw = os.listdir("C:/SNC/SNC_DATASET/2015")
filename_cleaned = []
filename_num = len(filename_raw)

for i in range(filename_num):
    ## BASIC CLEAN
    filename_raw[i] = filename_raw[i].replace("ftp-bq.ftp.buct.edu-", "")
    filename_raw[i] = filename_raw[i].replace(".log", "")
    filename_raw[i] = filename_raw[i].replace("-", "")
    filename_raw[i] = filename_raw[i].replace(" ", "")
    # filename_cleaned.append(filename_raw[int(i)])

    ## ADVANCED CLEAN
    flag_the_1 = 0
    string_the_1 = "(1)"
    flag_the_2 = 0
    string_the_2 = "(2)"
    flag_the_1_chinese = 0
    string_the_1_chinese = "（1）"
    flag_the_2_chinese = 0
    string_the_2_chinese = "（2）"
    flag_the_fuben = 0
    string_the_fuben = "副本"
    flag_the_copy = 0
    string_the_copy = "拷贝"
    # 好家伙，这天有两个
    if filename_raw[int(i)].find(string_the_1) != -1:
        flag_the_1 = 1
        print("At", i, "have the string", string_the_1)
        print(i, flag_the_1, flag_the_2, flag_the_1_chinese, flag_the_2_chinese, flag_the_copy, flag_the_fuben)
    if filename_raw[int(i)].find(string_the_2) != -1:
        flag_the_2 = 1
        print("At", i, "have the string", string_the_2)
        print(i, flag_the_1, flag_the_2, flag_the_1_chinese, flag_the_2_chinese, flag_the_copy, flag_the_fuben)
    if flag_the_1 == 0 and flag_the_2 == 0:
        filename_cleaned.append(filename_raw[int(i)])

filename_num = len(filename_cleaned)
print(filename_num, "/", len(filename_raw))

# DEFINE AND TRANSFORM TO ARRAY

filename_list = np.arange(filename_num)
filename_list = np.resize(filename_cleaned, (filename_num, 1))
calender = np.arange(filename_num * 3)
calender = np.resize(calender, (filename_num, 3))

for i in range(filename_num):
    num_of_year = int(filename_list[i]) // 10000
    num_of_month = (int(filename_list[i]) - num_of_year * 10000) // 100
    num_of_day = (int(filename_list[i]) - num_of_year * 10000 - num_of_month * 100) // 1
    calender[i][0] = int(num_of_year)
    calender[i][1] = int(num_of_month)
    calender[i][2] = int(num_of_day)
    # print(calender[i][0], "--", calender[i][1], "--", calender[i][2])

# CALCULATE GRID

days_of_year = int(365)  # 实际上要看到底是什么年的，应该可以获取，引入一个闰年判断吧
days_of_year_default = days_of_year
days_of_week = 7

axis_x = (days_of_year // days_of_week)
print(axis_x, days_of_week, axis_x * days_of_week, "[delta=", axis_x * days_of_week - days_of_year, "]")

axis_x = (days_of_year // days_of_week) + 1
print(axis_x, days_of_week, axis_x * days_of_week, "[delta=", axis_x * days_of_week - days_of_year, "]")

firstday_of_year = datetime(year=calender[0][0], month=1, day=1)  # 因为不一定有01月01日的数据，所以不能从数据中的首个算而是写死01.01
# print(dt_obj.weekday())
if firstday_of_year.weekday() != 1:
    days_of_year += int(firstday_of_year.weekday() - 1)

axis_x = (days_of_year // days_of_week) + 1

print(axis_x, days_of_week, axis_x * days_of_week, "[delta=", axis_x * days_of_week - days_of_year, "]")
print("[days_of_year now= ", days_of_year, "]", "[days_of_year default= ", days_of_year_default, "]")

# 所以53周是一定没问题的,不管是不是闰年(
# 经过推算，上一行有误，若第一天是周日，并且是闰年，将可以达到54周的跨度

day_of_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# CALCULATE EVERYDAY HEAT

date_grid = np.arange(axis_x * days_of_week)
date_grid = np.resize(date_grid, (axis_x, days_of_week))

## Draw shadowing
# print(Do NOTHING when calc)

## Draw Random
# for i in range(axis_x):
#     for j in range(days_of_week):
#         date_grid[i][j] = int(random.random() * 100)

## Draw Exactly data

day_offset = firstday_of_year.weekday() - 1
print("[day_offset =", day_offset, "]")
for m in range(axis_x):
    for n in range(days_of_week):
        date_grid[m][n] = int(0)
        # For Beauty Blues
        # date_grid[m][n] += int(1.98 * int(1 + (m // 2) * n))
        # For Beauty Blues
        date_grid[m][n] += 1.2 * int(1.88 * int(1 + (m // 2) * n * 0.8))
for i in range(filename_num):
    num_of_year = calender[i][0]
    num_of_month = calender[i][1]
    num_of_day = calender[i][2]
    day_series = num_of_day + day_offset
    if num_of_month >= 2 and num_of_month <= 12:
        for j in range(num_of_month - 1):
            day_series += day_of_month[j]
    # print(day_series, end="")
    num_of_week = day_series // days_of_week
    num_of_weekday = day_series % days_of_week
    # print("(", num_of_week, ",", num_of_weekday, ")")
    date_grid[num_of_week][num_of_weekday] = int(1)
    # For Beauty Default
    # date_grid[num_of_week][num_of_weekday] = (990 * int(1)) + num_of_weekday * 16.5 * (1 + int(num_of_month // 12))
    # For Beauty BuGn Blues
    date_grid[num_of_week][num_of_weekday] = (990 * int(1)) + num_of_weekday * 16.5 + 3.14 * (
                1 + int(num_of_month // 12))

# DRAW GRID

date_grid = date_grid.T
# print(date_grid)
width = int(axis_x // 2)
height = int(days_of_week // 2)
DPI = 96
fig, ax = plt.subplots(figsize=(width-10, height))
plt.xticks(rotation='90')
## DEFAULT COLOR
# sns.heatmap(date_grid, square=True, linewidths=.88, annot=False, xticklabels=False, yticklabels=False, cbar=False)
## COLORMAP COLOR
## Optional cmap: BuGn  Blues
sns.heatmap(date_grid, square=True, linewidths=.88, cmap="Blues", annot=False, xticklabels=False, yticklabels=False,
            cbar=False)
ax.set_title(str(calender[0][0]), fontsize=25.5)
## ADVANCED SETTING
# fig = plt.gcf()
# fig.set_size_inches(width*50 / DPI, height*50 / DPI)
## ZERO FRAME
plt.subplots_adjust(top=0.95, bottom=0, left=0, right=1, hspace=0, wspace=0)
plt.margins(0, 0)
## SHOW
# plt.show()
## SAVE
save_path = os.getenv("APPDATA")
save_path = save_path.replace("AppData\\Roaming", "")
save_path += "Desktop\\"
save_path.replace("\\", '/')
print(save_path)
plt.savefig(save_path + str(calender[0][0]) + '.png', dpi=DPI, pad_inches=0.0)
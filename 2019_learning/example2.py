# -*- coding: UTF-8 -*-
#------------------------第一步，将文件夹下所有的文件读取进来---------------------摄像头编号 摄像日期 摄像时间 笼号  变化点数 帧数 视频时间长度
import pandas as pd
import numpy as np
import os
import time
def deal_with_file(csv):
    file_dir='C:\\Users\\83804\\Desktop\\作业\\TextResult\\'+str(csv)
    r = open(file_dir, mode='r',encoding='ANSI')
    r.readline()
    string = r.readline()  # 读取第二行
    ss = string.split(' ')
    ss = list(filter(None, ss))
    length = len(csv)
    result=None
    if length == 28:
        id = csv[0:4]
        date = csv[5:13]
        time = csv[13:19]
        cage = csv[20:23]
        try:
            change_point = ss[0]
            frame_number = ss[1]
            second_time = ss[2]
            second_time = second_time.strip('\n')
            result = id + ' ' + date + ' ' + time + ' ' + cage + ' ' + change_point + ' ' + frame_number + ' ' + second_time
        except:
            pass

    if length == 23:  # 此时处理无摄像头编号数据
        id = csv[0:4]
        date = csv[5:13]
        time = csv[13:19]
        cage = '1'
        try:
            change_point = ss[0]
            frame_number = ss[1]
            second_time = ss[2]
            second_time = second_time.strip('\n')
            result = id + ' ' + date + ' ' + time + ' ' + cage + ' ' + change_point + ' ' + frame_number + ' ' + second_time
        except:
            pass
    if result!=None:
        if result[0:2]!='ch':
            result=None
    return result

def file_name(file_dir):
    list=[]
    for files in os.walk(file_dir):
        list.append(files)
    return list[0][2]
# for root, dirs, files in os.walk(file_chdir):
#     for file in files:
#         if os.path.splitext(file)[1] == '.txt':
#             filecsv_list.append(file)

#data = pd.DataFrame()
def step_one():
    f=open('学号+姓名.txt',mode='w+',encoding='utf-8')
    f.write('摄像头编号  摄像日期    摄像时间    笼号  变化点数    帧数  视频时间长度')
    f.write('\n')
    for csv in file_name(r'C:\Users\83804\Desktop\作业\TextResult'):
        result=deal_with_file(csv)
        if result!=None:
            f.write(result)
            f.write('\n')
    f.close()
#     data = (pd.read_csv(csv, encoding='utf-8'))
#     data['id']=id
#     data['time']=time
#     date['date']=data
#     date['cage']=cage
#     data.to_csv('学号+姓名.txt', mode='a', index=0)
# # if length == 23:  # 此时处理无摄像头编号数据
# #     id = csv[0:4]
# #     date = csv[5:13]
# #     time = csv[13:19]
# #     Cage = '1'
# #     data = (pd.read_csv(csv, header=0, sep=None, encoding='utf-8'))
# #     data.to_csv('ALL.txt', mode='a', index=0)
#--------------------------------------------------------数据处理的第二步,这个文件的主要目的是把小白鼠的活动变化点数按照小时作为分割来做数据清洗，每天24小时，从00-23把它们分别处理在不同的时间单元内（

def step_two():
    file = '学号+姓名+结果1.txt'
    w = open(file, mode='w+', encoding='utf-8')
    w.write('摄像头编号 摄像日期 摄像时间 笼号 变化点数 帧数 视频时间长度 时段')
    w.write('\n')
    with open('学号+姓名.txt', 'r+', encoding='utf-8') as f:
        f.readline()
        ss = f.readline()
        while ss!= '':
            ss = ss.split(' ')
            if len(ss) == 7:
                date = ss[1]  # 8位数字
                day = int(date[6:8])
                time = ss[2]
                hh = int(time[0:2])
                mm = int(time[2:4])
                if mm < 40:
                    hh = hh
                if mm >= 40:
                    hh = hh + 1
                    if hh == 23:
                        day = day + 1
                        hh = 00
                template = ss[1][0:6] + str(day)
                if len(template) == 7:
                    template = ss[1][0:6] + '0' + str(day)
                video_time = ss[6]
                video_time = video_time.strip('\n')
                write_str = str(ss[0] + ' ' + template + ' ' + ss[2] + ' ' + ss[3] + ' ' + ss[4] + ' ' + ss[5] + ' ' + video_time + ' ' + str(hh))
                w.write(write_str)
                w.write('\n')
            ss = f.readline()
    w.close()

def step_three():
    file='学号 + 姓名 + 统计结果（1）.txt'
    data = pd.read_csv('学号+姓名+结果1.txt',sep=' ',engine='python',encoding='UTF-8')
    f=open(file,mode='w+',encoding='utf-8')
    camera=[]
    for i in data['摄像头编号']:
        if i not in camera:
            camera.append(i)
    for i in camera:
        col = data[data["摄像头编号"]==i]
        f.write(str(i)+' '+str((col['摄像日期'].value_counts()).shape[0]))
        f.write('\n')
    cage_id=[]
    for i in data['笼号']:
        if i not in cage_id:
            cage_id.append(i)
    for i in cage_id:
        col = data[data["笼号"]==i]
        f.write(str(i)+' '+str((col['摄像日期'].value_counts()).shape[0]))
        f.write('\n')
#--------------------------两者结构，方法类似-----------------------------

def step_four():
    data = pd.read_csv('学号+姓名+结果1.txt', sep=' ', engine='python', encoding='UTF-8')  # , header=None不要把第一行作为header，这里需要
    file = '学号 + 姓名 + 统计结果（2）.txt'
    data.sort_values("摄像日期", inplace=True)
    df = data[data['摄像日期'] <= 20180204]
    f = open(file, mode='w+', encoding='utf-8')
    f.write('摄像头编号 笼子编号 时段 变化点数')
    f.write('\n')
    for index, row in df.iterrows():
        print(row["摄像头编号"], row['笼号'], row["时段"], row['变化点数'])
        f.write(str(row["摄像头编号"]) + ' ' + str(row['笼号']) + ' ' + str(row["时段"]) + ' ' + str(row['变化点数']))
        f.write('\n')
    f.close()

def step_five():
    data = pd.read_csv('学号+姓名+结果1.txt', sep=' ', engine='python', encoding='UTF-8')  # , header=None不要把第一行作为header，这里需要
    file = '学号 + 姓名 + 统计结果（3）.txt'
    data.sort_values("摄像日期", inplace=True)
    df = data[data['摄像日期'] <= 20180204]
    f = open(file, mode='w+', encoding='utf-8')
    f.write('摄像头编号 笼子编号 日期段 时段 变化点数')
    f.write('\n')
    for index, row in df.iterrows():
        date_period = None
        if row['摄像日期'] >= 20180116 and row['摄像日期'] <= 20180122:
            date_period = 1
        if row['摄像日期'] >= 20180123 and row['摄像日期'] <= 20180129:
            date_period = 2
        if row['摄像日期'] >= 20180130 and row['摄像日期'] <= 20180204:
            date_period = 3
        if date_period != None:
            f.write(
                str(row["摄像头编号"]) + ' ' + str(row['笼号']) + ' ' + str(date_period) + ' ' + str(row["时段"]) + ' ' + str(
                    row['变化点数']))
            f.write('\n')
    f.close()
if __name__ == '__main__':
    step_one()
    time.sleep(1)
    step_two()
    time.sleep(1)
    step_three()
    time.sleep(1)
    step_four()
    time.sleep(1)
    step_five()



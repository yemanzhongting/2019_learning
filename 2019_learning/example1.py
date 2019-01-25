# -*- coding: UTF-8 -*-
_author_ = ''
_date_ = '2019/1/18 0018 13:56'
path=r'C:\Users\83804\Desktop\作业\TextResult'
import os
import pandas as pd
from dateutil.parser import parse

def file_name(file_dir):
    list=[]
    for files in os.walk(file_dir):
        list.append(files)
        #print(root)  # 当前目录路径
        #print(dirs)  # 当前路径下所有子目录
        #print(files)  # 当前路径下所有非目录子文件
    return list[0][2]#读取文件目录下所有文件存为数组

def get_data(data,filename):
    with open(filename, mode='w+', buffering=-1, encoding='utf-8', errors=None, newline=None, closefd=True, opener=None) as f:
        f.write('摄像头编号  摄像日期    摄像时间    笼号  变化点数    帧数  视频时间长度')
        f.write('\n')
        for i in data:
            if i[0:2]=='ch':
                path_file='C:\\Users\\83804\\Desktop\\作业\\TextResult\\'+str(i)
                length=len(i)
                r = open(path_file, "r")
                if length==28:#此时是处理有摄像头编号的数据
                    id=i[0:4]
                    date=i[5:13]
                    time=i[13:19]
                    cage=i[20:23]

                    r.readline()
                    str1 = r.readline()  # 读取第二行
                    ss = str1.split(' ')
                    ss = list(filter(None, ss))
                    try:
                        change_point = ss[0]
                        frame_number = ss[1]
                        second_time = ss[2]
                    except:
                        print(path_file)
                        # 有报错的跳出
                    data_line = id + ' ' + date + ' ' + time + ' ' + cage + ' ' + change_point + ' ' + frame_number + ' ' + second_time  # 这里用了table键分割
                    f.write(data_line)

                if length==23:#此时处理无摄像头编号数据
                    id = i[0:4]
                    date = i[5:13]
                    time = i[13:19]
                    cage = '1'

                    r.readline()
                    str1 = r.readline()  # 读取第二行
                    ss = str1.split(' ')
                    ss = list(filter(None, ss))
                    try:
                        change_point = ss[0]
                        frame_number = ss[1]
                        second_time = ss[2]
                    except:
                        print(path_file)
                        #有报错的跳出
                    data_line = id + ' ' + date + ' ' + time + ' ' + cage + ' ' + change_point + ' ' + frame_number + ' ' + second_time  # 这里用了table键分割
                    f.write(data_line)
                r.close()
                # 关闭打开的文件


def step_two():
    file='学号+姓名+结果1.txt'
    #data = pd.read_csv('学号.txt',engine='python',encoding='UTF-8')#, header=None不要把第一行作为header，这里需要
    #print(data.head())
    w=open(file,mode='w+',encoding='utf-8')
    w.write('摄像头编号 摄像日期 摄像时间 笼号 变化点数 帧数 视频时间长度 时段')
    w.write('\n')
    with open ('学号.txt','r+', encoding='utf-8') as f:
        f.readline()
        ss=f.readline()
        while ss!='':
            ss=ss.split(' ')
            if len(ss)==7:
                date=ss[1]#8位数字
                day=int(date[6:8])
                #进行要求的日期编辑操作
                time=ss[2]
                hh=int(time[0:2])
                mm=int(time[2:4])
                if mm <40:
                    hh=hh
                if mm>=40:
                    hh=hh+1
                    if hh==23:
                        day=day+1
                        hh=00

                template=ss[1][0:6]+str(day)
                if len(template)==7:
                    template=ss[1][0:6]+'0'+str(day)
                video_time=ss[6]
                video_time=video_time.strip( '\n' )
                write_str=str(ss[0]+' '+template+' '+ss[2]+' '+ss[3]+' '+ss[4]+' '+ss[5]+' '+video_time+' '+str(hh))
                #print(write_str)
                w.write(write_str)
                w.write('\n')
            ss = f.readline()
    w.close()
    # print(data['摄像日期'])
    # print(type(data['摄像日期']))
def step_three():#将其数据存入pandas的dateframe进行操作
    file='学号 + 姓名 + 统计结果（1）.txt'
    data = pd.read_csv('学号+姓名+结果1.txt',sep=' ',engine='python',encoding='UTF-8')#, header=None不要把第一行作为header，这里需要
    #print(type(data))
    rowNum = data.shape[0]  # 不包括表头
    colNum = data.columns.size
    #sorted_df = data.sort_index('摄像日期')
    #print((data['摄像日期']))
    sxt=data.groupby('摄像头编号').sum()
    lzbh=data.groupby('摄像头编号').sum()
    f=open(file,mode='w+',encoding='utf-8')

    l=['ch01','ch02','ch03','ch04']
    for i in l:
        col = data[data["摄像头编号"]==i]
        print((col['摄像日期'].value_counts()).shape[0])
        f.write(str(i)+' '+str((col['摄像日期'].value_counts()).shape[0]))
        f.write('\n')
    cage_id=[]
    for i in data['笼号']:
        if i not in cage_id:
            cage_id.append(i)
    print(cage_id)
    for i in cage_id:
        col = data[data["笼号"]==i]
        print((col['摄像日期'].value_counts()).shape[0])
        f.write(str(i)+' '+str((col['摄像日期'].value_counts()).shape[0]))
        f.write('\n')

def step_two_two():
    data = pd.read_csv('学号+姓名+结果1.txt', sep=' ', engine='python', encoding='UTF-8')  # , header=None不要把第一行作为header，这里需要
    file = '学号 + 姓名 + 统计结果（2）.txt'
    data.sort_values("摄像日期",inplace=True)
    print(data.head())
    print(data[data['摄像日期']>=20180116].head())#and data['摄像日期']<=20180204
    df=data[data['摄像日期']<=20180204]
    print(df[df['摄像日期']<=20180204].tail())#摄像头编号 笼子编号 时段 变化点数
    f = open(file, mode='w+', encoding='utf-8')
    f.write('摄像头编号 笼子编号 时段 变化点数')
    f.write('\n')
    for index, row in df.iterrows():
        print(row["摄像头编号"], row['笼号'],row["时段"],row['变化点数'])
        f.write(str(row["摄像头编号"])+' '+str(row['笼号'])+' '+str(row["时段"])+' '+str(row['变化点数']))
        f.write('\n')
    f.close()
    #index=0
    # for i in data['摄像日期']:
    #     df.iloc[index,1]=str(i)
    #     index=index+1
    # print(data.head())
def step_two_three():#摄像头编号 笼子编号 日期段 时段 变化点数
    data = pd.read_csv('学号+姓名+结果1.txt', sep=' ', engine='python', encoding='UTF-8')  # , header=None不要把第一行作为header，这里需要
    file = '学号 + 姓名 + 统计结果（3）.txt'
    data.sort_values("摄像日期", inplace=True)
    # print(data.head())
    print(data[data['摄像日期'] >= 20180116].head())  # and data['摄像日期']<=20180204
    df = data[data['摄像日期'] <= 20180204]
    print(df[df['摄像日期'] <= 20180204].tail())  # 摄像头编号 笼子编号 时段 变化点数
    f = open(file, mode='w+', encoding='utf-8')
    f.write('摄像头编号 笼子编号 日期段 时段 变化点数')
    f.write('\n')
    for index, row in df.iterrows():
        date_period=None
        if row['摄像日期']>=20180116 and row['摄像日期']<=20180122:
            date_period=1
        if row['摄像日期'] >= 20180123 and row['摄像日期'] <= 20180129:
            date_period=2
        if row['摄像日期'] >= 20180130 and row['摄像日期'] <= 20180204:
            date_period=3
        if date_period!=None:
            f.write(str(row["摄像头编号"]) + ' ' + str(row['笼号']) +' '+ str(date_period)+' '+ str(row["时段"]) + ' ' + str(row['变化点数']))
            f.write('\n')
    f.close()

    #parse(data.iloc[:,1])  # 将数据类型转换为日期类型
    #data = data.set_index('date')  # 将date设置为index
    #print(data.head())
    #col=df2.iloc[:,2] 处理行列
    #col=data
    #col.index =col.iloc[:,1]#进行切片操作
    # 把index处理为datetime格式
    # col.index = pd.to_datetime(col.index, unit='ns')

    #print(sxt)
    #print(data)
if __name__ == '__main__':
    result=file_name(path)
    get_data(result,r'学号.txt')
    step_two()
    step_three()
    step_two_two()
    step_two_three()


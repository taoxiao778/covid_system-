import numpy as np 
import pandas as pd
from datetime import datetime,date,time,timedelta
import time


def query_infomation():
    #查询居民居住信息，通过姓名、身份证号或所在区域查找。
    #居住信息包括：身份证、姓名、性别、出生年月日、所在街道、进入当前居住地日期、离开当前居住地日期
    global people_df
    print("输入1，通过姓名查找")
    print("输入2，通过身份证号码查找")
    print("输入3，通过街道查找")
    flag=False
    res=[]
    choice=int(input("请输入："))
    if choice==1:
        target=input("请输入姓名：")
        for i,row in people_df.iterrows():
            if row['姓名']==target:
                res.append(row)
                # print(row)
                flag=True
    elif choice==2:
        target=int(input("请输入身份证号码："))       
        for i,row in people_df.iterrows():            
            if row['id']==target:
                res.append(row)
                # print(row)
                flag=True

    elif choice==3:
        target=input("请输入街道：")
        for i,row in people_df.iterrows():
            if row['所在街道']==target:
                res.append(row)
                # print(row)
                flag=True
    if flag==False:
        print("没有找到您需要的信息")
    else:
        print(pd.DataFrame(res))


def delete_infomation():
    #删除某条居住信息，根据身份证号，删除该条信息
    global people_df
    flag=False
    target=int(input("输入需要删除的身份证号："))
    people_df=people_df.drop(people_df[people_df['id']==target].index)

    people_df.to_csv('数据库\\疫情防控系统\\people.csv',encoding='utf-8',index=False)


def acid_test_registration():
    #核酸检测登记，录入身份证号、检测时间（到秒）、
    #检测结果、检测样本编号（10位数字）
    global test_df
    csv_data2=pd.read_csv("数据库\\疫情防控系统\\test.csv")
    tmp_df=pd.DataFrame(csv_data2)

    tmp_df['检测时间']=tmp_df['检测时间'].map(lambda x:pd.to_datetime(x))

    test_df=pd.concat([test_df,tmp_df],ignore_index=True)
    print(test_df)

def query_covid():
    #阳性病例查询，按时间范围 and/or 所在街道查询阳性病例数据，
    #返回核酸检测信息和该居民的居住信息，
    #例如 111001111111212112，2022-9-6 19:00，阳性，……，张三，中关村街道，……
    global test_df,people_df
    start=input("输入开始时间：")
    end=input("输入截止时间：")
    # start_time=datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
    # end_time=datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
    start=pd.to_datetime(start)
    end=pd.to_datetime(end)

    is_covid=test_df[test_df['检测结果']=="阳性"]

    covid_in_time=is_covid[(is_covid['检测时间']>=start) & (is_covid['检测时间']<=end)]
    print(covid_in_time)
    covid_people=people_df[(people_df['id'].isin(covid_in_time['身份证号']))&
    (((people_df['进入当前居住地日期']>=start)&(people_df['进入当前居住地日期']<=end))
    |((people_df['离开当前居住地日期']>=start)&(people_df['离开当前居住地日期']<=end))
    |((people_df['进入当前居住地日期']<=start)&(people_df['离开当前居住地日期']>=end)))]
    print(covid_people)

    

def query_close():
    #密接人群查询，输入阳性病例的检测编号，
    #返回在病例检测时间往前7天内，与病例在同一街道居住的人员。
    #注意要排除已离开该街道的人员。
    global people_df,test_df
    num=int(input("输入阳性病例的检测编号："))
    index=0
    for i,row in test_df.iterrows():
        if row['检测样本编号']==num:
            index=i
            break
    target_id=test_df.iloc[i,0]
    target_time=test_df.iloc[i,1]
    target_person=people_df[people_df['id']==target_id]

    end_time=target_time.date()
    start_time=end_time-timedelta(days=7)
    # print(end_time,start_time)
    #7天之内去过的地方
    seven_days_target=target_person[((target_person['进入当前居住地日期']>=start_time)
    &(target_person['进入当前居住地日期']<=end_time))
    |((target_person['离开当前居住地日期']>=start_time)
    &(target_person['离开当前居住地日期']<=end_time))
    |((target_person['进入当前居住地日期']<=start_time)
    &(target_person['离开当前居住地日期']>=end_time))]
    # print(seven_days_target['所在街道'])
    target_place=seven_days_target['所在街道']

    close_people=people_df[(people_df['id']!=target_id)&
    (people_df['所在街道'].isin(target_place))
    &(((people_df['进入当前居住地日期']>=start_time)&(people_df['进入当前居住地日期']<=end_time))
    |((people_df['离开当前居住地日期']>=start_time)&(people_df['离开当前居住地日期']<=end_time))
    |((people_df['进入当前居住地日期']<=start_time)&(people_df['离开当前居住地日期']>=end_time)))]
    print(close_people)







def info():
    print("输入1，查询居民居住信息")
    print("输入2，删除某条居住信息")
    print("输入3，核酸检测登记")
    print("输入4，阳性病例查询")
    print("输入5，密接人群查询")
    print("输入其他值退出")
    print("请输入：")




if __name__=="__main__":
    global people_df,test_df
    csv_data=pd.read_csv("数据库\\疫情防控系统\\people.csv")
    people_df=pd.DataFrame(csv_data)
    people_df['进入当前居住地日期']=people_df['进入当前居住地日期'].map(lambda x:datetime.strptime(x,"%Y-%m-%d").date())
    people_df['离开当前居住地日期']=people_df['离开当前居住地日期'].map(lambda x:datetime.strptime(x,"%Y-%m-%d").date())
    col_name=['身份证号','检测时间','检测结果','检测样本编号']
    test_df=pd.DataFrame(columns=col_name)
    while 1:
        info()
        choice=int(input())
        if choice==1:
            query_infomation()
        elif choice==2:
            delete_infomation()
        elif choice==3:
            acid_test_registration()
        elif choice==4:
            query_covid()
        elif choice==5:
            query_close()
        else:
            break

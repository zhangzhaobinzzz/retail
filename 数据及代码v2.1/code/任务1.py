# -*- coding: utf-8 -*-

import pandas as pd
import os
# 读取数据
os.chdir('F:\产品部\在线实习\数据及代码v2.1')
data1 = pd.read_csv('data1.csv', encoding = 'gbk')
data2 = pd.read_csv('data2.csv', encoding = 'gbk')
# 任务1.1
# ----------data1数据预处理-----------
# data1查看描述性统计
print(data1.describe())
# 查看data1数据类型
print(data1.dtypes)
# 统计空值
print(data1.isnull().sum())
# 查看data1的CardNo有没有重复值
data1_drop=data1.drop_duplicates(['CardNo'])
print('CardNo去重前数据形状:',data1.shape)
print('CardNo去重后数据形状:',data1_drop.shape)

# 查看data1的AccessCardNo有没有重复值
data1_drop=data1.drop_duplicates(['AccessCardNo'])
print('AccessCardNo去重前数据形状:',data1.shape)
print('AccessCardNo去重后数据形状:',data1_drop.shape)

# ----------data2数据预处理-----------
# data2查看描述性统计
data2_des = data2['Money'].describe()
print(data2_des)
# 统计空值
data2_null = data2.isnull().sum()
data2_null = pd.DataFrame(data2_null,columns=['missing_value'])
print(data2_null)
print('data1数据形状',data1.shape)
print('data2数据形状',data2.shape)
# 缺失值处理,筛选不要的列
data2 = data2.drop(['TermSerNo', 'conOperNo'], axis = 1)
data2 = data2.dropna() # 去空值
data2=data2[data2['Type'] =='消费']
# 修改Date列为时间序列
data2['Date']=pd.to_datetime(data2['Date'])
# 查看data2学生消费表的消费时间有没有异常值
data2['hour']=data2.Date.dt.hour  # 提取小时


data2['minute']=data2.Date.dt.minute  # 提取分钟
print('最小时间',data2['hour'].min())
print('最大时间',data2['hour'].max())

# data2 消费时间异常，正常的学校饭堂并不会通宵营业，所以筛选6点以后的数据
data2=data2[data2['hour']>5]


# 任务1.2
# 对学生个人信息表和消费记录表进行关联
data_mer = pd.merge(data1, data2, left_on = 'CardNo', right_on = 'CardNo', how = 'inner')

# 统计合并后数据
data_out = data_mer['Money'].describe().T
data_out = data_mer.isnull().sum(axis=0)
data_out = pd.DataFrame(data_out,columns=['missing_value'])
print(data_out)
print('合并后数据形状',data_mer.shape)
# 保存数据
data_mer.to_csv('tmp/data_mer.csv',index = False,encoding = 'gbk')
data2.to_csv('tmp/data2.csv',index = False,encoding = 'gbk')


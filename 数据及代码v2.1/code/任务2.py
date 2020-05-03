# -*- coding: utf-8 -*-


import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
# 任务2.1
# 筛选食堂的数据
import os
os.chdir('F:\产品部\在线实习\数据及代码v2.1')
data2= pd.read_csv("tmp\data2.csv" ,encoding = 'gbk')
index=['第一食堂','第二食堂','第三食堂','第四食堂','第五食堂']
data = data2.loc[data2['Dept'].isin(index)]
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d %H:%M:%S')
# 处理单个学生消费记录表，合并同一地点同一刷卡时间的就餐记录。
# 实现过程：
# 1、为了实现“前后刷卡”，所以对时间进行排序
# 2、添加一列标签列
# 3、用shift()函数判断，如果前一个就餐地点不等于下一个，那么记为标签为1
# 4、用diff()函数计算前后刷卡时间差
# 5、如果时间差大于10分钟，那么记为标签为1
# 6、用dcumsum()函数对标签列进行累记，记为re_index列
# 7、对re_index进行分组聚和，求一次就餐金额、刷卡时间和，并且进行去重
def deal_data(data):
    data=data.sort_values(by='Date')  # 对时间进行排序
    data['lab']=0
    data.loc[data['Dept']!=data['Dept'].shift(1),'lab']=1
    data['s']=data['Date'].diff()
    # 时间差转化为秒
    data['s']=[s.total_seconds() for s in data['s']]
    # 默认第一次刷卡为一次就餐，赋值大于阈值即可(设置为10分钟=600秒)
    data.loc[data['s']>600,'lab']=1
    data['re_index']=data['lab'].cumsum()
    df1=data.groupby(['re_index']).agg({'Money':sum,'s':sum}).reset_index()
    data_new=pd.merge(data,df1,on='re_index')
    data_new=data_new.drop_duplicates(['re_index'])
    del data_new['s_x'],data_new['re_index'],data_new['Money_x']
    return data_new

# 对所有学生进行分组，处理消费记录
data_new=data.groupby(['CardNo']).apply(deal_data)
# 绘制各食堂就餐人次的占比饼图，分析学生早中晚餐的就餐地点是否有显著差别。
# 画早中晚餐就餐区域饼图
# 提取早中晚时间
data_morning = data_new.loc[(data_new['hour'].apply(lambda x: x in [6, 7, 8, 9,])),  :]
data_noon = data_new.loc[(data_new['hour'].apply(lambda x: x in [11, 12, 13])),  :]
data_dinner = data_new.loc[(data_new['hour'].apply(lambda x: x in [17, 18, 19, 20])),  :]
# 画早中晚餐就餐区域饼图
data_dict1 = pd.DataFrame.from_dict(Counter(data_morning['Dept']), orient = 'index').reset_index()
data_dict2 = pd.DataFrame.from_dict(Counter(data_noon['Dept']), orient = 'index').reset_index()
data_dict3 = pd.DataFrame.from_dict(Counter(data_dinner['Dept']), orient = 'index').reset_index()
data_dict1.columns = ['Dept', 'Count']
data_dict2.columns = ['Dept', 'Count']
data_dict3.columns = ['Dept', 'Count']   
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
p = plt.figure(figsize = (24, 8))  # 将画布设定为正方形，则绘制的饼图是正圆
ax1 = p.add_subplot(1,3,1)
label1 = data_dict1['Dept']  # 定义饼图的标签，标签是列表
values1 = data_dict1['Count']
plt.pie(values1, autopct = '%1.1f%%', labels = label1)  # 绘制饼图
plt.title('早餐就餐地点饼图')  # 绘制标题
plt.legend(loc='upper right')
ax2 = p.add_subplot(1,3,2)
label2 = data_dict2['Dept']  # 定义饼图的标签，标签是列表
values2 = data_dict2['Count']
plt.pie(values2, autopct = '%1.1f%%', labels = label2)  # 绘制饼图
plt.title('午餐就餐地点饼图')  # 绘制标题
plt.legend(loc='upper right')
ax3 = p.add_subplot(1,3,3)
label3 = data_dict3['Dept']  # 定义饼图的标签，标签是列表
values3 = data_dict3['Count']
plt.pie(values3, autopct = '%1.1f%%', labels = label3)  # 绘制饼图
plt.title('晚餐就餐地点饼图')  # 绘制标题
plt.legend(loc='upper right')
plt.show()

# 任务2.2
# 通过食堂刷卡记录，分别绘制工作日和非工作日食堂就餐时间曲线图，分析食堂早中晚餐的就餐峰值。
# 划分工作日和非工作日，0表示工作日，1表示非工作日
data_new['day'] = data_new['Date'].apply(lambda x: x.day) 
#工作日与休息日
data_new['weekday'] = data_new['Date'].apply(lambda x: x.weekday()+1)
isrest = ((data_new['weekday'] == 6) | (data_new['weekday'] == 7))  
data_new['label'] = isrest*1
# 节假日(5、6、7日为清明节放假，28日因五一假期，所以调休后04-28要上班)
holiday = [5, 6, 7]
for i in holiday:
    data_new.loc[data_new['day']==i,'label']=1
data_new.loc[data_new['day']==28,'label']=0
data_weekday = data_new[data_new['label']==0] # 提取工作日数据
data_weekend = data_new[data_new['label']==1] # 提取非工作日数据
# 计算工作日和非工作日每小时食堂就餐频次
data_gb1 = data_weekday['label'].groupby(data_weekday['hour']).count().reset_index()
data_gb2 = data_weekend['label'].groupby(data_weekend['hour']).count().reset_index()
data_gb1['label'] = data_gb1['label']/22
data_gb2['label'] = data_gb2['label']/8

# 画工作日和非工作日食堂就餐时间折线图
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
p = plt.figure(figsize = (18, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
ax1 = p.add_subplot(1,2,1)
plt.plot(data_gb1['hour'], data_gb1['label'])
plt.title('工作日食堂就餐时间曲线图')
ax2 = p.add_subplot(1,2,2)
plt.plot(data_gb2['hour'], data_gb2['label'])
plt.title('非工作日食堂就餐时间曲线图')
plt.show() # 显示图形
data_new.to_csv('tmp/data_new.csv',index = False,encoding = 'gbk')
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn import preprocessing 
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

os.chdir('F:\产品部\在线实习\数据及代码v2.1')
# 任务3.1
data2= pd.read_csv("tmp\data2.csv" ,encoding = 'gbk')
# 总消费次数
tic = len(data2)
# 总消费金额 
price = data2['Money'].sum()
# 总人数 
people = len(data2['CardNo'].unique())
# 本月人均刷卡频次 
aver_tic = tic/people
print('本月人均刷卡频次',aver_tic)
# 人均消费金额 
aver_price = price/people
print('本月人均消费金额',aver_price)
# 为了分析不同专业、不同性别的学生消费，所以读取合并后的数据
data_mer= pd.read_csv('tmp\data_mer.csv', encoding = 'gbk')
#计算不同专业、不同性别人均消费
data_gb1 = data_mer['Money'].groupby(data_mer['Major']).mean().reset_index()
data_gb2 = data_mer['Money'].groupby([data_mer['Sex'], data_mer['Major']]).mean().reset_index()
data_boy = data_gb2[data_gb2['Sex'] == '男']
data_girl = data_gb2[data_gb2['Sex'] == '女']
# 绘制不同专业、不同性别人均消费柱状图
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
p = plt.figure(figsize = (36,12))  # 将画布设定为正方形，则绘制的饼图是正圆
ax1 = p.add_subplot(1,3,1)
plt.bar(data_gb1['Major'], data_gb1['Money'])
plt.title('不同专业人均消费柱状图', size=20)  # 绘制标题
plt.xticks(rotation=90, size=14)
ax2 = p.add_subplot(1,3,2)
plt.bar(data_boy['Major'], data_boy['Money'])
plt.title('男生人均消费柱状图', size=20)  # 绘制标题
plt.xticks(rotation=90, size=14)
ax3 = p.add_subplot(1,3,3)
plt.bar(data_girl['Major'], data_girl['Money'])
plt.title('女生人均消费柱状图', size=20)  # 绘制标题
plt.xticks(rotation=90, size=14)
plt.show()
# 选择三个专业，分析不同专业不同性别学生消费特点，一共有4 2个专业，从经管类、工科、艺术类分别选取一个代表进行研究。 
# 分别选取了18国际金融、18计算机网络、18艺术设计三个专业。
major = ['18国际金融','18计算机网络','18艺术设计']
data_gb3 = data_gb1.loc[data_gb1['Major'].isin(major)]
data_boy1 = data_boy.loc[data_boy['Major'].isin(major)]
data_girl1 = data_girl.loc[data_girl['Major'].isin(major)]
# 绘制三个专业、不同性别人均消费柱状图
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
p = plt.figure(figsize = (12,6))  # 将画布设定为正方形，则绘制的饼图是正圆
ax1 = p.add_subplot(1,3,1)
plt.bar(data_gb3['Major'], data_gb3['Money'])
plt.title('不同专业人均消费柱状图', size=20)  # 绘制标题
plt.xticks(rotation=90, size=14)
ax2 = p.add_subplot(1,3,2)
plt.bar(data_boy1['Major'], data_boy1['Money'])
plt.title('男生人均消费柱状图', size=20)  # 绘制标题
plt.xticks(rotation=90, size=14)
ax3 = p.add_subplot(1,3,3)
plt.bar(data_girl1['Major'], data_girl1['Money'])
plt.title('女生人均消费柱状图', size=20)  # 绘制标题
plt.xticks(rotation=90, size=14)
plt.show()

# 任务3.2
# 根据学生的整体校园消费行为，选择合适的特征，构建聚类模型
#构建特征：1、早餐平均每餐消费额；2、午餐平均每餐消费额；3、晚餐平均每餐消费额
input1 = "tmp/data_new.csv"
data_new = pd.read_csv(input1 ,encoding = 'gbk')
morning_data = data_new.loc[(data_new['hour'].apply(lambda x: x in [6, 7, 8, 9,])),  :]
noon_data = data_new.loc[(data_new['hour'].apply(lambda x: x in [11, 12, 13])),  :]
dinner_data = data_new.loc[(data_new['hour'].apply(lambda x: x in [17, 18, 19, 20])),  :]
morning_data=morning_data[['CardNo','Money_y']].groupby(by='CardNo').mean().reset_index()
noon_data=noon_data[['CardNo','Money_y']].groupby(by='CardNo').mean().reset_index()
dinner_data=dinner_data[['CardNo','Money_y']].groupby(by='CardNo').mean().reset_index()
# 4、月就餐次数
month_count=data_new[['CardNo','Money_y']].groupby(by='CardNo').count().reset_index()
#合并特征
features = pd.merge(morning_data,noon_data,on='CardNo',how='inner')
features = pd.merge(dinner_data,features,on='CardNo',how='inner')
features = pd.merge(month_count,features,on='CardNo',how='inner')
features.columns=['CardNo','月就餐次数','晚餐平均每餐消费额','早餐平均每餐消费额','午餐平均每餐消费额'] # 修改列名

# 标准化处理
data_prp = preprocessing.scale(features.iloc[:,1:])

# 轮廓系数法确定聚类数
silhouettteScore=[]
for i in range(2,8):
    kmeans1=KMeans(n_clusters=i,random_state=123).fit(data_prp )
    score=silhouette_score(data_prp ,kmeans1.labels_)
    silhouettteScore.append(score)
plt.figure(figsize=(6,4))
plt.plot(range(2,8),silhouettteScore,linewidth=1.5,linestyle="-")
plt.show()
# 构建Kmeans模型
kmeans_model = KMeans(n_clusters= 3, max_iter = 100)
kmeans_model.fit(data_prp)
fit_label = kmeans_model.labels_
features['fit_label']=fit_label
center=kmeans_model.cluster_centers_

# 分群雷达图
fig = plt.figure(figsize=(8,8))
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文
ax = fig.add_subplot(111, polar=True)  # polar参数
labels=['月就餐次数','晚餐平均每餐消费额','早餐平均每餐消费额','午餐平均每餐消费额']
angles = np.linspace(0, 2*np.pi,4, endpoint=False)
angles = np.concatenate((angles, [angles[0]])) # 闭合
for i in range(3):
    data= np.concatenate((center[i], [center[i][0]])) # 闭合
    ax.plot(angles, data)
ax.set_thetagrids(angles * 180/np.pi, labels)
plt.legend(("学生分群1","学生分群2","学生分群3"),loc=1) # 图例
ax.set_title("学生分群雷达图") # 绘制标题
ax.grid(True) # 显示网格
plt.show()

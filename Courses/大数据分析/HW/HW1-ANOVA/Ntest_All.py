import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签

data = pd.read_excel('data.xlsx', sheet_name='data')
s = data.iloc[:, [6]]

# 创建自定义图像
fig = plt.figure(figsize=(10, 6))
# 创建子图1
ax1 = fig.add_subplot(2, 1, 1)
# 绘制散点图
ax1.scatter(s.index, s.values)
plt.grid()  # 添加网格

# 创建子图2
ax2 = fig.add_subplot(2, 1, 2)
# 绘制直方图
s.hist(bins=30, alpha=0.5, ax=ax2)
# 绘制密度图
s.plot(kind='kde', secondary_y=True, ax=ax2)  # 使用双坐标轴
plt.grid()  # 添加网格

# 显示自定义图像
plt.show()

# 计算均值
u = s['平均年龄'].mean()
# 计算标准差
std = s['平均年龄'].std()  # 计算标准差
print('scipy.stats.kstest统计检验结果：----------------------------------------------------')
print(stats.kstest(s['平均年龄'], 'norm', (u, std)))
print('scipy.stats.normaltest统计检验结果：----------------------------------------------------')
print(stats.normaltest(s['平均年龄']))
print('scipy.stats.shapiro统计检验结果：----------------------------------------------------')
print(stats.shapiro(s['平均年龄']))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签

data = pd.read_excel('data.xlsx', sheet_name='data').iloc[:, [1, 6]]
s = data.values
classList = []
for i in range(5):
    classList.append(pd.DataFrame([n for index, n in enumerate(s[:, [1]]) if s[:, [0]][index] == i + 1]))

# 创建自定义图像
fig = plt.figure(figsize=(10, 10))
for i in range(5):
    # 创建子图
    ax = fig.add_subplot(5, 1, i + 1)
    # 绘制直方图
    classList[i].hist(bins=30, label='te', alpha=0.5, ax=ax)
    # 绘制密度图
    classList[i].plot(kind='kde', secondary_y=True, ax=ax)  # 使用双坐标轴
    plt.grid()  # 添加网格

# 显示自定义图像
fig.tight_layout(pad=0.4, w_pad=0, h_pad=1)
plt.show()

for i in range(5):
    # 计算均值和标准差
    mean = classList[i][0].mean()
    std = classList[i][0].std()
    print('testing class {}----------------------------------'.format(i + 1))
    print('均值为 {}'.format(mean))
    print('标准差为 {}'.format(std))
    print('scipy.stats.kstest统计检验结果：----------------------------------------------------')
    print(stats.kstest(classList[i][0], 'norm', (mean, std)))
    print('scipy.stats.normaltest统计检验结果：----------------------------------------------------')
    print(stats.normaltest(classList[i][0]))
    print('scipy.stats.shapiro统计检验结果：----------------------------------------------------')
    print(stats.shapiro(classList[i][0]))

print(stats.levene(classList[0].values.reshape(len(classList[0])),
                   classList[1].values.reshape(len(classList[1])),
                   classList[2].values.reshape(len(classList[2])),
                   classList[3].values.reshape(len(classList[3])),
                   classList[4].values.reshape(len(classList[4]))))

F, P = stats.f_oneway(classList[0].values.reshape(len(classList[0])),
                      classList[1].values.reshape(len(classList[1])),
                      classList[2].values.reshape(len(classList[2])),
                      classList[3].values.reshape(len(classList[3])),
                      classList[4].values.reshape(len(classList[4])))
print('F value:', F)
print('P value:', P, '\n')

print(anova_lm(ols('平均年龄~C(群类别)', data).fit()))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签

data = pd.read_excel('data.xlsx', sheet_name='data')


data["群人数"] = data["群人数"].apply(np.log1p)
data["消息数"] = data["消息数"].apply(np.log1p)
data["会话数"] = data["会话数"].apply(np.log1p)

s = data.iloc[:, [1, 2, 3, 10]].values

colList = []
for i in range(3):
    classList = []
    for j in range(5):
        classList.append(pd.DataFrame([n for index, n in enumerate(s[:, [i + 1]]) if s[:, [0]][index] == j + 1]))
    colList.append({'classList': classList})

for col in colList:
    for i in range(5):
        col['classList'][i][0], lambda_ = stats.boxcox(col['classList'][i][0])

# 创建自定义图像
fig = plt.figure(figsize=(10, 10))
for index, col in enumerate([2, 3, 10]):
    col_data = data.iloc[:, [col]]
    # 创建子图
    ax = fig.add_subplot(3, 1, index + 1)
    # 绘制直方图
    col_data.hist(bins=30, label='te', alpha=0.5, ax=ax)
    # 绘制密度图
    col_data.plot(kind='kde', secondary_y=True, ax=ax)  # 使用双坐标轴
    plt.grid()  # 添加网格

# 显示自定义图像
fig.tight_layout(pad=0.4, w_pad=0, h_pad=1)
plt.show()

for index, col in enumerate([2, 3, 10]):
    print('testing col {}----------------------------------'.format(col + 1))
    meanList = []
    stdList = []
    for i in range(5):
        # 计算均值和标准差
        meanList.append(colList[index]['classList'][i][0].mean())
        stdList.append(colList[index]['classList'][i][0].std())
        print('testing class {}----------------------------------'.format(i + 1))
        print('scipy.stats.kstest统计检验结果：----------------------------------------------------')
        print(stats.kstest(colList[index]['classList'][i][0], 'norm', (meanList[i], stdList[i])))
        print('scipy.stats.normaltest统计检验结果：----------------------------------------------------')
        print(stats.normaltest(colList[index]['classList'][i][0]))
        print('scipy.stats.shapiro统计检验结果：----------------------------------------------------')
        print(stats.shapiro(colList[index]['classList'][i][0]))

    print(stats.levene(colList[index]['classList'][0].values.reshape(len(colList[index]['classList'][0])),
                       colList[index]['classList'][1].values.reshape(len(colList[index]['classList'][1])),
                       colList[index]['classList'][2].values.reshape(len(colList[index]['classList'][2])),
                       colList[index]['classList'][3].values.reshape(len(colList[index]['classList'][3])),
                       colList[index]['classList'][4].values.reshape(len(colList[index]['classList'][4]))))

    F, P = stats.f_oneway(colList[index]['classList'][0].values.reshape(len(colList[index]['classList'][0])),
                          colList[index]['classList'][1].values.reshape(len(colList[index]['classList'][1])),
                          colList[index]['classList'][2].values.reshape(len(colList[index]['classList'][2])),
                          colList[index]['classList'][3].values.reshape(len(colList[index]['classList'][3])),
                          colList[index]['classList'][4].values.reshape(len(colList[index]['classList'][4])))
    print('F value:', F)
    print('P value:', P, '\n')

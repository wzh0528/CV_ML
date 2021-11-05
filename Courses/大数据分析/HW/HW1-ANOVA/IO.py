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

data.to_excel('D:\\Desktop\\data.xlsx',sheet_name='data')


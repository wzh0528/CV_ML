# HW1-ANOVA

(1) 

​	样本被随机抽样且相互独立，各总体服从正态分布，每组方差齐次

(2 )

​	H0：不同类别的成员平均年龄是一样的

​	H1：至少一个类别的平均年龄是不同的

(3) 

a）使用python

绘制经验概率密度函数

![image-20211025210036418](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211025210036418.png)

使用scipy的几种正态分布检验方式进行测试

结果如下：

![image-20211103204500532](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103204500532.png)

p-value远远小于0.05，有足够的理由认为总体不符合正态分布

b）使用python

从上到下分别画出五个类别的PDF

![Figure_1](D:\Desktop\Figure_1.png)

使用scipy的几种正态分布检验方式对5个类分别进行测试，结果如下：

![image-20211103204940002](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103204940002.png)

![image-20211103204956362](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103204956362.png)

从各个结果的p-value看来 类别1，2，3 kstest的p-value大于0.05 满足正态性假设

类别4 5 则不满足正态性假设

类中最大的标准差为5.217 最小的标准差为2.553, 从经验出发不满足方差齐次性

使用levene检验方差齐次性，在统计学角度看不具有方差齐次性

```
print(stats.levene(classList[0].values.reshape(len(classList[0])),
                   classList[1].values.reshape(len(classList[1])),
                   classList[2].values.reshape(len(classList[2])),
                   classList[3].values.reshape(len(classList[3])),
                   classList[4].values.reshape(len(classList[4]))))
```

![image-20211026014606127](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211026014606127.png)

c）使用SPSS

使用Q2所答假设进行one-way ANOVA

<img src="C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211026015630528.png" alt="image-20211026015630528" style="zoom:60%;margin-left:0" />

使用python代码得到类似结果

```
F, P = stats.f_oneway(classList[0].values.reshape(len(classList[0])),
                      classList[1].values.reshape(len(classList[1])),
                      classList[2].values.reshape(len(classList[2])),
                      classList[3].values.reshape(len(classList[3])),
                      classList[4].values.reshape(len(classList[4])))
print('F value:', F)
print('P value:', P, '\n')

print(anova_lm(ols('平均年龄~C(群类别)', data).fit()))
```

<img src="C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211102175652127.png" alt="image-20211102175652127" style="zoom:67%;" /> 

根据表格结果p-value远远小于0.05，拒绝假设H0 得到结论：不同群类别的成员平均年龄有明显差别



(4)

选择群人数、消息数和会话数

分别画PDF

![image-20211102173127540](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211102173127540.png)

使用python分别验证三列是否符合问题一假设

群人数：

![image-20211103210717644](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103210717644.png)

![image-20211103210747686](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103210747686.png)

从检验结果看各组别都不满足正态性假设，同时也不具备方差齐次性

群人数不满足单因素ANOVA假设



消息数

![image-20211103210901113](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103210901113.png)

![image-20211103210928146](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103210928146.png)

从检验结果看各组别都不满足正态性假设，同时也不具备方差齐次性

消息数不满足单因素ANOVA假设



会话数：

![image-20211103211032515](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103211032515.png)

![image-20211103211044967](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103211044967.png)

从检验结果看各组别都不满足正态性假设，同时也不具备方差齐次性

会话数不满足单因素ANOVA假设



进行对数转换

```
data["群人数"] = data["群人数"].apply(np.log)
data["消息数"] = data["消息数"].apply(np.log)
data["会话数"] = data["会话数"].apply(np.log)
```

从PDF图看出正态性有所改善

![image-20211103211201366](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103211201366.png)

测试结果如下

![image-20211103211406013](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103211406013.png)

![image-20211103211442116](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103211442116.png)

![image-20211103211457082](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103211457082.png)

![image-20211103211514875](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103211514875.png)

很多组的正态性得到显著改善，但仍存在不满足正态性假设的组别以及方差仍不具备齐次性



(5)

a）

使用正态分布图直观判断正态分布的特质，而不是检验的方法。检验方法比较严格，现实数据满足钟形曲线特征即可

进行数据转换，将数据分布转换为正态分布

- 取对数或开根号等压缩处理
- BOX-COX转换等

使用不需要正态性假设的非参数检验等方法，如kruskal-wallis H检验

不满足方差齐次性时，可使用Welch检验或者Brown-Forsythe检验

b)

对各组使用log变换＋box-cox变换改善正态性后

<img src="C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103232120706.png" alt="image-20211103232120706" style="zoom:67%;" />

原总体的正态性有所改善，但仍不具备明显正态特征

直接进行单因素ANOVA结果为并进行事后LSD检验

群人数：

<img src="C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103232348002.png" alt="image-20211103232348002" style="zoom:87%;" />

![image-20211103234506595](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103234506595.png)

消息数：

![image-20211103232406188](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103232406188.png)

![image-20211103234551804](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103234551804.png)

会话数：

<img src="C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103232421055.png" alt="image-20211103232421055" style="zoom:77%;" />

![image-20211103234632546](C:\Users\10417\AppData\Roaming\Typora\typora-user-images\image-20211103234632546.png)

观察p-value，三列的p-value都极小，从统计的角度可以认为群人数、消息数、会话数在不同的群类别中有显著差异

事后比较得出，两两之间群类别和群人数、消息数以及会话数存在显著关系


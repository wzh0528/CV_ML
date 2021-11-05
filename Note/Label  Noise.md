# Label  Noise

### Taxonomy of label noise

#### *1) **Instance-independent Label Noise***

assume:  corruption process is conditionally *independent* of data features when the true label is given

​	symmetric noise : 变换到其他label的可能性相同

​	asymmetric noise(label-dependent): 变换到其他label的可能性不同

​	pair noise: 只可能变换到一种label



#### *2) **Instance-dependent Label Noise***

assume: corruption probability is assumed to be *dependent* on both the data features and class labels 



### Non-deep Learning approaches

- *Data cleaning* : excluding examples whose labels are likely to be corrupted
- *Surrogate Loss*:  受0-1 loss function的噪声容忍度启发，对LOSS进行替换与改进
- *Probabilistic Method*： label confidence clustering -> weighted training scheme
- *Model-based Method*: 模型改进



### Theoretical Foundation between DNNs and Label noise

#### *Label Transition* 

given an example $x$， the estimation of the noisy label distribution for the example $x$ is expressed by:
$$
p(\tilde{y}=j|x)=\sum_{i=1}^cp(\tilde{y}=j,y=i|x)=\sum_{i=1}^cT_{ij}p(y=i|x) \\
where \quad T_{ij}=p(\tilde{y}=j|y=i,x)
$$

#### *Risk Minimization*

对于噪声数据，设计合适的损失函数 $\mathscr{l}^{\prime}$ 可以得到贝叶斯最佳分类器 $f^*$ , 对应最佳$\mathcal{R}^*=\mathcal{R}_{\mathcal{D}}(f^*)$

那么对于$f=argmin_{f}$

#### *Memorization Effect*



### Deep Learning approaches

#### *Robust architecture*



#### *Robust regularization*



#### *Robust loss function*



#### *Loss adjustment*



#### *Sample selection*





噪声标签 + LT：把并行的噪声标签鉴别转化成串行的来做，在处理少数类的时候，引入之前的先验消息，帮忙排除来自多数类的噪声样本



实验：生成一个长尾噪声标注数据集

跑跑SOTA的结果 ：dividemix  elr

LT方面：泛读文章

noisy label方面：精度最新文章，学习实验组织方法


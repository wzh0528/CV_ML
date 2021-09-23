# Basic Algorithm

<img src="D:\Desktop\CV_ML\img\map.png" style="zoom:80%; margin-left:50px" />



3 tasks: regression, classification and structured learning

## Linear Model

### logistic regression

#### probabilistic generative model

选择不同的distribution作为model，进行参数估计

基于贝叶斯公式，进行分类

#### Analysis Posterior Probability

<img src="D:\Desktop\CV_ML\img\logistic regression.png" style="zoom:80%;margin-left: 20px; " />

#### loss function

the problem of using  **squared cost function**  : non-convex

using  **cross-entropy loss function** √

看作两个两点分布的交叉熵，便于理解

#### Discriminative vs. Generative

Generative的model它有做了某些假设，假设你的data来自于某个概率模型；对data依赖小

Discriminative的model是完全不作任何假设的；data充足时，准确率一般比generative model高



### support vector machine

<img src="D:\Desktop\CV_ML\img\svm.png" style="zoom:80%;" />

SVM是一种二分类模型，基本模型是定义在特征空间上的**间隔最大的线性分类器**



## Neural network

逻辑回归单元堆叠！ deep learning



### back propagation

**Forward pass**：每个neuron的activation function的output，就是它所连接的weight的 $\frac{\partial z}{\partial w}$

**Backward pass**：建一个与原来方向相反的neural network，它的三角形neuron的output就是 $\frac{\partial l}{\partial z}$

把通过forward pass得到的 $\frac{\partial z}{\partial w}$和通过backward pass得到的 $\frac{\partial l}{\partial z}$乘起来就可以得到对的偏微分 $\frac{\partial l}{\partial w}$

<img src="D:\Desktop\CV_ML\img\bp.png" style="zoom:80%; margin-left:200px; "/>



### vanishing gradient problem

network叠很深时，靠近input的参数的梯度较小，靠近output的参数的梯度较大

当lr一定时，靠近output的参数快速收敛，参数loss下降很慢

解决：

采用ReLU（Rectified Linear Unit，整流线性单元函数）

- Fast to compute
- Biological reason
- 无穷多bias不同的sigmoid函数叠加就是ReLU

延申：Leaky ReLU、Parametric ReLU

#### Maxout network

network自动去学习它的activation function



### Batch & Momentum

#### batch size

<img src="D:\Desktop\CV_ML\img\batch.png" style="zoom:85%; margin-left:0px;" />

#### momentum

受**惯性**启发



### Adaptive learning rate

#### adagrad

坡度比较大的时候,learning rate就减小,坡度比较小的时候,learning rate就放大

<img src="D:\Desktop\CV_ML\img\adagrad.png" style="zoom:80%; margin-left:30px" />



#### RMSProp

lr设置为一个固定值 $\eta$ 除掉一个变化的 $\sigma$ ，这个$\sigma$ 等于上一个$\sigma$ 和当前梯度 *g* 的加权方均根

在第一个时间点$\sigma$ 就是第一个算出来的gradient值，$\alpha$ 可以调节

<img src="D:\Desktop\CV_ML\img\RMSProp.png" style="zoom:80%; margin-left:20px" />



#### Adam

RMSProp加上Momentum，就可以得到Adam

#### learning rate scheduling

<img src="D:\Desktop\CV_ML\img\lrscheduling.png" style="zoom:60%; margin-left:20px" />



### Feature Normalization

#### batch normalization

<img src="D:\Desktop\CV_ML\img\BN.png" style="zoom:80%; margin-left:20px" />



### Regularization

使用L2 regularization可以让weight每次都乘上(1- $\eta\lambda$),就叫做**Weight Decay**(权重衰减)

使用L1 regularization可以让weight每次都减去$\eta\lambda$sgn($w$)，使绝对值接近0



### Dropout

**Dropout真正要做的事情，就是要让你在training set上的结果变差，但是在testing set上的结果是变好的**

- testing的时候不做dropout，所有的neuron都要被用到
- 假设在training的时候，dropout rate是p%，从training data中被learn出来的所有weight都要乘上(1-p%)才能被当做testing的weight使用

**如果network很接近linear的话，dropout所得到的performance会比较好，而ReLU和Maxout的network相对来说是比较接近于linear的，所以我们通常会把含有ReLU或Maxout的network与Dropout配合起来使用**






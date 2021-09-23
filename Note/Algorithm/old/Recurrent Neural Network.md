# Recurrent Neural Network

![](D:\Desktop\CV_ML\img\RNN.png)

核心：**memory**

**changing sequence order will change the output**

- Elman network：将hidden layer的输出保存在memory里
- Jordan network:将整个neural network的输出保存在memory里  （BETTER)

loss function为经典的cross entropy，训练采用bp算法进阶版，Backpropagation through time，简称BPTT算法

训练困难：

- 梯度消失(gradient vanishing)，一直在梯度平缓的地方停滞不前
- 梯度爆炸(gradient explode)，梯度的更新步伐迈得太大导致直接飞出有效区间

### long short-term memory（LSTM）

Special Neuron

- 4 inputs ：input data、input gate、forget gate、output gate
- 1 output ：output data

can deal with **gradient vanishing**（not gradient explode）

### Seq2seq 

编码器Encoder把所有的输入序列都编码成一个统一的语义向量Context

然后再由解码器Decoder解码



### Recursive 

相对于RNN，更generative

E.G. <u>tree LSTM</u>


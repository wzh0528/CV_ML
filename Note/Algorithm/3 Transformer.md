# Transformer

### Self-attention

任务：sequence labeling

FC可以和self-attention交替使用，FC处理局部信息，SA处理全局信息

**本质运算过程**如下图所示：

<img src="D:\Desktop\CV_ML\img\self-attention.png" style="zoom:56%; margin-left:20px" />

Q为query，K为key， A为attention score， V是由I提取得到的新vectors

#### multi-head self-attention

多套Q, K, V

#### self-attention plus PE(position encoding)

考虑位置信息，在I上加入PE矩阵

#### self-attention vs. CNN

CNN本质上是self-attention的特例

#### self-attention vs. RNN

RNN: non-parallel   有IO时序信息

self-attention: parallel   无IO时序信息



### Seq2seq

<img src="D:\Desktop\CV_ML\img\seq2seq.png" style="zoom:75%; margin-left:20px" />

#### Encoder

输入一排向量，输出相同长度的另一排向量

##### transformer encoder

<img src="D:\Desktop\CV_ML\img\transformer_encoder.png" style="zoom:90%; margin-left:-40px" />                                     

在self-attention基础上增加了PE, residual和layer norm

#### Decoder

##### autoregressive（AT) 

自回归！循环：decoder的输出作为下一次的输入

transformer ⬇除了中间模块，其余和encoder相同，中间模块所做工作为：cross-attention

<img src="D:\Desktop\CV_ML\img\transformer_decoder.png" style="zoom:80%; margin-left:150px" />

##### non-autoregressive（NAT) 

parallel √   输出长度可控 √

multi-modality ×  

no dependency on output structure × 

no latent variable ×

#### Training

transformer做法: **Teacher forcing: using the ground truth as input**

##### tips

- copy mechanism: 复制输入
- guided attention：人为先验知识控制attention
- beam search：区别于greedy decoding




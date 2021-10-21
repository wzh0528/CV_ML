# 5 BERT

<img src="D:\Desktop\CV_ML\img\self-supervised learning.png" style="zoom:60%;" />

 没有标签，自己创造标签

### BERT

bert是一个transformer的encoder（训练方法masking input与next sentence prediction（做”填空题“））

#### masking input

首先随机盖住一些tokens，方法有两种：

- 换成special token
- 替换成随机的token

#### next sentence prediction 

<img src="D:\Desktop\CV_ML\img\NSP.png" style="zoom:60%; margin-left:20px" />

not helpful (easy task)

sentence order prediction(SOP): more helpful

#### DOWNSTREAM TASKS WITH FINE-TUNE

sequence -> class (sentiment analysis)

sequence -> sequence (POS tagging)

2 sequences -> class (natural language inference)

2 sequences -> 2 classes (extraction-based question answering)

#### Multi-lingual BERT

多种语言进行预训练（104种）

结果：Zero-shot reading comprehension！

###  GPT

GPT更像是decoder，训练方法（predict next token）

#### predict next token

自回归进行token生成

#### DOWNSTREAM TASKS WITH FINE-TUNE

(In-context learning) : 翻译

- “few-shot" learning 
- "one-shot" learning 
- "zero-shot" learning 

<img src="D:\Desktop\CV_ML\img\GPT.png" style="zoom:43%; margin-left:20px" />


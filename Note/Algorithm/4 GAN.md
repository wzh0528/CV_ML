# GAN

### Unconditional generator

<img src="D:\Desktop\CV_ML\img\unconditional generation.png" style="zoom:80%; margin-left:20px" />



#### Training process

**循环以下两步**

- Fix generator G，and update discriminator D  (区别真实图片和generated objects)
- Fix discriminator D，and update generator G  (试着骗过discriminator)



### Conditional generator

application ：text to image

<img src="D:\Desktop\CV_ML\img\conditional generation.png" style="zoom:90%;margin-left:20px" />

#### Training process

区别与unconditional

G和D都要输入x和z，同时loss再设计



### 



### Tips for GAN

#### JS divergence is not suitable

多数情况下，*P~G~* and *P~data~* are not overlapped

JS divergence在完全不重叠的情况下，结果永远是*log2*

#### Wasserstein distance（WGAN)

<img src="D:\Desktop\CV_ML\img\wasserstein distance.png" style="zoom:70%; margin-left:0px" />

​    better than  JS divergence！

1-Lipschitz : D has to be smooth enough（gradient penalty , spectral normalization)

#### difficult to generate text sequences

scratchGAN (暴搜 Hyperparameter,跟一大堆的 Tips)



### Unsupervised conditional generation

<img src="D:\Desktop\CV_ML\img\cycleGAN.png" style="zoom:67%;margin-left:20px" />



## More generative model

### *VAE(variational autoencoder)*

### *FLOW-based Model*



## Evaluation of Generation

### existing problems

diversity

- mode collapse(生成内容单一重复)
- mode dropping(生成内容缺少多样性)

memory

#### Inception score

good quality & large diversity

#### Frechet Inception  Distance(FID)

Frechet distance between two Gaussions(CNN hidden layer output)

smaller is better


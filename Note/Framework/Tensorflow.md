# Tensorflow

### 程序结构

计算图定义+计算图执行

**计算图**是包含节点和边的网络

每个节点可以有零个或多个输入，但只有一个输出；网络中的节点表示对象，边表示运算操作之间流动的张量

### 数据类型

![](D:\Desktop\CV Learning\img\tfdatatype.png)

张量类型

1. 常量 tf.constrant
2. 变量 tf.Variable
3. 占位符 tf.placeholder

### Cheat Sheet

#### device

- tf.ConfigProto(log_device_placement=True) 验证设备
- tf.ConfigProto(allow_soft_placement=True) 自动选择
-  tf.device() 自动选择（CPU表示为'/cpu: 0' GPU表示为'/gpu: i'）
- 利用for循环手动选择多个GPU




























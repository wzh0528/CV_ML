### Network compression

#### Network pruning

network are typically **over-parameterized**

**weight pruning** or **neural pruning** 

#### Knowledge distillation

##### label refinery

1. train model C0, 目标label为GT
2. train model C1, 目标label为C0的输出
3. 一直训练2直到精度不再提升为止

##### deep mutual learning

#### Parameter Quantization

- Using less bits to represent a value
- Weight clustering
- Represent frequent clusters by less bits, represent rare clusters by more bits ( e.g. Huffman encoding)

binary weight

#### Architecture Design

#### Dynamic Computation
#!/bin/bash --login
pssh "mkdir -p ~/multi-nodes"             # 在thumm01-thumm06节点的主目录下创建multi-nodes目录
cd multi-nodes


bytes=`ls -l ../wc_bigdataset.txt | awk '{print $5}'`     # 计算wc_bigdataset.txt的比特数
bytes_per_node=$(($bytes/6+1))              # 将wc_bigdataset.txt划分为6部分，计算每部的比特数
split -C $bytes_per_node ../wc_bigdataset.txt -d part  # 划分wc_dataset.txt为part00-part06

# 将不同的部分分别传至不同的节点
for ((i=0;i<6;i=i+1));do
    scp part0$i thumm0$(($i+1)):~/multi-nodes/part &
done
wait  # 等待节点传输完成

# 让每个节点运行任务，将结果保存在各自的~/multi-nodes/result文件中
pssh "grep '^t' ~/multi-nodes/part > ~/multi-nodes/result"

# 将所有节点的计算结果传至thumm01(当前操作的主机)
pslurp -L ~/multi-nodes/ ~/multi-nodes/result .

# 将所有结果整合成一个文件：t_head_multi_node.txt
rm -rf ~/multi-nodes/t_head_multi_node.txt
for ((i=1; i<=6; i=i+1)); do
    cat ~/multi-nodes/thumm0$i/result >> ~/multi-nodes/t_head_multi_node.txt
done

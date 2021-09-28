# 实验一 Linux集群基础

![sudo](./assets/sudo.png)

## 一、实验目的

没有使用过linux命令行的同学可以通过本文了解常用命令，为之后使用服务器打下良好的基础。**初次使用服务器集群的同学请务必跟着教程配置一遍。**

- 通过对常用命令`cd、ls、cp、mv、rm、mkdir`等文件命令的操作，掌握Linux操作系统中文件命令的用法。

- 了解集群中多主机之间的文件传输的命令。

## 二、实验任务与要求
(1)建立数据集
- 建立两个大数据集，可以是你所感兴趣的领域的内容，一个能支持求均值、求方差、多元线性回归训练和神经网络训练，另一个能支持WordCount任务（比如服务器中的参考数据集`/home/dsjxtjc/wc_dataset.txt`），建议用心准备。
- 可以在本地随机生成数据集，但建议通过网上的公开数据库、开放API等来下载抓取有意义的数据。（比如US Open Database、微博API）
- 生成的数据集不得小于2GB，但不建议超过5GB（一份参考数据集放在服务器`/home/dsjxtjc/wc_dataset.txt`）
- 将获得的数据集上传至集群主机个人目录下。


(2)单机Linux实验
- 使用`ssh`指令登录远程服务器，并设置免密登录。
- 掌握`mkdir、cd、pwd`命令的操作，要求能建立目录、进入与退出目录。
- 掌握`cp、ls、mv、rm`命令的操作，要求能拷贝文件、新建文件、查看文件、文件重命名、删除文件等操作。
- 掌握`vi`或`vim`的使用，要求能新建、编辑、保存一个文本文件。
- 掌握`cat、head、scp、awk、grep`等文本处理命令的使用，对文本数据进行查看、过滤、统计等操作。
- 了解Linux中阻塞与非阻塞的概念，测试两种情况指令执行的情况。

(3)多机协同实验
- 配置集群中多主机的免密登录，掌握使用`scp`在不同主机之间传输文件。
- 尝试在多节点（即多个Linux主机上）上完成你的任务，包括如何将资源分配至各个节点、如何协调各个节点的任务、如何整合多个结果等等。对比在单节点和多节点上任务处理的速度。

## 三、实验步骤

首先，之前没用过Terminal的同学可以下载实验需要用到的软件XShell，下载地址https://www.netsarang.com/en/free-for-home-school/ ，打开之后即可使用ssh的命令远程连接我们的集群。（课下可以跟着[VSCode Remote Development](https://code.visualstudio.com/docs/remote/ssh)配置下，方便做后续的实验二~四）。

#### 任务1. 使用ssh远程登录服务器 （0.5 分）

课程服务器的地址是**10.103.9.11**，使用`ssh xxx@10.103.9.11`命令即可登录服务器，其中**xxx**使用大家的学号代替, 对应的密码也是学号。

```
$ ssh 2019211199@10.103.9.11
2019211199@10.103.9.11's password:
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.12.9-041209-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

2019211199@thumm01:~$
```

#### 任务2. 配置免密登录 （0.5 分）

接下来我们需要配置一下免密登录。任务1中每次登录需要输入密码挺麻烦的, 对此我们可以配置免密登录，原理是将本机的公钥保存在服务器，每次登录时主机和服务器可以通过公钥验证身份，因此不再需要输入密码。下面是免密登录的方法:

##### 2.1. 生成公钥和私钥

使用ssh-keygen在个人机器上生成公钥和私钥，存放的位置一般不需要改。

```
szxie at ubuntu:~$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/dsjxtjc/2019211199/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/dsjxtjc/2019211199/.ssh/id_rsa.
Your public key has been saved in /home/dsjxtjc/2019211199/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:pDlFzmQA+bFtVlcSwH3hqMT9Du/qjs7rMu7eXb9yZls 2019211199@thumm01
The key's randomart image is:
+---[RSA 2048]----+
|    .o..+..oooo. |
|    . .* .o.o+.  |
|     . +=.o.o..  |
|      o=+. . .   |
|      +oS . . .  |
|       .     +   |
|              + E|
|        oo o + =.|
|       ++=B+=.*o+|
+----[SHA256]-----+
```

##### 2.2. 将公钥内容复制到服务器

使用ssh-copy-id将本地的公钥(localhost:\~/.ssh/id_rsa.pub)添加到远程服务器的认证列表(szcluster.mmlab.top:\~/.ssh/authorized_keys)中，这个过程也可以手动拷贝。

```
szxie at ubuntu$ ssh-copy-id -i ~/.ssh/id_rsa.pub 2019211199@thumm01
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/dsjxtjc/2019211199/.ssh/id_rsa.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
2019211199@thumm01's password:

Number of key(s) added:        1

Now try logging into the machine, with:   "ssh '2019211199@thumm01'"
and check to make sure that only the key(s) you wanted were added.
```

之后使用ssh登录服务器就不需要输入密码了~

<div STYLE="page-break-after: always;"></div> 
#### 任务3. 掌握pwd、mkdir、cd命令的操作，要求能建立目录、进入与退出目录 （0.5 分）

查看当前目录

```
2019211199@thumm01:~$ pwd
/home/dsjxtjc/2019211199
```

创建新目录

```
2019211199@thumm01:~$ mkdir dir_name
2019211199@thumm01:~$ ls
dir_name
```

进入新目录

```
2019211199@thumm01:~$ cd dir_name
2019211199@thumm01:~/dir_name$ pwd
/home/dsjxtjc/2019211199/dir_name
```

退出回到上级目录

```
2019211199@thumm01:~/dir_name$ cd ..
2019211199@thumm01:~$ pwd
/home/dsjxtjc/2019211199
```

#### 任务4. 掌握cp、vim、ls、mv、rm命令的操作，要求能拷贝文件、新建文件、查看文件、文件重命名、删除文件等操作 （0.5 分）

使用vim创建一个文件file.txt, **在命令模式下输入i 切换到插入模式**，输入内容‘helloworld’, **按ESC返回命令模式**，输入:wq保存并退出。

```
2019211199@thumm01:~$ vim file.txt
2019211199@thumm01:~$ ls
dir_name  file.txt
```

查看文件内容

```
2019211199@thumm01:~$ cat file.txt
helloworld
```

拷贝文件file.txt, 生成新的文件new_file.txt

```
2019211199@thumm01:~$ cp file.txt new_file.txt
2019211199@thumm01:~$ ls
dir_name  file.txt  new_file.txt
```

<div STYLE="page-break-after: always;"></div> 
给新文件重命名

```
2019211199@thumm01:~$ mv new_file.txt new_file_renamed.txt
2019211199@thumm01:~$ ls
dir_name  file.txt  new_file_renamed.txt
```

删除file.txt

```
2019211199@thumm01:~$ rm file.txt
2019211199@thumm01:~$ ls
dir_name  new_file_renamed.txt
```

查看文件详细信息

```
2019211199@thumm01:~$ ls -l
total 8
drwxr-xr-x 2 2019211199 dsjxtjc 4096 Sep 20 16:02 dir_name
-rw-r--r-- 1 2019211199 dsjxtjc   11 Sep 20 16:12 new_file_renamed.txt
```

#### 任务5. 掌握cat、head、scp、awk、grep等文本处理命令的使用，对文本数据进行查看、过滤、统计等操作 （0.5 分）

首先拷贝数据集wc_dataset.txt到主目录下，wc_dataset是一个包含2683500个单词的大数据集，每个单词占据一行，大概13M大小。

```
2019211199@thumm01:~$ cp /home/dsjxtjc/wc_dataset.txt ./
2019211199@thumm01:~$ ls
dir_name  new_file_renamed.txt	wc_dataset.txt
```

接着使用指令对该数据集进行操作

##### head、tail命令使用

head/tail用于查看文件头部/尾部的内容，默认最多显示十行

```
2019211199@thumm01:~$ head wc_dataset.txt
chapter
i
down
the
rabbit
hole
alice
was
beginning
to
2019211199@thumm01:~$
```

<div STYLE="page-break-after: always;"></div> 
也可以通过添加参数-n来设定显示的行数

```
2019211199@thumm01:~$ head -n 5 wc_dataset.txt
chapter
i
down
the
rabbit
2019211199@thumm01:~$
```

head和tail可以结合，可以查看文件中任意几行的内容。例如我们要查看wc_dataset.txt中6-10行，我们可以这样做

```
2019211199@thumm01:~$ head -n 10 wc_dataset.txt | tail -n 5
hole
alice
was
beginning
to
2019211199@thumm01:~$
```

##### 重定向符'>'的使用

重定向符可以将指令执行的结果重新定向，可以将原本在控制台输出的内容输出到文件。

将wc_dataset.txt中1-5行内容保存为文件wc_1-5.txt, 将6-10行保存为wc_6-10.txt。

```
2019211199@thumm01:~$ head -n 5 wc_dataset.txt > wc_1-5.txt
2019211199@thumm01:~$ head -n 10 wc_dataset.txt | tail -n 5 > wc_6-10.txt
2019211199@thumm01:~$ ls
dir_name  new_file_renamed.txt	wc_1-5.txt  wc_6-10.txt  wc_dataset.txt
```

使用了重定向符，原先执行指令后的结果输出不见了，同时可以看到多了wc_1-5.txt和wc_6-10.txt两个文件，指令的输出结果被保存在了文件中。

##### cat命令使用

查看两文件的内容

```
2019211199@thumm01:~$ cat wc_1-5.txt
chapter
i
down
the
rabbit
2019211199@thumm01:~$ cat wc_6-10.txt
hole
alice
was
beginning
to
```

<div STYLE="page-break-after: always;"></div> 
cat 也可以同时查看多个文件内容, `cat wc_1-5.txt wc_6-10.txt > wc_1-10.txt`相当于合并两文件，内容为1-10行的内容。

```
2019211199@thumm01:~$ cat wc_1-5.txt wc_6-10.txt > wc_1-10.txt
2019211199@thumm01:~$ cat wc_1-10.txt
chapter
i
down
the
rabbit
hole
alice
was
beginning
to
2019211199@thumm01:~$ head -n 10 wc_dataset.txt
chapter
i
down
the
rabbit
hole
alice
was
beginning
to
```

可以看到结果和head -n 10 wc_dataset.txt一致。

- scp命令使用

scp命令用来在不同主机之间传输文件，它使用的协议是SSH协议，两台主机之间若配置好了ssh免密，那么使用scp传输时不需要输入密码。
scp的详细用法可以通过man指令查看, 下面简单介绍下不同主机之间文件的传输。

首先开启两个终端，一个终端连接上thumm01, 另一个连接连接上thumm02(这里开两个终端只是为了方便查看实验的结果，scp并不需要预先登录两台主机)

在thumm01上

```
2019211199@thumm01:~$ ls
dir_name  new_file_renamed.txt	wc_1-10.txt  wc_1-5.txt  wc_6-10.txt  wc_dataset.txt
2019211199@thumm01:~$
```

在thumm02上

```
2019211199@thumm02:~$ ls
2019211199@thumm02:~$
```

将thumm01中的wc_1-10.txt传到thumm02的主目录

<div STYLE="page-break-after: always;"></div> 
在thumm01上

```
2019211199@thumm01:~$ scp wc_1-10.txt thumm02:~/
2019211199@thumm02's password:
wc_1-10.txt                      100%   54     0.1KB/s   00:00
```

在thumm02上多了一个wc_1-10.txt

```
2019211199@thumm02:~$ ls
wc_1-10.txt
```

##### awk命令使用

awk是一种处理文本文件的语言，是一个强大的文本分析工具，它的具体介绍可以看 [Linux awk 命令](https://www.runoob.com/linux/linux-comm-awk.html )，我们仅介绍awk的一些常用的功能。

基本用法
```sh
awk [选项参数] 'script' var=value file(s)
或
awk [选项参数] -f scriptfile var=value file(s)
```

awk指令适合处理格式规整的数据，例如`/etc/passwd`文件，它保存着Linux系统中用户的用户名以及其他信息(不包含密码), 我们可以通过它了解当前主机上的用户信息，例如我将使用`awk`查看服务器用户列表中学号为2019开头的学生的个数。

要处理数据，我们首先要分析一下数据的格式

```
2019211199@thumm01:~$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
......
2019211333:x:1057:502::/home/dsjxtjc/2019211333:/bin/bash
2019211334:x:1058:502::/home/dsjxtjc/2019211334:/bin/bash
```

我们可以看到，数据每一行代表一个用户，开头为用户的用户名，后面为用户信息（具体代表什么我们不管），每个信息使用`:`进行分割。对此，我们可以依据冒号进行分割，然后取每行第一个元素（用户名），使用正则表达式匹配下看用户名是否为2020开头，如果是则输出。

要实现这个功能，我们可以使用下面的指令

```
2019211199@thumm01:~$ awk -F: '$1~"^2020"{print $1}' /etc/passwd
2020211056
2020214153
......
2020211055
```

其中-F:参数表示使用:作为分隔符进行分割，\$1~"^2020"{print \$1}中\$1表示分割后第一个元素（用户名），"\^2020"是一个正则表达式，表示以2020开头，`~`表示匹配，所以\$1\~"^2020"表示分割后第一个元素满足2020开头，那么就执行后面的指令{print \$1}。
所以指令最终会输出所有2020开头的用户名。

<div STYLE="page-break-after: always;"></div> 
使用`wc -l`统计下有多少个这样的学号，即可知道参加本课程的20级同学的数量了。

```
2019211199@thumm01:~$ awk -F: '$1~"^2020"{print $1}' /etc/passwd | wc -l
69
```

可以看到，一共有69名20级同学参加本课程~~

#####  grep命令使用

> grep命令用于查找文件里符合条件的字符串。grep 指令用于查找内容包含指定的范本样式的文件，如果发现某文件的内容符合所指定的范本样式，预设 grep 指令会把含有范本样式的那一列显示出来。若不指定任何文件名称，或是所给予的文件名为-，则 grep 指令会从标准输入设备读取数据。

接下来我们使用grep命令对wc_dataset.txt作分析

1. 显示1000~2000行中所有以"dis"开头的单词（显示前10条）

```
2019211199@thumm01:~$ grep "^dis" wc_dataset.txt |head
disappointment
distance
disagree
distance
distance
distance
distant
dish
dishes
disgust
```

2. 反向过滤，添加参数-v。

查找wc_1-10.txt中以t字母开头的单词：

```
2019211199@thumm01:~$ grep "^t" wc_1-10.txt
the
to
```

接着添加参数-v，过滤掉wc_0-9.txt以t开头的单词。

```
2019211199@thumm01:~$ grep -v "^t" wc_1-10.txt
chapter
i
down
rabbit
hole
alice
was
beginning
```

<div STYLE="page-break-after: always;"></div> 
#### 任务6. 阻塞与非阻塞时间对比 （0.5 分）

在Linux shell脚本中，里面的指令是顺序执行的，但实际上一些之间并没有依赖关系，这些没有相互依赖（或者说数据关联）的指令可以并行地运行而对结果没有影响。为了让同一个脚本中没有相互依赖的指令并行地执行，我们就需要在边写shell脚本时指定这些指令为非阻塞。

让一条指令不阻塞的方法是在指令德最后面添加上'&'。

接下来边写两个脚本，第一个脚本使用阻塞的方法执行，第二个脚本使用非阻塞的方法执行，对比两个脚本的运行时间：

脚本一: shell_blocked.sh

```sh
#!/bin/bash
awk '$1~"^chapter"{}' wc_dataset.txt
awk '$1~"^chapter"{}' wc_dataset.txt
awk '$1~"^chapter"{}' wc_dataset.txt
awk '$1~"^chapter"{}' wc_dataset.txt
awk '$1~"^chapter"{}' wc_dataset.txt
```

脚本二：shell_unblocked.sh

```sh
#!/bin/bash
awk '$1~"^chapter"{}' wc_dataset.txt &
awk '$1~"^chapter"{}' wc_dataset.txt &
awk '$1~"^chapter"{}' wc_dataset.txt &
awk '$1~"^chapter"{}' wc_dataset.txt &
awk '$1~"^chapter"{}' wc_dataset.txt &
wait
```

运行这两个脚本，对比它们运行的时间

```
2019211199@thumm01:~$ vim shell_block.sh
2019211199@thumm01:~$ vim shell_unblock.sh
2019211199@thumm01:~$ time bash ./shell_block.sh

real	0m5.387s
user	0m5.323s
sys	0m0.064s

2019211199@thumm01:~$ time bash ./shell_unblock.sh

real	0m1.142s
user	0m5.521s
sys	0m0.025s
```

运行程序后，可以看到用户时间不变，都是5秒左右，即所耗费的计算资源不变，但是真实时间脚本二是脚本一的五分之一，因此从用户的角度看脚本二运行更快。
（用户时间user time是指程序在多个核上运行时间的和，真实时间real time是现实中程序运行过去了多长时间，真实时间变短原因是每个操作不再阻塞，而是利用多个处理器核心并行计算。）

<div STYLE="page-break-after: always;"></div> 
#### 任务7. 多节点任务处理 （2 分）


为了充分利用集群的运算性能，我们需要将资源分配至各个节点、协调各个节点的任务、整合多个结果等等。接下来我们来控制命令在多个主机上协同运行。

##### 7.1 集群主机之间免密登录配置 （0.5 分）

首先，我们需要在这些节点之间配置免密登录，下面是一个写好的设置集群中主机之间免密登录的脚本，首先创建一个ssh-keys的文件夹

```
2019211199@thumm01:~$ mkdir ssh-keys
2019211199@thumm01:~$ cd ssh-keys
```

创建一个登录脚本auto_autho.sh, 内容如下
```
2019211199@thumm01:~/ssh-keys$ vim auto_autho.sh
```

auto_autho.sh文件的内容:

```sh
#!/bin/bash
echo "" > authorized_keys
for ((i=1; i<=6; i=i+1));do
    mkdir -p thumm0$i
    ssh-keygen -q -t rsa -N "" -f thumm0$i/id_rsa
    cat thumm0$i/id_rsa.pub >> authorized_keys
done
for ((i=1; i<=6; i=i+1));do
    cp authorized_keys thumm0$i/
    ssh thumm0$i "mkdir -p ~/.ssh"
    scp -r thumm0$i/* thumm0$i:~/.ssh/
done
```
这个脚本做的事情是现在thumm01上生成5个节点的公钥和私钥，然后把所有公钥加入到authorized_keys中，然后把各自的公钥私钥以及authorized_keys分发到各个节点。

运行auto_autho.sh, 这里需要输入10次密码。

```
2020214210@thumm01:~/ssh-keys$ bash ./auto_autho.sh
The authenticity of host 'thumm01 (192.168.0.101)' can't be established.
ECDSA key fingerprint is SHA256:rqu0++2Y5npZ0Mm/pW1G5E+ja1rjuUJTOrR/iPCmnI4.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'thumm01,192.168.0.101' (ECDSA) to the list of known hosts.
2020214210@thumm01's password:
2020214210@thumm01's password:
authorized_keys                                                                                                                                                                                                                             100% 2401     2.3KB/s   00:00
id_rsa                                                                                                                                                                                                                                      100% 1679     1.6KB/s   00:00
id_rsa.pub                                                                                                                                                                                                                                  100%  400     0.4KB/s   00:00
2020214210@thumm02's password:
2020214210@thumm02's password:
authorized_keys                                                                                                                                                                                                                             100% 2401     2.3KB/s   00:00
id_rsa                                                                                                                                                                                                                                      100% 1675     1.6KB/s   00:00
id_rsa.pub                                                                                                                                                                                                                                  100%  400     0.4KB/s   00:00
The authenticity of host 'thumm03 (192.168.0.103)' can't be established.
ECDSA key fingerprint is SHA256:TbMcJfwC7cnUzDHkJ9440xMPYt3DRzxvE1fBeEFEgFo.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'thumm03,192.168.0.103' (ECDSA) to the list of known hosts.
2020214210@thumm03's password:
2020214210@thumm03's password:
authorized_keys                                                                                                                                                                                                                             100% 2401     2.3KB/s   00:00
id_rsa                                                                                                                                                                                                                                      100% 1679     1.6KB/s   00:00
id_rsa.pub                                                                                                                                                                                                                                  100%  400     0.4KB/s   00:00
The authenticity of host 'thumm04 (192.168.0.104)' can't be established.
ECDSA key fingerprint is SHA256:HHEICdQxoc3cJUWVPKNWxkviFOm42H1bRVIjrfoIZNA.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'thumm04,192.168.0.104' (ECDSA) to the list of known hosts.
2020214210@thumm04's password:
2020214210@thumm04's password:
authorized_keys                                                                                                                                                                                                                             100% 2401     2.3KB/s   00:00
id_rsa                                                                                                                                                                                                                                      100% 1675     1.6KB/s   00:00
id_rsa.pub                                                                                                                                                                                                                                  100%  400     0.4KB/s   00:00
The authenticity of host 'thumm05 (192.168.0.105)' can't be established.
ECDSA key fingerprint is SHA256:aAkPOkqqXYoEk0LcyqSyNwT7Qu9+5qI5PzahrzPevTA.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'thumm05,192.168.0.105' (ECDSA) to the list of known hosts.
2020214210@thumm05's password:
2020214210@thumm05's password:
authorized_keys                                                                                                                                                                                                                             100% 2401     2.3KB/s   00:00
id_rsa                                                                                                                                                                                                                                      100% 1675     1.6KB/s   00:00
id_rsa.pub                                                                                                                                                                                                                                  100%  400     0.4KB/s   00:00
The authenticity of host 'thumm06 (192.168.0.106)' can't be established.
ECDSA key fingerprint is SHA256:oZOkUf51aloEV9hYXaW2+f99ggDFfKQNkCKq7j6QYxo.
Are you sure you want to continue connecting (yes/no)? yes
yeWarning: Permanently added 'thumm06,192.168.0.106' (ECDSA) to the list of known hosts.
2020214210@thumm06's password:
2020214210@thumm06's password:
authorized_keys                                                                                                                                                                                                                             100% 2401     2.3KB/s   00:00
id_rsa                                                                                                                                                                                                                                      100% 1675     1.6KB/s   00:00
id_rsa.pub
```

之后就可以通过ssh thumm0**X**免密登录到**X**号节点了~

##### 7.2 集群批管理  （0.5 分）

集群中的thumm01上已经配置好了parallel-ssh集群管理工具，方便将文件复制到其他节点。
例如，我们需要查看thumm01-thumm05上的时间是否正确，我们需要在每台主机上运行date指令。使用pssh我们可以轻松实现在多主机上运行命令。

```
2020214210@thumm01:~$ pssh "date"
[1] 23:15:57 [SUCCESS] thumm01
[2] 23:15:57 [SUCCESS] thumm02
[3] 23:15:57 [SUCCESS] thumm05
[4] 23:15:57 [SUCCESS] thumm03
[5] 23:15:57 [SUCCESS] thumm04
[6] 23:15:57 [SUCCESS] thumm06
```

parallel-ssh除了pssh外，还包括了pscp、pnuke、pslurp等指令， 使用这些指令我们控制集群中的节点会更轻松。

<div STYLE="page-break-after: always;"></div> 
##### 7.3 在多主机上并行执行任务  （1 分）

```sh
#!/bin/bash --login
pssh "mkdir -p ~/multi-nodes"             # 在thumm01-thumm06节点的主目录下创建multi-nodes目录
cd multi-nodes


lines=`cat ../wc_dataset.txt | wc -l`     # 计算wc_dataset.txt的行数
lines_per_node=$(($lines/6+1))              # 将wc_dataset.txt划分为6部分，计算每部的行数
split -l $lines_per_node ../wc_dataset.txt -d part  # 划分wc_dataset.txt为part00-part06

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

# 为了保证结果的正确性，接下来在单个节点上对wc_dataset.txt进行操作，并与多节点的结果作对比

# 在单节点上得到以t开头的单词
grep '^t' ~/wc_dataset.txt > ~/multi-nodes/t_head_single_node.txt

# 检查单节点和多节点的结果是否一致
diff ~/multi-nodes/t_head_multi_node.txt ~/multi-nodes/t_head_single_node.txt
```
运行上面的脚本，最后diff指令输出为空则表示单机与多机结果一致。

到这里我们就完成了多机实验了。

### Bonus

#### 任务8. 尝试提出一种可以加快多节点处理速度的方法并验证（1分）

#### 任务9. 不使用pssh，pslurp等命令，运用master-agent的方式在多主机运行一个简单的任务并汇总，对比在单机和多机的结果和运行时间（2分）

<div STYLE="page-break-after: always;"></div> 
## 四、一些常见的问题

### 1. 找不到pssh指令

pssh的指令全称为parallel-ssh，可以通过ssh在多个指定主机上执行相同的命令。为了方便大家使用，这里通过宏定义隐藏了主机列表配置文件（/home/dsjxtjc/hostname）,为了使宏定义生效，当大家在脚本中使用pssh、pscp、pslurp等指令是需要在文件头添加

```sh
#!/bin/bash --login
```

然后给脚本添加运行权限

```sh
chmod +x ./test.sh
```

最后使用`./test.sh`的方式运行。（以`bash ./test.sh`方式运行会报错）

## 五、报告提交要求

请按照以下要求提交实验报告：

1. 将命令和结果**截图**放入报告，实验报告需为pdf 格式（命名为`学号_姓名_实验一.pdf`，例如：`2021200000_张三_实验一.pdf`），连同代码文件一同打包成压缩文件（命名为`学号_姓名_实验一.*`，例如：`2021200000_张三_实验一.zip`），最后上交到网络学堂。压缩文件中文件目录应为：

   ```bash
   .
   ├── 学号_姓名_实验一.pdf # 实验报告
   └── YOUR_CODE_DIR # 你的代码文件夹
       └── ...
   ```

2. 迟交作业一周以内，以50% 比例计分；一周以上不再计分。另一经发现抄袭情况，零分处理。


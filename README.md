# opencps-agent

新版本 智能体版本
### 新版本更新历史
##### 2018-4-12
1. 新增节点状态信息实时上报的功能

##### 2018-4-14
1. 构建矩阵解析程序

##### 2018-4-15
1. 重新设计完成新版的数据库
2. 基于矩阵解析程序构建完整任务处理逻辑程序
3. 完成任务自动循环处理的功能模块
4. 全部输入参数改为从数据库中调用
5. 新建DataCach数据库的控制函数

下一步计划：

1. 设计循环检测传感器数据并发送模块
2. 接收其他模块传递的数据并保存在dataCach数据库中
3. 构建基本控制器模块
4. 构建基于web控制的sanic脚本

### 迭代历史
##### 2018-3-21  

1. 完成智能体单元模块

##### 2018-3-22

1. 添加任务循环监听处理模块
2. 更改一些智能体单元模块bug

##### 2018-3-23

1. 完成控制器基本通信模块

##### 2018-3-25

1. 在docker上测试代码（存在bug未修复）
2. 已知问题：dht11的数据类型比较奇怪，需要进行额外处理，需要相应修改workProcess代码

##### 2018-3-26
1. 完成在Docker上的第一版代码测试（已修复BUG）
2. 搭建了一套完整的本地测试系统（包括dht102和switch104）
3. 搭建同时执行多条任务代码

## 版本说明
该版本由master版本迭代，在稳定运行基础上，添加如下新功能：

1. 添加故障检测功能
2. 添加在线设备检测功能
3. 优化控制接口，暂定`create`,`addtask`,`start`,`stop`,`delete`,`test`功能

注：multi-task多任务分支版本未完全开发完成，该版本为multi-task版本的拓展版本。

## 上一版本说明

智能体虚拟化模块主要有两大功能

1. 监听控制器的配置请求
2. 监听其他传感器的控制请求

### 目前智能体支持的控制命令
|控制命令|说明|范例|
|--------|----|----|
|add|添加一条任务|controller&add&>30;192.168.1.1:3000:off&20|
|clear|清空任务队列|controller&clear|
|period|更新任务执行周期|controller&period&20|

注： 控制器命令目前由`./tests/testListenSer.py`代为执行
 
### 版本目前存在问题
1. 任务队列中只能存在一条任务 (已解决)

### 未来要支持的功能

控制器：

1. 任务队列的异常发现与处理功能

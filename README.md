# AMLSim-Extension

To create complex money laundering networks according to transaction schemes defined in AMLSim(https://github.com/IBM/AMLSim).



- gen_ml_graph.py 交易图生成工具，定义了交易如何前后连接
- gen_ml_mode.py 设计了一系列洗钱交易结构样例
- gen_ml_modes.py 将多个样例组合，形成有多个洗钱结构的网络
- merge_0_and_1.py 之前3个生成的都是异常结构，需要将他们注入到正常交易网络中，形成最终数据集




依赖：
my_networkx
neo4j_plot
my_matplotlib_plot.py
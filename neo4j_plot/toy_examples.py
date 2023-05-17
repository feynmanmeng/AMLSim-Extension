# %% 1. 生成一个 nx.MultiDiGraph 的图
import networkx as nx

G = nx.MultiDiGraph()
G.add_edges_from(
    [(1, 2, {'weight': 0}),
     (1, 2, {'weight': 1}),
     (1, 2, {'weight': 2}),
     (4, 1, {'weight': 0}),
     (2, 3, {'weight': 0}),
     (3, 4, {'weight': 0})]
)

# %% 2. 检查 neo4j_plot 目录下的 db_connection.json文件，修改为自己的 neo4j 服务器信息
'''
{
  "username": "neo4j",
  "password": "feynmanneo4j",
  "database": "neo4j",
  "port": "7695"
}
'''

# %% 3. 导入 G 到 neo4j
from neo4j_plot.auto_loader import nx_to_neo4j, nodes_edges_to_nx

nx_to_neo4j(G)
'''
【已清空】
4it [00:00, 3990.77it/s]
thread: t194 is processing... 0 left
退出主线程
【节点导入】耗时：1.0718624591827393 s
6it [00:00, ?it/s]
thread: t34 is processing... 0 left
退出主线程
【边导入】耗时：1.2519407272338867 s
节点数量：4
边数量：6
总数量：10
'''

# %% 从文件中导入
import os
import pandas
from neo4j_plot.auto_loader import nx_to_neo4j, nodes_edges_to_nx

def view_std_graph_folder(path):
    # path下只有node.csv和edge.csv
    nodes = pandas.read_csv(os.path.join(path, 'nodes.csv'))
    edges = pandas.read_csv(os.path.join(path, 'edges.csv'))
    G = nodes_edges_to_nx(nodes, edges)
    nx_to_neo4j(G)

view_std_graph_folder("data/sar/SML")

# %% end
print("end")

from collections import Counter, defaultdict

import networkx as nx
import numpy

def _explore_g_from_1_node(G, n):
    # 定义一个函数，从一个指定的节点n开始，沿着出边的方向探索G，并记录每个节点被经过的次数
    # 初始化一个字典，用来存储每个节点被经过的次数
    count = {}
    # 对于G中的每个节点，初始值设为0
    for node in G.nodes():
        count[node] = 0

    # 定义一个辅助函数，用来递归地探索后继节点，并更新计数
    def count_pass(node):
        # 将当前节点的计数加1
        # print(node)
        count[node] += 1
        # 对于当前节点的每个后继节点，递归地调用辅助函数
        for successor in G.successors(node):
            count_pass(successor)

    # 从指定的节点n开始，调用辅助函数
    count_pass(n)
    # 返回计数字典
    return count


def cal_freq_passby(G) -> dict:
    '''
    计算图上的每个节点的经过次数
    '''
    Gr = G.reverse()  # 用于回溯计算

    counter = Counter()
    for node in list(Gr.nodes()):
        # 计算所有节点的路过信息，并统计
        counter.update(_explore_g_from_1_node(Gr, node))
    return counter


def find_frontier_nodes(G) -> list:
    '''
    找到 nx.MultiDiGraph 中只有入边，没有出边的节点
    '''
    frontier_nodes = []
    for node in list(G.nodes()):
        if len(list(G.successors(node))) == 0:
            frontier_nodes.append(node)
    return frontier_nodes


def cal_shortest_path_len(G, frontier_nodes) -> dict:
    '''
    统计 nx.MultiDiGraph 中每个节点到 frontier_nodes 的平均路径长度。如果两点之间没有路径则不计算
    '''
    shortest_path_len = {}
    for node in G.nodes():
        lengths = []
        for frontier_node in frontier_nodes:
            if nx.has_path(G, node, frontier_node):
                lengths.append(nx.shortest_path_length(G, node, frontier_node))
        if lengths:
            shortest_path_len[node] = min(lengths)
    return shortest_path_len



# %%
from gen_ml_mode import MLMode

mlm = MLMode()
G = mlm.m_cal_split_point()

H = nx.MultiDiGraph(G)  # 含标记信息

counter = cal_freq_passby(G)
nx.set_node_attributes(H, counter, 'freq_passby')

frontier_nodes = find_frontier_nodes(G)
shortest_path_len = cal_shortest_path_len(G, frontier_nodes)
nx.set_node_attributes(H, shortest_path_len, 'frontier_distance')

# 从 nx.MultiDiGraph 中提取每个节点的'freq_passby'和'frontier_distance'属性值，保存在key为节点id的字典中
freq_passby = nx.get_node_attributes(H, 'freq_passby')
frontier_distance = nx.get_node_attributes(H, 'frontier_distance')

# 将上述两个字典的值作为节点的特征，保存在一个二维数组中
X = numpy.array([list(freq_passby.values()), list(frontier_distance.values())]).T

# 对 X 使用密度聚类
def density_cluster(X, eps=0.1, min_samples=3):
    import hdbscan
    # from sklearn.cluster import DBSCAN, OPTICS
    #
    # db = OPTICS(min_samples=min_samples).fit(X)
    # db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    # labels = db.labels_

    clusterer = hdbscan.HDBSCAN(min_cluster_size=3, gen_min_span_tree=True)
    clusterer.fit(X)
    labels = clusterer.labels_
    return labels

labels = density_cluster(X)

# 使用散点图可视化X，每个节点有label标签，每个标签用不同颜色表示
import matplotlib.pyplot as plt
plt.figure()
plt.scatter(X[:, 0], X[:, 1], c=labels)
plt.show()

node_labels = dict(zip(list(freq_passby.keys()), labels))
# 将聚类结果保存在nx.MultiDiGraph中
nx.set_node_attributes(H, node_labels, 'cluster')

print(X)

# %%
# plt显示
from plt_plot import plot_graph_from_nx

plot_graph_from_nx(G)

# neo4j导入
from neo4j_plot.autoloader import nx_to_neo4j

nx_to_neo4j(G)
nx_to_neo4j(H)

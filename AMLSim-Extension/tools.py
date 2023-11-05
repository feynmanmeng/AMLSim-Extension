import os.path
import random
import pandas
import networkx as nx

from my_networkx.convert import nx_to_nodes_edges


def split_float(amount, n_sep, variation = 0.35)->list:
    '''
    函数功能：将一个金额拆分为n个近似均等的数值列表
    参数：一个浮点型金额，一个整型参数n_sep表示拆分成n个数值，一个浮点型参数variation表示生成数值的波动大小(默认为0.35)
    返回值：该金额被拆分后的结果，返回一个列表
    split_float(54782, 4)
    54782, 4 -> [11001, 6085, 9494, 28202]
    split_float(1578.1, 2)
    '''
    amount_left = amount
    avg_amount = amount / n_sep
    delta = float(avg_amount * variation) # 计算平均值的波动范围
    out = list()
    for i in range(0, n_sep - 1):
        per = avg_amount + random.uniform(-1 * delta, delta) # 生成一个波动范围内的随机数，表示当前分配的金额
        out.append(per)
        amount_left -= per # 将已分配的金额从总金额中减去，得到剩余未分配金额
    out.append(amount_left)
    return out

def split_int(amount, n_sep, variation = 0.35)->list:
    '''
    54782, 4 -> [11001, 6085, 9494, 28202]
    '''
    amount_left = amount
    avg_amount = amount // n_sep
    delta = int(avg_amount * variation)
    out = list()
    for i in range(0, n_sep - 1):
        per = avg_amount + random.randint(-1 * delta, delta)
        out.append(per)
        amount_left -= per
    out.append(amount_left)
    return out

def merge_graph(g1:nx.MultiDiGraph, g2:nx.MultiDiGraph):
    '''
    https://www.codenong.com/32652149/
    '''
    # 相同属性会合并
    # g = nx.compose(g1, g2)
    # g = nx.compose_all([g1, g2])

    # 保留两者的所有值
    g = nx.MultiDiGraph()
    g.add_edges_from(list(g1.edges(data=True)) + list(g2.edges(data=True)))
    g.add_nodes_from(list(g1.nodes(data=True)) + list(g2.nodes(data=True)))
    return g

def nx_to_csv(G:nx.MultiDiGraph, path="./data"):
    ''''
    将 nx.MultiDigraph 保存为 node edge 的 csv 文件
    '''
    if not os.path.exists(path):
        os.makedirs(path)
    nodes, edges = nx_to_nodes_edges(G)
    nodes.to_csv(os.path.join(path, 'nodes.csv'), index=False)
    edges.to_csv(os.path.join(path, 'edges.csv'), index=False)

def nodes_edges_to_csv(nodes, edges, type='tmp'):
    '''
    将临时计算出的 nodes和 edges保存到临时文件夹
    '''
    # 只保留两位小数
    edges['amount'] = edges['amount'].map(lambda x: round(x, 2))

    if type == 'tmp':
        path = r'./data/tmp'
        nodes.to_csv(os.path.join(path, 'nodes.csv'), index=False)
        edges.to_csv(os.path.join(path, 'edges.csv'), index=False)










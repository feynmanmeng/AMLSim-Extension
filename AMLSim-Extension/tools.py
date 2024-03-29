import os.path
import random

import networkx as nx
import pandas
from my_networkx.convert import nx_to_nodes_edges
from networkx_to_neo4j import plot_directed_with_plt
from networkx_to_neo4j.auto_loader import AutoLoader


def split_float(amount, n_sep, variation=0.35) -> list:
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
    delta = float(avg_amount * variation)  # 计算平均值的波动范围
    out = list()
    for i in range(0, n_sep - 1):
        per = avg_amount + random.uniform(-1 * delta, delta)  # 生成一个波动范围内的随机数，表示当前分配的金额
        out.append(per)
        amount_left -= per  # 将已分配的金额从总金额中减去，得到剩余未分配金额
    out.append(amount_left)
    return out


def split_int(amount, n_sep, variation=0.35) -> list:
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


def nx_to_csv(G: nx.MultiDiGraph, path="./data"):
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


def plot_nx(G, use_plt=True, use_neo4j=False):
    if use_plt:
        plot_directed_with_plt(G, layout='kamada_kawai')  # kamada_kawai

    if use_neo4j:
        username = 'neo4j'
        password = 'Feynmanmeng'
        database = 'neo4j'
        port = '7442'
        al = AutoLoader()
        al.connect_to_neo4j(username, password, database, port)
        al.load_to_neo4j(G=G)

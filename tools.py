import os.path
import random
import pandas
import networkx as nx

def split_float(amount, n_sep, variation = 0.35):
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

def split_int(amount, n_sep, variation = 0.35):
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

def nodes_edges_to_nx(nodes, edges):
    ''''
    从 nodes和 edges的 csv文件生成 nx图
    '''
    # 添加 edges
    g = nx.from_pandas_edgelist(df=edges, source='src', target='dst', edge_attr=True, create_using=nx.MultiDiGraph)
    # 补充属性
    nodes_attr = nodes.set_index('id').to_dict('index')
    nx.set_node_attributes(G=g, values=nodes_attr)
    return g

def nx_to_nodes_edges(g:nx.MultiDiGraph):
    nodes = []
    for u, c in g.nodes.data():
        per = list()
        per.extend([u])
        per.extend(list(c.values()))
        nodes.append(per)
    columns = ['id', 'issar']
    nodes = pandas.DataFrame(nodes, columns=columns)

    edges = []
    for u, v, c in g.edges.data():
        per = list()
        per.extend([u, v])
        per.extend(list(c.values()))
        edges.append(per)
    columns = ['src', 'dst', 'name', 'amount', 'step', 'cotype', 'alertid', 'issar']
    edges = pandas.DataFrame(edges, columns=columns)
    return nodes, edges

def nx_to_csv(g:nx.MultiDiGraph, type='tmp'):
    ''''
    将 networkx保存为 csv文件，【仅观察洗钱结构：'tmp'】【与正常数据融合：'sar_normal'】

    节点属性：【'id', 'issar'】
    边属性：【'id', 'src', 'dst', 'name', 'amount', 'step', 'cotype', 'issar'】

    # 只保留两位小数
    edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
    '''
    nodes, edges = nx_to_nodes_edges(g)

    if type == 'tmp':
        # 新生成的 ml_graph没有边 id，需要生成
        # edges = edges.reset_index()
        # edges.rename(columns={'index': 'id'}, inplace=True)
        # 保存
        path = r'./data/tmp'
        nodes.to_csv(os.path.join(path, 'nodes.csv'), index=False)
        edges.to_csv(os.path.join(path, 'edges.csv'), index=False)
    # elif type == 'sar_normal':
    #     # 保存
    #     path = r'./data/sar_normal'
    #     nodes.to_csv(os.path.join(path, 'nodes_sar.csv'), index=False)
    #     edges.to_csv(os.path.join(path, 'edges_sar.csv'), index=False)

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










import os

import networkx as nx
import pandas

from gen_ml_graph.tools import nx_to_nodes_edges, nodes_edges_to_nx, nx_to_csv
from gen_ml_graph.ml_model_generator import MLMode

def merge_gs(gs):
    lst_n = []
    lst_e = []
    for g in gs:
        n, e = nx_to_nodes_edges(g)
        lst_n.append(n)
        lst_e.append(e)
    nodes = pandas.concat(lst_n, axis=0)
    edges = pandas.concat(lst_e, axis=0)

    return nodes, edges


class MLS():
    '''
    生成多组洗钱结构，加入alert_id这个属性
    '''
    def __init__(self):
        self.g = nx.MultiDiGraph()

    def combination_1(self):
        mlm = MLMode()
        g1 = mlm.m5_max(g_name='m5_1', id_start=0, id_end=250, start_step=1, margin_ratio=0.99, alertid=1)
        g2 = mlm.m5_max(g_name='m5_2', id_start=250, id_end=500, start_step=30, margin_ratio=0.99, alertid=2)
        nodes, edges = merge_gs([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.g = nodes_edges_to_nx(nodes, edges)
        return self.g

    def combination_2(self):
        mlm = MLMode()
        g1 = mlm.m6_max(g_name='m6_1', id_start=0, id_end=120, start_step=1, margin_ratio=0.99, alertid=1)
        g2 = mlm.m6_max(g_name='m6_2', id_start=120, id_end=240, start_step=30, margin_ratio=0.99, alertid=2)
        nodes, edges = merge_gs([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.g = nodes_edges_to_nx(nodes, edges)
        return self.g

    def combination_3(self):
        mlm = MLMode()
        g1 = mlm.m7_max(g_name='m7_1', id_start=0, id_end=250, start_step=1, margin_ratio=0.99, alertid=1)
        g2 = mlm.m7_max(g_name='m7_2', id_start=250, id_end=500, start_step=30, margin_ratio=0.99, alertid=2)
        nodes, edges = merge_gs([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.g = nodes_edges_to_nx(nodes, edges)
        return self.g

    def combination_4(self):
        mlm = MLMode()
        g1 = mlm.m8_max(g_name='m8_1', id_start=0, id_end=400, start_step=1, margin_ratio=0.99, alertid=1)
        g2 = mlm.m8_max(g_name='m8_2', id_start=400, id_end=800, start_step=30, margin_ratio=0.99, alertid=2)
        nodes, edges = merge_gs([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.g = nodes_edges_to_nx(nodes, edges)
        return self.g

    def combination_5(self):
        pass

def end():
    pass

if __name__ == '__main__':
    mls = MLS()
    g = mls.combination_4()

    _n, _e = nx_to_nodes_edges(g)

    # 保存到文件，待合并
    nx_to_csv(g)

    # 单独导出洗钱结构，在 neo4j中观察
    # nodes, edges = nx_to_nodes_edges(g)
    # edges = edges.reset_index()
    # edges.rename(columns={'index': 'id'}, inplace=True)
    # path = r'./data/tmp'
    # nodes.to_csv(os.path.join(path, 'nodes.csv'), index=False)
    # edges.to_csv(os.path.join(path, 'edges.csv'), index=False)



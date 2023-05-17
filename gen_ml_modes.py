import os

import networkx as nx
import pandas

from neo4j_plot.AutoLoader import nx_to_neo4j, nx_to_nodes_edges, nodes_edges_to_nx
from plt_plot import plot_graph_from_nx
from tools import nx_to_csv
from gen_ml_mode import MLMode

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
        self.G = nx.MultiDiGraph()

    def combination_SML(self):
        mlm = MLMode()
        g1 = mlm.m_SML(id_start=0, id_end=500, start=1, alertid=1)
        g2 = mlm.m_SML(id_start=500, id_end=1000, start=30, alertid=2)
        nodes, edges = merge_gs([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.G = nodes_edges_to_nx(nodes, edges)
        return self.G

    def combination_CML(self):
        mlm = MLMode()
        g1 = mlm.m_CML(id_start=0, id_end=500, start=1, alertid=1)
        g2 = mlm.m_CML(id_start=500, id_end=1000, start=30, alertid=2)
        nodes, edges = merge_gs([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.G = nodes_edges_to_nx(nodes, edges)
        return self.G

    def combination_TGS(self):
        mlm = MLMode()
        g1 = mlm.m_TGS(id_start=0, id_end=500, start=1, alertid=1)
        g2 = mlm.m_TGS(id_start=500, id_end=1000, start=30, alertid=2)
        nodes, edges = merge_gs([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.G = nodes_edges_to_nx(nodes, edges)
        return self.G

    def combination_TSG(self):
        mlm = MLMode()
        g1 = mlm.m_TSG(id_start=0, id_end=500, start=1, alertid=1)
        g2 = mlm.m_TSG(id_start=500, id_end=1000, start=30, alertid=2)
        nodes, edges = merge_gs([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.G = nodes_edges_to_nx(nodes, edges)
        return self.G

    def combination_5(self):
        pass

def end():
    pass

#%%
if __name__ == '__main__':
    mls = MLS()
    G = mls.combination_TSG()

    nx_to_csv(G, path="./data/sar/TSG/")

    # plt显示
    # plot_graph_from_nx(G)

    # neo4j导入
    nx_to_neo4j(G)



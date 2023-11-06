import networkx as nx
from my_networkx.convert import nodes_edges_to_nx

from examples.aml_graph import gen_SML, gen_CML, gen_TGS, gen_TSG
from tools import nx_to_csv, merge_graphes


class AmlGraphMerged():
    '''
    生成多组洗钱结构，加入alert_id这个属性
    '''

    def __init__(self):
        self.G = nx.MultiDiGraph()

    def combination_SML(self):
        mlg1 = gen_SML(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=10)
        g1 = mlg1.get_graph()
        lei1 = mlg1.get_latest_edge_id() + 1

        mlg2 = gen_SML(id_start=500, id_end=1000, latest_edge_id=lei1, margin_ratio=0.999, alertid=2, start=25)
        g2 = mlg2.get_graph()
        lei2 = mlg2.get_latest_edge_id() + 1

        nodes, edges = merge_graphes([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.G = nodes_edges_to_nx(nodes, edges)
        return self.G

    def combination_CML(self):
        mlg1 = gen_CML(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=2)
        g1 = mlg1.get_graph()
        lei1 = mlg1.get_latest_edge_id() + 1

        mlg2 = gen_CML(id_start=500, id_end=1000, latest_edge_id=lei1, margin_ratio=0.999, alertid=2, start=22)
        g2 = mlg2.get_graph()
        lei2 = mlg2.get_latest_edge_id() + 1

        nodes, edges = merge_graphes([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.G = nodes_edges_to_nx(nodes, edges)
        return self.G

    def combination_TGS(self):
        mlg1 = gen_TGS(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=7)
        g1 = mlg1.get_graph()
        lei1 = mlg1.get_latest_edge_id() + 1

        mlg2 = gen_TGS(id_start=500, id_end=1000, latest_edge_id=lei1, margin_ratio=0.999, alertid=2, start=27)
        g2 = mlg2.get_graph()
        lei2 = mlg2.get_latest_edge_id() + 1

        nodes, edges = merge_graphes([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.G = nodes_edges_to_nx(nodes, edges)
        return self.G

    def combination_TSG(self):
        mlg1 = gen_TSG(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=4)
        g1 = mlg1.get_graph()
        lei1 = mlg1.get_latest_edge_id() + 1

        mlg2 = gen_TSG(id_start=500, id_end=1000, latest_edge_id=lei1, margin_ratio=0.999, alertid=2, start=17)
        g2 = mlg2.get_graph()
        lei2 = mlg2.get_latest_edge_id() + 1

        nodes, edges = merge_graphes([g1, g2])
        edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
        self.G = nodes_edges_to_nx(nodes, edges)
        return self.G

    def combination_5(self):
        pass

import os
import pandas
import networkx as nx

from neo4j_plot.AutoLoader import nodes_edges_to_nx, nx_to_neo4j


class CvtAmlsim():
    def __init__(self):
        pass

    def load_normal_data_amlsim(self, version='v2', name='1k_180'):

        # Output folder of AMLSim
        path = r'xxx'

        addr_nodes = os.path.join(path, r'accounts.csv')
        addr_edges = os.path.join(path, r'tx_log.csv')
        nodes = pandas.read_csv(addr_nodes)
        edges = pandas.read_csv(addr_edges)

        nodes = nodes[['ACCOUNT_ID','IS_SAR']]
        nodes.columns = ['id', 'issar']

        edges = edges[['nameOrig', 'nameDest', 'amount', 'step', 'isSAR']]
        edges.columns = ['src', 'dst', 'amount', 'step', 'issar']
        edges['issar'] = edges['issar'].map(lambda x : False if x == 0 else None)

        path = r'./data/' + name
        if not os.path.exists(path):
            os.makedirs(path)
        nodes.to_csv(os.path.join(path, 'nodes.csv'), index=False)
        edges.to_csv(os.path.join(path, 'edges.csv'), index=False)

def merge_normal_sar(path, nodes_sar, nodes_normal, edges_sar, edges_normal):
    # 合并 nodes
    nodes = pandas.merge(nodes_normal, nodes_sar, on='id', how='left')
    nodes = nodes[['id', 'issar_y']].copy() # 保留issar_y
    nodes.columns = ['id', 'issar']
    nodes['issar'].fillna(False, inplace=True) # 由于issar不完全，所以这里用False填充
    # 合并 edges
    # 1. 为 normal 的边添加 id
    max_edge_id = max(edges_sar['id'])
    normal_ids = [max_edge_id * 10 + x for x in range(len(edges_normal))]
    edges_normal['id'] = normal_ids
    # 2. 逐行合并
    edges = pandas.concat([edges_sar, edges_normal], axis=0)
    edges['coname'].fillna('normal', inplace=True)
    edges['cotype'].fillna('normal', inplace=True)
    edges['alertid'].fillna(0, inplace=True)
    edges['alertid'] = edges['alertid'].astype(int) # concat后变成float，这里变回来
    edges['amount'] = edges['amount'].map(lambda x: round(x, 1))
    # 保存
    if not os.path.exists(path):
        os.makedirs(path)
    nodes.to_csv(os.path.join(path, 'nodes.csv'), index=False)
    edges.to_csv(os.path.join(path, 'edges.csv'), index=False)
    return nodes, edges

def merge_amlsim(path, sar = "SML", normal = "1k_90"):
    # 从AMLSim项目中，导入正常交易，保存到本项目中
    # D:\BaiduSyncdisk\TJ\学术\codes\AML2s\method2\data\normal\1k_90

    # 转换模拟器的直接输出
    # ca = CvtAmlsim()
    # ca.load_normal_data_amlsim(version='v1', name='1k_360')

    # 读取 2组各 2个文件
    path_sar = os.path.join(r"./data/sar/", sar)
    nodes_sar = pandas.read_csv(os.path.join(path_sar, 'nodes.csv'))
    edges_sar = pandas.read_csv(os.path.join(path_sar, 'edges.csv'))

    path_normal = os.path.join(r"./data/v1_normal/", normal)
    nodes_normal = pandas.read_csv(os.path.join(path_normal, 'nodes.csv'))
    edges_normal = pandas.read_csv(os.path.join(path_normal, 'edges.csv'))

    # 合并
    nodes, edges = merge_normal_sar(path, nodes_sar, nodes_normal, edges_sar, edges_normal)

def merge_real():
    # 读取 2组各 2个文件
    path_sar = r'./data/tmp'
    path_normal = r'./data/real/'
    nodes_sar = pandas.read_csv(os.path.join(path_sar, 'nodes.csv'))
    nodes_normal = pandas.read_csv(os.path.join(path_normal, 'nodes.csv'))
    edges_sar = pandas.read_csv(os.path.join(path_sar, 'edges.csv'))
    edges_normal = pandas.read_csv(os.path.join(path_normal, 'edges.csv'))

    # 合并
    nodes, edges = merge_normal_sar(nodes_sar, nodes_normal, edges_sar, edges_normal)

def view_std_graph_folder(path):
    # path下只有node.csv和edge.csv
    nodes = pandas.read_csv(os.path.join(path, 'nodes.csv'))
    edges = pandas.read_csv(os.path.join(path, 'edges.csv'))
    G = nodes_edges_to_nx(nodes, edges)
    nx_to_neo4j(G)

def end():
    pass

if __name__ == '__main__':
    # view_std_graph_folder('data/v1_normal/1k_90')

    #
    merge_amlsim(path="./data/sar_normal/1k_90_SML/",sar = "SML", normal = "1k_90")
    merge_amlsim(path="./data/sar_normal/1k_90_CML/", sar="CML", normal="1k_90")
    merge_amlsim(path="./data/sar_normal/1k_90_TGS/", sar="TGS", normal="1k_90")
    merge_amlsim(path="./data/sar_normal/1k_90_TSG/", sar="TSG", normal="1k_90")

    #
    merge_amlsim(path="./data/sar_normal/10k_90_SML/", sar="SML", normal="10k_90")
    merge_amlsim(path="./data/sar_normal/100k_90_SML/", sar="SML", normal="100k_90")
    merge_amlsim(path="./data/sar_normal/1k_180_SML/", sar="SML", normal="1k_180")
    merge_amlsim(path="./data/sar_normal/1k_360_SML/", sar="SML", normal="1k_360")

    print('end')


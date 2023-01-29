import os
import pandas
import networkx as nx

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

def merge_normal_sar(nodes_sar, nodes_normal, edges_sar, edges_normal):
    # 合并 nodes
    nodes = pandas.merge(nodes_normal, nodes_sar, on='id', how='left')
    nodes = nodes[['id', 'issar_y']].copy()
    nodes.columns = ['id', 'issar']
    nodes['issar'].fillna(False, inplace=True)
    # 合并 edges
    edges = pandas.concat([edges_sar, edges_normal])
    edges['name'].fillna('normal', inplace=True)
    edges['cotype'].fillna('normal', inplace=True)
    edges['alertid'].fillna(0, inplace=True)
    edges['alertid'] = edges['alertid'].astype(int) # concat后变成float，这里变回来
    edges = edges.reset_index() # 这一轮仍会是乱序的，要再reset一次
    edges.drop('index', axis=1, inplace=True) # 删除前一轮
    edges = edges.reset_index() # 正确的编号
    edges.rename(columns={'index':'id'},inplace=True)
    # amount 保留小数
    edges['amount'] = edges['amount'].map(lambda x: round(x, 2))
    # 保存
    path = r'./data/sar_normal'
    nodes.to_csv(os.path.join(path, 'nodes.csv'), index=False)
    edges.to_csv(os.path.join(path, 'edges.csv'), index=False)
    return nodes, edges

def auto_merge_amlsim():
    # 从AMLSim项目中，导入正常交易，保存到本项目中
    ca = CvtAmlsim()
    ca.load_normal_data_amlsim(version='v1', name='1k_360')

    # 读取 2组各 2个文件
    path_sar = r'./data/tmp'
    path_normal = r'./data/1k_360/'
    nodes_sar = pandas.read_csv(os.path.join(path_sar, 'nodes.csv'))
    nodes_normal = pandas.read_csv(os.path.join(path_normal, 'nodes.csv'))
    edges_sar = pandas.read_csv(os.path.join(path_sar, 'edges.csv'))
    edges_normal = pandas.read_csv(os.path.join(path_normal, 'edges.csv'))

    # 合并
    nodes, edges = merge_normal_sar(nodes_sar, nodes_normal, edges_sar, edges_normal)

def auto_merge_real():
    # 读取 2组各 2个文件
    path_sar = r'./data/tmp'
    path_normal = r'./data/real/'
    nodes_sar = pandas.read_csv(os.path.join(path_sar, 'nodes.csv'))
    nodes_normal = pandas.read_csv(os.path.join(path_normal, 'nodes.csv'))
    edges_sar = pandas.read_csv(os.path.join(path_sar, 'edges.csv'))
    edges_normal = pandas.read_csv(os.path.join(path_normal, 'edges.csv'))

    # 合并
    nodes, edges = merge_normal_sar(nodes_sar, nodes_normal, edges_sar, edges_normal)


def end():
    pass

if __name__ == '__main__':
    auto_merge_amlsim()
    # auto_merge_real()
    pass


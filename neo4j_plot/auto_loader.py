import networkx as nx
import pandas

from neo4j_plot.neo4j_clear import autorun_clear
from neo4j_plot.neo4j_nodes import autorun_add_nodes
from neo4j_plot.neo4j_edges import autorun_add_edges

def nx_to_neo4j(G: nx.MultiDiGraph):
    '''
    说明：
        将 G:nx.MultiDiGraph在 Neo4j数据库中可视化
        将需要导入的全量数据拆分为多份，由不同线程去执行

    要求：
        节点：第一列名字叫 id，其他属性
        边：第一列 src，第二列 dst，第三列建议是 id，其他属性

    连接：
        Neo4j <- py2neo
            graph = Graph("neo4j://localhost:7687/", auth=("neo4j", "feynmanneo4j"), name="neo4j")

        Gephi <- neo4j-import
            neo4j://localhost:7687/
            neo4j
            neo4j
            feynmanneo4j

    '''
    # 转化为 nodes edges 的 pandas.DataFrame
    nodes, edges = nx_to_nodes_edges(G)

    # 1. 清空数据库
    autorun_clear()
    # 2. 加载节点
    autorun_add_nodes(data=nodes, n_label='ACCOUNT', r_label='TRANS', n_thread=200, batch_size=50)
    # 3. 加载边
    autorun_add_edges(data=edges, n_label='ACCOUNT', r_label='TRANS', n_thread=200, batch_size=50)

    print(f"节点数量：{G.number_of_nodes()}")
    print(f"边数量：{G.number_of_edges()}")
    print(f"总数量：{G.number_of_nodes() + G.number_of_edges()}")

def nx_to_nodes_edges(G:nx.MultiDiGraph):
    ''''
    将 networkx 图保存为 节点和边文件

    格式要求：
        节点：第一列名字叫 id，其他属性
        边：第一列 src，第二列 dst，第三列建议是 id，其他属性
    '''
    nodes = []
    edges = []

    for u, c in G.nodes.data():
        per = list()
        per.extend([u])
        per.extend(list(c.values()))
        nodes.append(per)
    # 上面已经保存了所有数据，后面就是命名columns，对于node第一列是nodeid，之后是所有属性
    columns = ['id']
    columns.extend(list(c.keys()))
    nodes = pandas.DataFrame(nodes, columns=columns)

    for u, v, c in G.edges.data():
        per = list()
        per.extend([u, v])
        per.extend(list(c.values()))
        edges.append(per)
    # 上面已经保存了所有数据，后面就是命名columns，对于edge前两列是src和dst，之后是所有属性
    columns = ['src', 'dst']
    columns.extend(list(c.keys()))
    edges = pandas.DataFrame(edges, columns=columns)

    return nodes, edges


def nodes_edges_to_nx(nodes, edges, edge_attr=True):
    ''''
    从 nodes和 edges的 csv文件生成 nx图

    格式要求：
        节点：第一列名字叫 id，其他属性
        边：第一列 src，第二列 dst，第三列建议是 id，其他属性

     edge_attr : str or int, iterable, True, or None
        A valid column name (str or int) or iterable of column names that are
        used to retrieve items and add them to the graph as edge attributes.
        If `True`, all of the remaining columns will be added.
        If `None`, no edge attributes are added to the graph.
    '''
    # 添加 edges
    g = nx.from_pandas_edgelist(df=edges, source='src', target='dst', edge_attr=edge_attr, create_using=nx.MultiDiGraph)
    # 补充属性
    nodes_attr = nodes.set_index('id').to_dict('index')
    nx.set_node_attributes(G=g, values=nodes_attr)
    return g

def vSrc_vDst_eWeight_to_nodes_edges(src:list, dst:list, w:list):
    '''
    格式要求：
        节点：第一列名字叫 id，其他属性
        边：第一列 src，第二列 dst，第三列建议是 id，其他属性

    src = [0, 0, 0, 1, 1, 2, 2, 3, 3]
    dst = [1, 2, 3, 2, 4, 3, 4, 2, 4]
    w = [20, 30, 10, 40, 30, 10, 20, 5, 20]
    '''

    unique_nodes = list(set(src+dst))
    nodes = pandas.DataFrame(unique_nodes,columns=['id'])

    lst_edges = [[u,v,i,w] for i,(u,v,w) in enumerate(zip(src, dst, w))]
    edges = pandas.DataFrame(lst_edges, columns=['src','dst','id','weight'])

    return nodes, edges




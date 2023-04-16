import os
import networkx as nx

# from my_networkx.plot import plot_graph_multi


# class NXDemo():
#     def __init__(self):
#         self.g = nx.MultiDiGraph()



def begin():
    g = nx.MultiDiGraph() # 创建图
    g.add_edge(1,2,key=0, w=float(50)) # 添加边，key表示边的id,w这个是自定义的属性
    g.has_edge(1,2)
    ed = g.get_edge_data(1,2,0)['w']
    g.remove_edge(1,2,0)
    g.add_edge(1,2,key=0,w=ed+float(30))

    g = nx.MultiDiGraph()  # 创建图
    g.add_edge(1, 2, key=0, w=50)
    g.add_edge(2, 3, key=0, w=45)
    g.nodes()
    list(g.predecessors(2))

def add_nodes(g:nx.MultiDiGraph):
    '''
    add_nodes_from([(node, node_attribute_dict), (), ()])
    '''
    g.add_node(1, attr = 'a')
    g.nodes[1]['attr'] = 'c'
    g.add_nodes_from([2, 3], attr = 'b')
    g.add_nodes_from([
        (4, {"color": "red"}),
        (5, {"color": "blue"})
    ])

    # 只能添加边，无法保留 h 中的图形
    h = nx.path_graph(5)
    g.add_nodes_from(h) # 节点0
    # g.add_node(h) # 将 h 作为整体看作是 g 中的一个节点

def add_edges(g:nx.MultiDiGraph):

    g.add_edge(1, 2, attr = 'a')
    e1 = (2, 3);    g.add_edge(*e1) # 传入参数
    g.adj[2][3][0]['attr'] = 'b' # MultiDiGraph需要指定边索引
    g.edges[2, 3, 0]['attr'] = 'c'
    g.add_edges_from([
        (3, 4, {'weight': 0.2}),
        (3, 5, {'weight': 0.3})
    ])

def remove_nodes(g:nx.MultiDiGraph):
    g.remove_node(0)
    g.remove_nodes_from([1,2])

def remove_edges(g:nx.MultiDiGraph):
    g.remove_edge(1,2,0) # u, v, key(distinguish multiple edges between a pair of nodes)
    g.remove_edges_from([
        (3,4,0),
        (3,5,0)
    ])

def merge_graph(g1:nx.MultiDiGraph=None, g2:nx.MultiDiGraph=None):
    '''
    https://www.codenong.com/32652149/
    '''
    if g1 == None and g2 == None:
        g1 = nx.MultiDiGraph()
        g1.add_node(1, weight=2)
        g1.add_node(2, weight=3)
        g1.add_edge(1, 2, flux=5)
        g1.add_edge(2, 4)

        g2 = nx.MultiDiGraph()
        g2.add_node(1, weight=4)
        g2.add_edge(1, 2, flux=10)
        g2.add_edge(1, 2, flux2=10)
        g2.add_edge(1, 3)
    # 相同属性会合并
    g = nx.compose(g1, g2)
    # g = nx.compose_all()
    # 保留两者的所有值
    g = nx.MultiDiGraph()
    g.add_edges_from(list(g1.edges(data=True)) + list(g2.edges(data=True)))
    g.add_nodes_from(list(g1.nodes(data=True)) + list(g2.nodes(data=True)))

def multigraph_to_graph(demo=None):
    # 将存在多条边的图转化为单边图，取多条边中的最小值，然后执行最短路径
    MG = nx.MultiGraph()
    MG.add_weighted_edges_from([(1, 2, 0.5), (1, 2, 0.75), (2, 3, 0.5)])
    dict(MG.degree(weight='weight'))
    GG = nx.Graph()
    for n, nbrs in MG.adjacency():
        for nbr, edict in nbrs.items():
            minvalue = min([d['weight'] for d in edict.values()])
            GG.add_edge(n, nbr, weight=minvalue)

    a = nx.shortest_path(GG, 1, 3)
    # nx.dijkstra_path()


def clear_graph(g:nx.MultiDiGraph):
    g.clear()

def show_info(g:nx.MultiDiGraph):

    g.nodes.data() # NodeDataView({1: {'attr': 'c'}, 2: {'attr': 'b'}, 3: {'attr': 'b'}, 4: {'color': 'red'}, 5: {'color': 'blue'}, 0: {}})
    g.edges.data() # OutMultiEdgeDataView([(1, 2, {'attr': 'a'}), (2, 3, {'attr': 'c'}), (3, 4, {'weight': 0.2}), (3, 5, {'weight': 0.3})])

    '''
    27 1 {'tid': 0, 'amount': 255.35329762583973, 'step': 1, 'issar': True, 'txtype': 'fan_in'}
    28 1 {'tid': 0, 'amount': 361.12266825278914, 'step': 2, 'issar': True, 'txtype': 'fan_in'}
    29 1 {'tid': 0, 'amount': 260.76174920184474, 'step': 6, 'issar': True, 'txtype': 'fan_in'}
    30 1 {'tid': 0, 'amount': 239.83517782058425, 'step': 5, 'issar': True, 'txtype': 'fan_in'}
    '''
    for u,v,c in a.edges.data():
        print(u,v,c)

    n_nodes = g.number_of_nodes()
    n_edges = g.number_of_edges()

    succ = list(g.successors(2))
    pred = list(g.predecessors(2))
    g.neighbors()

    # 创建图的视图（只读）：G.nodes、G.edges、G.adj 和 G.degree
    # 类似于 dict，因为您可以查找节点，通过视图和边缘数据属性并使用数据属性进行迭代，使用方法.items()、.data()
    g.adj[1]  # 返回 node 1 的所有邻居信息
    g.adj[3][4][0]  # {'weight': 0.2} 最后那个0 表示的是第几条平行边，应该是之前自动分配的
    g.nodes  # 所有节点编号 NodeView((1, 2, 3, 4, 5, 0))
    g.edges  # 所有边编号 OutMultiEdgeView([(1, 2, 0), (2, 3, 0), (3, 4, 0), (3, 5, 0)])
    g.degree  # 每个节点的度 DiMultiDegreeView({1: 1, 2: 2, 3: 3, 4: 1, 5: 1, 0: 0})







if __name__ == '__main__':
    pass
    # os.chdir(r'C:\Users\feynman\OneDrive\PAN\PythonLib\my_tools\my_networkx')

    # nxg = NXDemo()




    # add_nodes(g)
    # add_edges(g)
    #
    #
    #
    # plot_graph_multi(g)

    # H = nx.path_graph(10)
    # g.add_nodes_from(H)


import networkx as nx
from graph_tools.plot import plot_graph_from_nx
from gen_ml_graph.ml_model_generator import MLMode

def 基本():

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

    # 创建图的视图（只读）：G.nodes、G.edges、G.adj 和 G.degree
    # 类似于 dict，因为您可以查找节点，通过视图和边缘数据属性并使用数据属性进行迭代，使用方法.items()、.data()
    g.adj[1]  # 返回 node 1 的所有邻居信息
    g.adj[3][4][0]  # {'weight': 0.2} 最后那个0 表示的是第几条平行边，应该是之前自动分配的
    g.nodes  # 所有节点编号 NodeView((1, 2, 3, 4, 5, 0))
    g.edges  # 所有边编号 OutMultiEdgeView([(1, 2, 0), (2, 3, 0), (3, 4, 0), (3, 5, 0)])
    g.degree  # 每个节点的度 DiMultiDegreeView({1: 1, 2: 2, 3: 3, 4: 1, 5: 1, 0: 0})

    # 输出的是字典 # in_degree() out_degree()
    g.degree()
    print("0节点度：", g.degree()[0])

    # 查询邻居
    print(g[0])
    print(list(g.neighbors(0)))
    print("节点0和节点32的共同邻居：",list(nx.common_neighbors(g,0,32)))

def 遍历():
    # 图搜索
    print("dfs 搜索节点对:")
    a = nx.dfs_edges(g, source=0, depth_limit=1) # 搜索 0 周围深度为 1 的节点对
    for x in a: print(x)

    print("dfs 可视化路径:")
    a = nx.dfs_tree(g, source=0, depth_limit=1)
    plot_graph_from_nx(a)

    # print("dfs 前驱")
    # a = nx.dfs_predecessors(g, source=0, depth_limit=1)
    # for k,v in a.items(): print(k,v)
    #
    # print("dfs 后继")
    # a = nx.dfs_successors(g, source=0, depth_limit=1)
    # for k,v in a.items(): print(k,v)

    print("先序遍历:", list(nx.dfs_preorder_nodes(g, 0)))
    print("后序遍历:", list(nx.dfs_postorder_nodes(g, 0)))

    print("bfs 搜索节点对:")
    a = nx.bfs_edges(g, source=0, depth_limit=1)
    for x in a: print(x)

    print("bfs 可视化路径:")
    a = nx.bfs_tree(g, source=0, depth_limit=1)
    plot_graph_from_nx(a)

def 路径():
    # 是否有路径
    a = nx.has_path(g, 0, 16)
    nx.has_path(g, 231, 178) # True
    nx.has_path(g, 178, 231) # False

    # 两点之间所有路径
    paths = nx.all_simple_paths(g, source=16, target=26, cutoff=5)  # 没有重复节点的路径
    paths = nx.all_simple_paths(g, source=231, target=178, cutoff=5)
    print(next(paths))  # 一串节点编号

    # 最短路径
    print("图所有节点到其他节点的最短路径")
    paths = nx.shortest_path(g, weight=None, method="dijkstra")

    print("两点间（所有）的最短路径")
    path = nx.shortest_path(g, source=16, target=0, weight=None, method="dijkstra")
    paths = nx.all_shortest_paths(g, source=16, target=0, weight=None, method="dijkstra")
    print(next(paths))

    # nx.shortest_simple_paths
    # nx.shortest_path_length

def 子图():

    a = nx.subgraph(g, [2,7,8,13,18,33]) # subgraph
    a = nx.induced_subgraph(g, [2,7,8,13,18,33]) # subgraph view  a = a.copy()  a = nx.Graph(a)
    a = nx.edge_subgraph(g,[(7,13),(7,3),(3,13),(13,2)]) # subgraph view

if __name__ == "__main__":

    # g = nx.karate_club_graph()  # 生成空手道图
    # plot_graph_from_nx(g)  # 画图

    mlm = MLMode()
    mlm.m5()
    g = mlm.get_graph('m5')
    plot_graph_from_nx(g)










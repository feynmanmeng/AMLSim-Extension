import numpy
import matplotlib.pyplot as plt
import networkx as nx
import pandas

...
'''
# 从Pandas.DataFrame中导入
# https://www.osgeo.cn/networkx/reference/generated/networkx.convert_matrix.from_pandas_edgelist.html
G = nx.convert_matrix.from_pandas_edgelist(sub_df_edge, 'src', 'dst', ['timestamp','amount','issar'])
# 将networkx图转为DataFrame，以边的形式保存
df_edge_kcore = nx.convert_matrix.to_pandas_edgelist(G, 'src', 'dst')

4种类型：
| Networkx Class | Type       | Self-loops allowed | Parallel edges allowed |
| :------------- | :--------- | :----------------- | :--------------------- |
| Graph          | undirected | Yes                | No                     |
| DiGraph        | directed   | Yes                | No                     |
| MultiGraph     | undirected | Yes                | Yes                    |
| MultiDiGraph   | directed   | Yes                | Yes                    |


Layout:
    circular_layout：节点在一个圆环上均匀分布
    random_layout：节点随机分布
    shell_layout：节点在同心圆上分布
    spring_layout： 用Fruchterman-Reingold算法排列节点(多中心放射状)
    spectral_layout：根据图的拉普拉斯特征向量排列节
'''



def plot_graph_from_df(df_edge, directed=False):
    ...
    '''
    绘制无向图，允许自环，允许平行边，无属性
    networkx.classes.multigraph.MultiGraph
    绘制有向图，允许自环，允许平行边，无属性
    networkx.classes.multigraph.MultiDiGraph
    '''
    # df_edge = pandas.DataFrame([(1, 0), (0, 2), (2, 1), (1, 4), (4, 6), (5, 6), (5, 3)])
    col_name = df_edge.columns.values.tolist()
    if 'src' in col_name:
        df = df_edge[['src','dst']]
    else:
        df = df_edge.iloc[:,:2]
        df.columns = ['src','dst']

    if directed == False:
        # 法1 直接生成图
        G = nx.convert_matrix.from_pandas_edgelist(df,'src','dst',create_using=nx.MultiGraph)
        # 法2 先成图后添加
        # G = nx.MultiGraph()
        # G.add_edges_from(numpy.array(df))
    elif directed == True:
        G = nx.convert_matrix.from_pandas_edgelist(df,'src','dst',create_using=nx.MultiDiGraph)
    else:
        print("wrong operator")

    # 设置布局
    pos = nx.spring_layout(G)

    # 绘图
    plt.figure()
    # plt.rcParams['font.serif'] = ['Times New Roman']  # 用来正常显示中文标签
    nx.draw(G, pos=pos,
            # cmap=plt.get_cmap('jet'),
            # node_size=25,
            with_labels=True,
            font_weight='bold',
            font_color='white')
    plt.show()

def plot_graph_from_nx(g):
    # 设置布局
    # pos = nx.spectral_layout(g)
    pos = nx.spring_layout(g)
    # pos = nx.circular_layout(g)
    # 绘图
    plt.figure(dpi=300, figsize=(10,8))
    # plt.rcParams['font.serif'] = ['Times New Roman']  # 用来正常显示中文标签
    nx.draw(g, pos=pos,
            # cmap=plt.get_cmap('jet'),
            node_size=150,
            font_size=6,
            with_labels=True,
            font_weight='bold',
            font_color='red')
    plt.show()


def plot_graph_multi(g):
    # 箭头指向有问题
    plt.figure()
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, node_color='black', node_size=100, alpha=1)
    ax = plt.gca()
    for e in g.edges:
        ax.annotate("",
                    xy=pos[e[0]], xycoords='data',
                    xytext=pos[e[1]], textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="0.5",
                                    shrinkA=5, shrinkB=5,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=rrr".replace('rrr', str(0.3 * e[2])
                                                                           ),
                                    ),
                    )
    plt.axis('off')
    plt.show()


def draw(g:nx.MultiDiGraph):
    '''
    Layout:
        circular_layout：节点在一个圆环上均匀分布
        random_layout：节点随机分布
        shell_layout：节点在同心圆上分布
        spring_layout： 用Fruchterman-Reingold算法排列节点(多中心放射状)
        spectral_layout：根据图的拉普拉斯特征向量排列节

    '''
    plt.figure(dpi=300, figsize=(10,8))
    # plt.rcParams['font.serif'] = ['Times New Roman']  # 用来正常显示中文标签
    # pos = nx.spectral_layout(g)
    pos = nx.spring_layout(g)
    # pos = nx.circular_layout(g)

    nx.draw_networkx_nodes(g,
                           pos,
                           cmap=plt.get_cmap('jet'),  # https://blog.csdn.net/lly1122334/article/details/88535217
                           node_size=60,  # 600
                           node_shape='o',  # 节点的形状（默认是圆形，用字符串'o'标识）
                           alpha=0.1,
                           )  # 绘制节点
    # labels = g.
    nx.draw_networkx_labels(g,
                            pos,
                            # labels = labels,
                            font_size=4, #8
                            )  # 节点label

    nx.draw_networkx_edges(g,
                           pos,
                           # edgelist=x,
                           edge_color='r',  # r
                           width = 0.5,# weights,
                           arrows=True
                           )  # 绘制边，带箭头

    edge_labels = dict()
    for u, v, c in g.edges.data():
        edge_labels[(u, v)] = round(c['amount'], 1)
        # edge_labels[(u, v)] = c['step']
    nx.draw_networkx_edge_labels(g,
                                 pos,
                                 edge_labels=edge_labels,
                                 font_size=4, #6
                                 alpha=1
                                 ) # 绘制图中边的权重

    # 去掉边框
    plt.axis('off')
    # plt.tight_layout()
    plt.show()

def end():
    pass

if __name__ == "__main__":
    plot_graph_from_nx(g)
    # plot_graph_multi(g)
    # g = nx.MultiDiGraph()
    # draw(g)







from networkx_to_neo4j import plot_directed_with_plt
from networkx_to_neo4j.auto_loader import AutoLoader

from gen_ml_graph import MLGraph
from tools import plot_nx


def test_graph_0():
    pass
    # NCNID = 100
    # CNID = [id_end - NCNID + x for x in range(1, NCNID)]  # customized node id，自动分配占前面，手动分配占后100个
    #
    # g_name = 'mx' # 标准生成模板
    # mlg = MLGraph(id_start=id_start, id_end=id_end, margin_ratio=0.999, alertid=alertid) # 500开始可供自定义使用
    # # mlg.shuffle_ids() # 由于存在自定义节点id，就不打散了
    # mlg.add_n(coname='', n=, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    # mlg.add_1_to_1(coname='', lname='', period=1, target_id=-1)
    # mlg.add_n_to_1(coname='', lname='', period=1, target_id=-1)
    # mlg.add_1_to_n(coname='', lname='', n=, period=1, target_ids=[])
    # mlg.add_n_to_n(coname='', lname='', n=, period=1, target_ids=[])
    # mlg.add_n_to_n_prob(coname='', lname='', n=, period=1, prob=0.5, target_ids=[])
    # mlg.split_components(lname='', n_accounts=[], conames=[])
    # mlg.merge_components(coname='', lnames=[])
    # mlg.cvt_edge_to_edges()
    # g = mlg.get_graph()


def test_graph_1():
    '''
    说明：
        多个账户向一个节点汇款，这个节点再发散金额到其他账户
    '''
    mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
    # mlg.shuffle_ids()
    mlg.add_n(coname='c1_1', n=30, min_amount=200, max_amount=400, start=0, period=7, target_ids=[])
    mlg.add_1_to_1(coname='c1_2', lname='c1_1', period=1, target_id=-1)
    mlg.add_1_to_n(coname='c1_3', lname='c1_2', n=5, period=7, target_ids=[])
    mlg.cvt_edge_to_edges()
    G = mlg.get_graph()

    plot_nx(G, use_plt=True, use_neo4j=False)

def test_graph_2():
    '''
    说明：
        两路平行传递资金链
    '''
    mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
    # mlg.shuffle_ids()
    mlg.add_n(coname='c1_1', n=30, min_amount=200, max_amount=400, start=0, period=7, target_ids=[])
    mlg.add_n_to_n(coname='c1_2', lname='c1_1', n=2, period=2, target_ids=[])
    mlg.split_components(lname='c1_2', n_accounts=[1, 1], conames=['c1_s1', 'c1_s2'])
    mlg.add_1_to_1(coname='c1_3', lname='c1_s1', period=1, target_id=-1)
    mlg.add_1_to_1(coname='c1_4', lname='c1_3', period=1, target_id=-1)
    mlg.add_1_to_1(coname='c1_5', lname='c1_s2', period=1, target_id=-1)
    mlg.add_1_to_1(coname='c1_6', lname='c1_5', period=1, target_id=-1)
    mlg.merge_components(coname='c1_m1', lnames=['c1_4', 'c1_6'])
    mlg.add_n_to_1(coname='c1_7', lname='c1_m1', period=2, target_id=-1)
    mlg.add_1_to_n(coname='c1_8', lname='c1_7', n=15, period=7, target_ids=[])
    mlg.cvt_edge_to_edges()
    G = mlg.get_graph()

    plot_nx(G, use_plt=True, use_neo4j=False)

def test_graph_3():
    '''
    说明：
        多部图
    '''
    mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
    mlg.shuffle_ids()
    mlg.add_n(coname='c1_1', n=30, min_amount=200, max_amount=400, start=0, period=7, target_ids=[])
    mlg.add_n_to_n(coname='c1_2', lname='c1_1', n=4, period=2, target_ids=[])
    mlg.add_n_to_n_prob(coname='c1_3', lname='c1_2', n=4, period=2, prob=0.5, target_ids=[])
    mlg.add_n_to_n_prob(coname='c1_4', lname='c1_3', n=4, period=2, prob=0.5, target_ids=[])
    mlg.add_n_to_n_prob(coname='c1_5', lname='c1_4', n=4, period=2, prob=0.5, target_ids=[])
    mlg.add_n_to_1(coname='c1_6', lname='c1_5', period=2, target_id=-1)
    mlg.add_1_to_n(coname='c1_7', lname='c1_6', n=15, period=3, target_ids=[])
    mlg.cvt_edge_to_edges()
    G = mlg.get_graph()

    plot_nx(G, use_plt=True, use_neo4j=False)

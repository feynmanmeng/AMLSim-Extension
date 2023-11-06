from gen_ml_graph import MLGraph
from tools import plot_nx


def gen_cal_split_point_graph():
    '''
    说明：
        存在社区分裂的交易图，用于密度聚类识别拐点
    '''
    mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)

    mlg.add_n(coname='a', n=2, min_amount=1000, max_amount=1000, start=0, period=0, target_ids=[1, 2])
    mlg.add_n_to_1(coname='b', lname='a', period=1, target_id=3)
    mlg.add_1_to_1(coname='c', lname='b', period=1, target_id=4)
    mlg.add_1_to_n(coname='d', lname='c', n=3, period=1, target_ids=[5, 6, 7])
    mlg.split_components(lname='d', n_accounts=[1, 1, 1], conames=['e', 'f', 'g'])
    mlg.add_1_to_n(coname='h', lname='f', n=2, period=1, target_ids=[8, 9])
    mlg.split_components(lname='h', n_accounts=[1, 1], conames=['i', 'j'])
    mlg.add_1_to_1(coname='k', lname='e', period=1, target_id=8)
    mlg.merge_components(coname='l', lnames=['k', 'j'])
    mlg.add_n_to_1(coname='m', lname='l', period=1, target_id=10)
    mlg.add_1_to_1(coname='n', lname='m', period=1, target_id=11)
    mlg.add_1_to_n(coname='o', lname='g', n=2, period=1, target_ids=[12, 13])
    mlg.add_n_to_1(coname='p', lname='o', period=1, target_id=14)
    mlg.add_1_to_1(coname='q', lname='p', period=1, target_id=15)
    mlg.add_1_to_n(coname='r', lname='n', n=2, period=1, target_ids=[16, 17])
    mlg.add_1_to_1(coname='s', lname='q', period=1, target_id=17)
    mlg.add_1_to_1(coname='t', lname='s', period=1, target_id=18)
    return mlg
import os
import pandas
import networkx as nx
from gen_ml_graph import MLGraph


class MLMode():
    '''
    '''

    def __init__(self):
        self.gs = dict()  # {name : g}
        # self.info = '说明'
        # self.g_name = 'graph_id'
        # self.id_start = 0
        # self.id_end = 1e3
        # self.start_step = 0
        # self.margin_ratio = 0.99
        # self.alertid = 1 # 异常

    def get_graph(self, name=None):
        if name == None:
            return self.gs
        else:
            return self.gs[name]

    def m1(self, g_name='单收集 - 单节点 - 单分散'):
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        # mlg.shuffle_ids()
        mlg.add_n(coname='c1_1', n=30, min_amount=200, max_amount=400, start=0, period=7, target_ids=[])
        mlg.add_1_to_1(coname='c1_2', lname='c1_1', period=1, target_id=-1)
        mlg.add_1_to_n(coname='c1_3', lname='c1_2', n=5, period=7, target_ids=[])
        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m2(self, g_name='单收集 - 3节点平行传递 - 单分散'):
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

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m3(self, info='单收集 - 多部图 - 单分散'):
        g_name = 'm3'
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        mlg.shuffle_ids()
        mlg.add_n(coname='c1_1', n=30, min_amount=200, max_amount=400, start=0, period=7, target_ids=[])
        mlg.add_n_to_n(coname='c1_2', lname='c1_1', n=4, period=2, target_ids=[])
        mlg.add_n_to_n_prob(coname='c1_3', lname='c1_2', n=4, period=2, prob=0.5, target_ids=[])
        mlg.add_n_to_n_prob(coname='c1_4', lname='c1_3', n=4, period=2, prob=0.5, target_ids=[])
        mlg.add_n_to_n_prob(coname='c1_5', lname='c1_4', n=4, period=2, prob=0.5, target_ids=[])
        mlg.add_n_to_1(coname='c1_6', lname='c1_5', period=2, target_id=-1)
        mlg.add_1_to_n(coname='c1_7', lname='c1_6', n=15, period=3, target_ids=[])

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m4(self, info='树状收集 - 多部图 - 单分散'):
        # mlg.add_n(coname='', n=, min_amount=1000, max_amount=1000, start=1, period=0, target_ids=[])
        # mlg.add_1_to_1(coname='', lname='', period=1, target_id=-1)
        # mlg.add_n_to_1(coname='', lname='', period=1, target_id=-1)
        # mlg.add_1_to_n(coname='', lname='', n=, period=1, target_ids=[])
        # mlg.add_n_to_n(coname='', lname='', n=, period=1, target_ids=[])
        # mlg.add_n_to_n_prob(coname='', lname='', n=, period=1, prob=0.5, target_ids=[])
        # mlg.split_components(lname='', n_accounts=[], conames=[])
        # mlg.merge_components(coname='', lnames=[])
        g_name = 'm4'
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        mlg.shuffle_ids()
        mlg.new_n_to_1(name='c1_1', new_n=30, start_step=1, new_period=1, min_amount=200, max_amount=400, period=7)
        mlg.new_n_to_1(name='c1_2', new_n=30, start_step=2, new_period=1, min_amount=200, max_amount=400, period=7)
        mlg.new_n_to_1(name='c1_3', new_n=30, start_step=3, new_period=1, min_amount=200, max_amount=400, period=7)
        mlg.merge_components(name='c1_m1', lnames=['c1_1', 'c1_2', 'c1_3'])
        mlg.new_n_to_1(name='c1_4', new_n=30, start_step=2, new_period=1, min_amount=200, max_amount=400, period=7)
        mlg.new_n_to_1(name='c1_5', new_n=30, start_step=3, new_period=1, min_amount=200, max_amount=400, period=7)
        mlg.new_n_to_1(name='c1_6', new_n=30, start_step=1, new_period=1, min_amount=200, max_amount=400, period=7)
        mlg.merge_components(name='c1_m2', lnames=['c1_4', 'c1_5', 'c1_6'])
        mlg.new_n_to_1(name='c1_7', new_n=30, start_step=3, new_period=1, min_amount=200, max_amount=400, period=7)
        mlg.new_n_to_1(name='c1_8', new_n=30, start_step=2, new_period=1, min_amount=200, max_amount=400, period=7)
        mlg.new_n_to_1(name='c1_9', new_n=30, start_step=1, new_period=1, min_amount=200, max_amount=400, period=7)
        mlg.merge_components(name='c1_m3', lnames=['c1_7', 'c1_8', 'c1_9'])
        mlg.add_n_to_1(name='c1_10', lname='c1_m1', period=2)
        mlg.add_n_to_1(name='c1_11', lname='c1_m2', period=2)
        mlg.add_n_to_1(name='c1_12', lname='c1_m3', period=2)
        mlg.merge_components(name='c1_m4', lnames=['c1_10', 'c1_11', 'c1_12'])
        mlg.add_n_to_1(name='c1_13', lname='c1_m4', period=2)
        mlg.add_1_to_n(name='c1_14', lname='c1_13', n=8, period=2)
        mlg.add_n_to_n_prob(name='c1_15', lname='c1_14', n=6, period=2, prob=0.5)
        mlg.add_n_to_n_prob(name='c1_16', lname='c1_15', n=4, period=2, prob=0.5)
        mlg.add_n_to_n_prob(name='c1_17', lname='c1_16', n=2, period=2, prob=0.5)
        mlg.add_n_to_1(name='c1_18', lname='c1_17', period=2)
        mlg.add_1_to_n(name='c1_19', lname='c1_18', n=15, period=3)

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m5(self, info='串联多级', g_name='m5', id_start=0, id_end=250, start_step=1, margin_ratio=0.99, alertid=1):
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        mlg.shuffle_ids()
        mlg.new_n_to_1(name='c1_1', new_n=50, start_step=start_step, new_period=1, min_amount=200, max_amount=400,
                       period=1)
        mlg.add_1_to_n(name='c1_2', lname='c1_1', n=8, period=1)
        mlg.add_n_to_1(name='c1_3', lname='c1_2', period=1)
        mlg.add_1_to_n(name='c1_4', lname='c1_3', n=8, period=1)
        mlg.add_n_to_n_prob(name='c1_5', lname='c1_4', n=6, period=1, prob=0.5)
        mlg.add_n_to_n_prob(name='c1_6', lname='c1_5', n=4, period=1, prob=0.5)
        mlg.add_n_to_1(name='c1_7', lname='c1_6', period=1)
        mlg.add_1_to_n(name='c1_8', lname='c1_7', n=25, period=1)

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m6(self, info='多路并行环形', g_name='m6', id_start=0, id_end=250, start_step=1, margin_ratio=0.99, alertid=1):
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        mlg.shuffle_ids()
        mlg.new_n_to_1(name='c1_1', new_n=25, start_step=start_step, new_period=1, min_amount=200, max_amount=400,
                       period=1)
        mlg.add_1_to_n(name='c1_2', lname='c1_1', n=4, period=1)
        mlg.add_n_to_n(name='c1_3', lname='c1_2', n=6, period=1)
        cycle_nodeid = mlg.add_n_to_1(name='c1_4', lname='c1_3', period=1, ret=True)  # 返回当前标记的节点

        mlg.add_n_to_n(name='c1_5', lname='c1_4', n=4, period=1)
        mlg.add_n_to_n(name='c1_6', lname='c1_5', n=8, period=1)
        mlg.add_n_to_n(name='c1_7', lname='c1_6', n=5, period=1)
        mlg.add_n_to_n(name='c1_8', lname='c1_7', n=8, period=1)
        mlg.add_n_to_n(name='c1_9', lname='c1_8', n=4, period=1)

        mlg.add_n_to_1(name='c1_10', lname='c1_9', period=1, nodeid=cycle_nodeid)
        mlg.add_1_to_1(name='c1_11', lname='c1_10', period=1)
        mlg.add_1_to_n(name='c1_12', lname='c1_11', n=25, period=1)

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m7(self, info='树形收发', g_name='m7', id_start=0, id_end=250, start_step=1, margin_ratio=0.99, alertid=1):
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        mlg.shuffle_ids()
        mlg.new_n_to_1(name='1', new_n=20, start_step=start_step, new_period=1, min_amount=200, max_amount=400,
                       period=1)
        mlg.new_n(name='2', n=20, start_step=start_step + 1, min_amount=200, max_amount=400)
        mlg.merge_components(name='3', lnames=['1', '2'])
        mlg.add_n_to_1(name='4', lname='3', period=1)
        mlg.new_n(name='5', n=20, start_step=start_step + 2, min_amount=200, max_amount=400)
        mlg.merge_components(name='6', lnames=['4', '5'])
        mlg.add_n_to_1(name='7', lname='6', period=1)
        mlg.add_1_to_n(name='8', lname='7', n=5, period=1)
        mlg.add_n_to_n(name='9', lname='8', n=5, period=1)
        mlg.add_n_to_1(name='10', lname='9', period=1)
        mlg.add_1_to_n(name='11', lname='10', n=2, period=1)  # 第一层分叉
        mlg.split_components(lname='11', n_accounts=[1, 1], names=['s1', 's2'])
        mlg.add_1_to_n(name='s1_1', lname='s1', n=2, period=1)
        mlg.add_1_to_n(name='s2_1', lname='s2', n=2, period=1)
        mlg.split_components(lname='s1_1', n_accounts=[1, 1], names=['ss1', 'ss2'])  # 第二层分支
        mlg.split_components(lname='s2_1', n_accounts=[1, 1], names=['ss3', 'ss4'])
        mlg.add_1_to_n(name='ss1_1', lname='ss1', n=15, period=1)  # 第三层展开
        mlg.add_1_to_n(name='ss2_1', lname='ss2', n=15, period=1)
        mlg.add_1_to_n(name='ss3_1', lname='ss3', n=15, period=1)
        mlg.add_1_to_n(name='ss4_1', lname='ss4', n=15, period=1)

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m8(self, info='混合1', g_name='m8', id_start=0, id_end=250, start_step=1, margin_ratio=0.99, alertid=1):
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        mlg.shuffle_ids()
        mlg.new_n_to_1(name='s1', new_n=30, start_step=start_step, new_period=1, min_amount=200, max_amount=400,
                       period=1)
        mlg.new_n_to_1(name='s2', new_n=30, start_step=start_step, new_period=1, min_amount=200, max_amount=400,
                       period=1)
        mlg.new_n_to_1(name='s3', new_n=30, start_step=start_step, new_period=1, min_amount=200, max_amount=400,
                       period=1)
        mlg.new_n_to_1(name='s4', new_n=30, start_step=start_step, new_period=1, min_amount=200, max_amount=400,
                       period=1)
        mlg.merge_components(name='m7', lnames=['s1', 's2'])
        mlg.add_n_to_1(name='s5', lname='m7', period=1)
        mlg.merge_components(name='m8', lnames=['s3', 's4'])
        mlg.add_n_to_1(name='s6', lname='m8', period=1)
        mlg.add_1_to_n(name='1', lname='s5', n=3, period=1)
        mlg.split_components(lname='1', n_accounts=[1, 1, 1], names=['2', '3', '4'])
        mlg.add_1_to_n(name='5', lname='2', n=5, period=1)
        mlg.add_n_to_n(name='6', lname='5', n=5, period=1)
        mlg.add_n_to_n(name='7', lname='6', n=5, period=1)
        mlg.add_1_to_1(name='8', lname='3', period=1)
        mlg.add_1_to_n(name='9', lname='s6', n=3, period=1)
        mlg.split_components(lname='9', n_accounts=[1, 1, 1], names=['10', '11', '12'])
        mlg.merge_components(name='m1', lnames=['4', '10'])
        mlg.add_n_to_1(name='13', lname='m1', period=1)
        mlg.merge_components(name='m2', lnames=['8', '13'])
        mlg.add_n_to_1(name='14', lname='m2', period=1)
        mlg.merge_components(name='m3', lnames=['7', '14'])
        mlg.add_n_to_1(name='15', lname='m3', period=1)
        mlg.add_1_to_n(name='16', lname='12', n=2, period=1)
        mlg.split_components(lname='16', n_accounts=[1, 1], names=['17', '18'])
        mlg.merge_components(name='m4', lnames=['11', '17'])
        mlg.add_n_to_1(name='19', lname='m4', period=1)
        mlg.add_1_to_n(name='20', lname='18', n=4, period=1)
        mlg.merge_components(name='m5', lnames=['19', '20'])
        mlg.add_n_to_n(name='21', lname='m5', n=5, period=1)
        mlg.add_n_to_n(name='22', lname='21', n=5, period=1)
        mlg.merge_components(name='m6', lnames=['15', '22'])
        loop_index = mlg.add_n_to_1(name='23', lname='m6', period=1, ret=True)
        mlg.add_1_to_n(name='24', lname='23', n=5, period=1)
        mlg.add_n_to_n(name='25', lname='24', n=5, period=1)
        mlg.add_n_to_n(name='26', lname='25', n=5, period=1)
        mlg.add_n_to_1(name='27', lname='26', period=1)
        mlg.add_1_to_n(name='28', lname='27', n=5, period=1)
        mlg.add_n_to_n(name='29', lname='28', n=5, period=1)
        mlg.add_n_to_n(name='30', lname='29', n=5, period=1)
        mlg.add_n_to_1(name='loop', lname='30', period=1, nodeid=loop_index)
        mlg.add_1_to_1(name='sp', lname='loop', period=1)
        mlg.add_1_to_1(name='31', lname='sp', period=1)
        mlg.add_1_to_n(name='32', lname='31', n=25, period=1)
        mlg.split_components(lname='32', n_accounts=[1, 24], names=['33', '34'])
        mlg.add_1_to_n(name='35', lname='33', n=25, period=1)

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m5_max(self, info='串联多级', g_name='m5_max', id_start=0, id_end=250, start_step=1, margin_ratio=0.99,
               alertid=1):
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        mlg.shuffle_ids()
        mlg.new_n_to_1(name='c1_1', new_n=50, start_step=start_step, new_period=1, min_amount=300, max_amount=600,
                       period=1)
        mlg.add_1_to_n(name='c1_2', lname='c1_1', n=8, period=1)
        mlg.add_n_to_1(name='c1_3', lname='c1_2', period=1)
        mlg.add_1_to_n(name='c1_4', lname='c1_3', n=8, period=1)
        mlg.add_n_to_n_prob(name='c1_5', lname='c1_4', n=6, period=1, prob=0.5)
        mlg.add_n_to_n_prob(name='c1_6', lname='c1_5', n=4, period=1, prob=0.5)
        mlg.add_n_to_1(name='c1_7', lname='c1_6', period=1)
        mlg.add_1_to_n(name='c1_8', lname='c1_7', n=25, period=1)

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m6_max(self, info='多路并行环形', g_name='m6_max', id_start=0, id_end=250, start_step=1, margin_ratio=0.99,
               alertid=1):
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        mlg.shuffle_ids()
        mlg.new_n_to_1(name='c1_1', new_n=50, start_step=start_step, new_period=1, min_amount=300, max_amount=600,
                       period=1)
        mlg.add_1_to_n(name='c1_2', lname='c1_1', n=4, period=1)
        mlg.add_n_to_n(name='c1_3', lname='c1_2', n=6, period=1)
        cycle_nodeid = mlg.add_n_to_1(name='c1_4', lname='c1_3', period=1, ret=True)  # 返回当前标记的节点

        mlg.add_n_to_n(name='c1_5', lname='c1_4', n=4, period=1)
        mlg.add_n_to_n(name='c1_6', lname='c1_5', n=8, period=1)
        mlg.add_n_to_n(name='c1_7', lname='c1_6', n=5, period=1)
        mlg.add_n_to_n(name='c1_8', lname='c1_7', n=8, period=1)
        mlg.add_n_to_n(name='c1_9', lname='c1_8', n=4, period=1)

        mlg.add_n_to_1(name='c1_10', lname='c1_9', period=1, nodeid=cycle_nodeid)
        mlg.add_1_to_1(name='c1_11', lname='c1_10', period=1)
        mlg.add_1_to_n(name='c1_12', lname='c1_11', n=25, period=1)

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m7_max(self, info='树形收发', g_name='m7_max', id_start=0, id_end=250, start_step=1, margin_ratio=0.99,
               alertid=1):
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        mlg.shuffle_ids()
        mlg.new_n_to_1(name='1', new_n=20, start_step=start_step, new_period=1, min_amount=300, max_amount=600,
                       period=1)
        mlg.new_n(name='2', n=20, start_step=start_step + 1, min_amount=300, max_amount=600)
        mlg.merge_components(name='3', lnames=['1', '2'])
        mlg.add_n_to_1(name='4', lname='3', period=1)
        mlg.new_n(name='5', n=20, start_step=start_step + 2, min_amount=300, max_amount=600)
        mlg.merge_components(name='6', lnames=['4', '5'])
        mlg.add_n_to_1(name='7', lname='6', period=1)
        mlg.add_1_to_n(name='8', lname='7', n=5, period=1)
        mlg.add_n_to_n(name='9', lname='8', n=5, period=1)
        mlg.add_n_to_1(name='10', lname='9', period=1)
        mlg.add_1_to_n(name='11', lname='10', n=2, period=1)  # 第一层分叉
        mlg.split_components(lname='11', n_accounts=[1, 1], names=['s1', 's2'])
        mlg.add_1_to_n(name='s1_1', lname='s1', n=2, period=1)
        mlg.add_1_to_n(name='s2_1', lname='s2', n=2, period=1)
        mlg.split_components(lname='s1_1', n_accounts=[1, 1], names=['ss1', 'ss2'])  # 第二层分支
        mlg.split_components(lname='s2_1', n_accounts=[1, 1], names=['ss3', 'ss4'])
        mlg.add_1_to_n(name='ss1_1', lname='ss1', n=15, period=1)  # 第三层展开
        mlg.add_1_to_n(name='ss2_1', lname='ss2', n=15, period=1)
        mlg.add_1_to_n(name='ss3_1', lname='ss3', n=15, period=1)
        mlg.add_1_to_n(name='ss4_1', lname='ss4', n=15, period=1)

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m8_max(self, info='混合1', g_name='m8_max', id_start=0, id_end=250, start_step=1, margin_ratio=0.99, alertid=1):
        mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
        mlg.shuffle_ids()
        mlg.new_n_to_1(name='s1', new_n=30, start_step=start_step, new_period=1, min_amount=300, max_amount=600,
                       period=1)
        mlg.new_n_to_1(name='s2', new_n=30, start_step=start_step, new_period=1, min_amount=300, max_amount=600,
                       period=1)
        mlg.new_n_to_1(name='s3', new_n=30, start_step=start_step, new_period=1, min_amount=300, max_amount=600,
                       period=1)
        mlg.new_n_to_1(name='s4', new_n=30, start_step=start_step, new_period=1, min_amount=300, max_amount=600,
                       period=1)
        mlg.merge_components(name='m7', lnames=['s1', 's2'])
        mlg.add_n_to_1(name='s5', lname='m7', period=1)
        mlg.merge_components(name='m8', lnames=['s3', 's4'])
        mlg.add_n_to_1(name='s6', lname='m8', period=1)
        mlg.add_1_to_n(name='1', lname='s5', n=3, period=1)
        mlg.split_components(lname='1', n_accounts=[1, 1, 1], names=['2', '3', '4'])
        mlg.add_1_to_n(name='5', lname='2', n=5, period=1)
        mlg.add_n_to_n(name='6', lname='5', n=5, period=1)
        mlg.add_n_to_n(name='7', lname='6', n=5, period=1)
        mlg.add_1_to_1(name='8', lname='3', period=1)
        mlg.add_1_to_n(name='9', lname='s6', n=3, period=1)
        mlg.split_components(lname='9', n_accounts=[1, 1, 1], names=['10', '11', '12'])
        mlg.merge_components(name='m1', lnames=['4', '10'])
        mlg.add_n_to_1(name='13', lname='m1', period=1)
        mlg.merge_components(name='m2', lnames=['8', '13'])
        mlg.add_n_to_1(name='14', lname='m2', period=1)
        mlg.merge_components(name='m3', lnames=['7', '14'])
        mlg.add_n_to_1(name='15', lname='m3', period=1)
        mlg.add_1_to_n(name='16', lname='12', n=2, period=1)
        mlg.split_components(lname='16', n_accounts=[1, 1], names=['17', '18'])
        mlg.merge_components(name='m4', lnames=['11', '17'])
        mlg.add_n_to_1(name='19', lname='m4', period=1)
        mlg.add_1_to_n(name='20', lname='18', n=4, period=1)
        mlg.merge_components(name='m5', lnames=['19', '20'])
        mlg.add_n_to_n(name='21', lname='m5', n=5, period=1)
        mlg.add_n_to_n(name='22', lname='21', n=5, period=1)
        mlg.merge_components(name='m6', lnames=['15', '22'])
        loop_index = mlg.add_n_to_1(name='23', lname='m6', period=1, ret=True)
        mlg.add_1_to_n(name='24', lname='23', n=5, period=1)
        mlg.add_n_to_n(name='25', lname='24', n=5, period=1)
        mlg.add_n_to_n(name='26', lname='25', n=5, period=1)
        mlg.add_n_to_1(name='27', lname='26', period=1)
        mlg.add_1_to_n(name='28', lname='27', n=5, period=1)
        mlg.add_n_to_n(name='29', lname='28', n=5, period=1)
        mlg.add_n_to_n(name='30', lname='29', n=5, period=1)
        mlg.add_n_to_1(name='loop', lname='30', period=1, nodeid=loop_index)
        mlg.add_1_to_1(name='sp', lname='loop', period=1)
        mlg.add_1_to_1(name='31', lname='sp', period=1)
        mlg.add_1_to_n(name='32', lname='31', n=25, period=1)
        mlg.split_components(lname='32', n_accounts=[1, 24], names=['33', '34'])
        mlg.add_1_to_n(name='35', lname='33', n=25, period=1)

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m_cal_split_point(self, g_name='g'):
        '''
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

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g

    def m(self, info, g_name, id_start, id_end, start_step, margin_ratio, alertid):
        mlg = MLGraph(id_start, id_end, margin_ratio, alertid)
        mlg.shuffle_ids()
        mlg.new_n_to_1(name='c1_1', new_n=50, start_step=start_step, new_period=1, min_amount=200, max_amount=400,
                       period=1)

        g = mlg.get_graph()
        self.gs[g_name] = g
        return g


def nx_to_nodes_edges(g: nx.MultiDiGraph):
    nodes = []
    for u, c in g.nodes.data():
        per = list()
        per.extend([u])
        per.extend(list(c.values()))
        nodes.append(per)
    columns = ['id', 'issar']
    nodes = pandas.DataFrame(nodes, columns=columns)

    edges = []
    for u, v, c in g.edges.data():
        per = list()
        per.extend([u, v])
        per.extend(list(c.values()))
        edges.append(per)
    columns = ['src', 'dst', 'name', 'amount', 'step', 'cotype', 'alertid', 'issar']
    edges = pandas.DataFrame(edges, columns=columns)
    return nodes, edges


def end():
    pass


# %%
if __name__ == '__main__':
    # 创建洗钱结构
    mlm = MLMode()
    G = mlm.m3()
    # G = mlm.m_cal_split_point()

    # plt显示
    from plt_plot import plot_graph_from_nx

    plot_graph_from_nx(G)

    # neo4j导入
    from neo4j_plot.autoloader import nx_to_neo4j

    nx_to_neo4j(G)

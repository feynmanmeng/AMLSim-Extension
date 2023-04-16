import os
import random
import networkx as nx
import numpy
import pandas

from tools import split_float, split_int, merge_graph, nx_to_csv


class MLGraph():
    '''
    os.getcwd()
    '''

    def __init__(self, id_start=0, id_end=250, margin_ratio=0.99, alertid=1):
        # 默认是10k
        self.g = nx.MultiDiGraph()  # 交易图
        self.pre_ids = [x for x in range(id_start, id_end)]  # 预生成的随机节点 id
        self.n_account = 0  # 账户总数
        self.components = dict()  # name : [sub_g, name, cotype, accounts, amounts, steps]
        self.margin_ratio = margin_ratio
        self.alertid = alertid

    def shuffle_ids(self):
        random.shuffle(self.pre_ids)

    def get_n_account(self):
        return self.n_account

    def get_graph(self):
        return self.g

    def get_components(self, tname=None):
        if tname == None:
            return self.components
        else:
            return self.components[tname]

    def _add_n(self, n=30, min_amount=200, max_amount=400, start=0, period=1):
        ''''
        添加 n 个节点，并给每个节点赋予传递金额
        '''
        # accounts = [self.n_account + x for x in range(1, n + 1)]
        accounts = self.pre_ids[:n];
        self.pre_ids = self.pre_ids[n:]
        amounts = [random.uniform(min_amount, max_amount) for x in accounts]
        steps = [start + random.randint(0, period) for x in accounts]
        self.g.add_nodes_from(accounts, issar=True)
        self.n_account += n
        return accounts, amounts, steps

    def new_n(self, name, n, start_step, min_amount, max_amount):
        '''
        新增功能，new_n + add_n_to_1 = new_n_to_1
        '''
        cotype = 'new_n'
        accounts = self.pre_ids[:n];
        self.pre_ids = self.pre_ids[n:]
        amounts = [random.uniform(min_amount, max_amount) / self.margin_ratio for x in accounts]  # n_to_1会乘，所以提前还原
        steps = [start_step for x in accounts]  # 只做标识初始点，不增加
        # 创建图
        sub_g = nx.MultiDiGraph()
        sub_g.add_nodes_from(accounts, issar=True)
        # 合并
        self.g = merge_graph(self.g, sub_g)
        self.n_account += n
        self.components[name] = {'sub_g': sub_g, 'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                 'cotype': cotype}

    def new_n_to_1(self, name, new_n=30, start_step=0, new_period=1, min_amount=200, max_amount=400, period=7):
        cotype = 'n_to_1'
        l_accounts, l_amounts, l_steps = self._add_n(new_n, min_amount, max_amount, start_step, new_period)
        # accounts =  [self.n_account + 1]
        accounts = self.pre_ids[:1];
        self.pre_ids = self.pre_ids[1:]
        amounts_mid = l_amounts
        amounts = [sum(amounts_mid) * self.margin_ratio]
        steps_mid = [x + random.randint(0, period) for x in l_steps]
        steps = [max(steps_mid) + 1]
        # 创建图
        sub_g = nx.MultiDiGraph()
        sub_g.add_nodes_from(accounts, issar=True)
        for l_account, amount, step in zip(l_accounts, amounts_mid, steps_mid):
            sub_g.add_edge(l_account, accounts[0], name=name, amount=amount, step=step, cotype=cotype,
                           alertid=self.alertid, issar=True)
        # 合并
        self.g = merge_graph(self.g, sub_g)
        self.n_account += 1
        self.components[name] = {'sub_g': sub_g, 'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                 'cotype': cotype}

    def add_1_to_1(self, name, lname, period=1):  # 增加指定连接功能
        ''''
        将 1 个输出，连接到 1 节点
        '''
        cotype = '1_to_1'
        _, l_accounts, l_amounts, l_steps, _ = self.components[lname].values()
        # accounts = [self.n_account + 1]
        accounts = self.pre_ids[:1];
        self.pre_ids = self.pre_ids[1:]
        amounts_mid = l_amounts
        amounts = [x * self.margin_ratio for x in amounts_mid]
        steps_mid = l_steps
        steps = [x + period for x in l_steps]
        # 创建图
        sub_g = nx.MultiDiGraph()
        sub_g.add_nodes_from(accounts, issar=True)
        sub_g.add_edge(l_accounts[0], accounts[0], name=name, amount=amounts[0], step=steps[0], cotype=cotype,
                       alertid=self.alertid, issar=True)
        # 合并
        self.g = merge_graph(self.g, sub_g)
        self.n_account += 1
        self.components[name] = {'sub_g': sub_g, 'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                 'cotype': cotype}

    def add_n_to_1(self, name, lname, period=7, ret=False, nodeid=None):
        ''''
        将 n 输出资金分散到 1 个节点上
        ret = True 时，返回 1这个节点的 id
        nodeid = int 时，这个新节点将会用这个 id
        '''

        cotype = 'n_to_1'
        _, l_accounts, l_amounts, l_steps, _ = self.components[lname].values()
        # 选择继续使用后续节点，还是使用指定节点
        if nodeid == None:
            accounts = self.pre_ids[:1];
            self.pre_ids = self.pre_ids[1:]
        else:
            accounts = [nodeid]
        amounts_mid = l_amounts
        amounts = [sum(amounts_mid) * self.margin_ratio]
        steps_mid = [x + random.randint(0, period) for x in l_steps]
        steps = [max(steps_mid) + 1]
        # 创建图
        sub_g = nx.MultiDiGraph()
        sub_g.add_nodes_from(accounts, issar=True)
        for l_account, amount, step in zip(l_accounts, amounts_mid, steps_mid):
            sub_g.add_edge(l_account, accounts[0], name=name, amount=amount, step=step, cotype=cotype,
                           alertid=self.alertid, issar=True)
        # 合并
        self.g = merge_graph(self.g, sub_g)
        self.n_account += 1
        self.components[name] = {'sub_g': sub_g, 'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                 'cotype': cotype}

        if ret == True:
            return accounts[0]  # 返回当前使用的 id

    def add_1_to_n(self, name, lname, n=15, period=7):
        ''''
        将 n 个节点的资金，汇总到 1 个节点，再分散发出
        '''
        cotype = '1_to_n'
        _, l_accounts, l_amounts, l_steps, _ = self.components[lname].values()
        # accounts = [self.n_account + x for x in range(1, n + 1)]
        accounts = self.pre_ids[:n];
        self.pre_ids = self.pre_ids[n:]
        amounts_mid = [x for x in split_float(sum(l_amounts), n)]
        amounts = [x * self.margin_ratio for x in amounts_mid]
        steps_mid = [l_steps[0] + random.randint(0, period) for x in accounts]
        steps = [x + 1 for x in steps_mid]
        # 创建图
        sub_g = nx.MultiDiGraph()
        sub_g.add_nodes_from(accounts, issar=True)
        for account, amount, step in zip(accounts, amounts_mid, steps_mid):
            sub_g.add_edge(l_accounts[0], account, name=name, amount=amount, step=step, cotype=cotype,
                           alertid=self.alertid, issar=True)
        # 合并
        self.g = merge_graph(self.g, sub_g)
        self.n_account += n
        self.components[name] = {'sub_g': sub_g, 'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                 'cotype': cotype}

    def add_n_to_n(self, name, lname, n=5, period=3):
        ''''
        将 n 个节点的资金，各自随机分散到，另外相同的 n 个节点上
        '''
        cotype = 'n_to_n'
        _, l_accounts, l_amounts, l_steps, _ = self.components[lname].values()
        # accounts = [self.n_account + x for x in range(1, n + 1)]
        accounts = self.pre_ids[:n];
        self.pre_ids = self.pre_ids[n:]
        # 分配资金
        amounts_mid = []
        for l_amount in l_amounts:
            amounts_mid.extend([x for x in split_float(l_amount, len(accounts))])
        # 分配时间
        steps_mid = []
        for l_step in l_steps:
            steps_mid.extend([l_step + random.randint(0, period) for x in accounts])
        # 创建图
        sub_g = nx.MultiDiGraph()
        sub_g.add_nodes_from(accounts, issar=True)
        for l_account in l_accounts:
            for account in accounts:
                sub_g.add_edge(l_account, account, name=name, amount=amounts_mid.pop(0), step=steps_mid.pop(0),
                               cotype=cotype, alertid=self.alertid, issar=True)
        # 统计资金、时间
        amounts = []
        steps = []
        for account in accounts:
            amounts.append(sum([c['amount'] for u, v, c in sub_g.edges.data() if v == account]) * self.margin_ratio)
            steps.append(max([c['step'] for u, v, c in sub_g.edges.data() if v == account]) + 1)
        # 合并
        self.g = merge_graph(self.g, sub_g)
        self.n_account += n
        self.components[name] = {'sub_g': sub_g, 'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                 'cotype': cotype}

    def add_n_to_n_prob(self, name, lname, n=2, period=7, prob=0.5):
        ''''
        n 个节点与另 n 个节点，以概率 p 连接， 保证节点至少有一条输入
        '''
        cotype = 'n_to_n_prob'
        _, l_accounts, l_amounts, l_steps, _ = self.components[lname].values()
        # accounts = [self.n_account + x for x in range(1, n + 1)]
        accounts = self.pre_ids[:n];
        self.pre_ids = self.pre_ids[n:]
        # 生成掩膜
        masks = []  # 二维
        for l_amount in l_amounts:
            rands = [random.uniform(0, 1) for x in accounts]  # 随机数
            mask = [1 if rand > prob else 0 for rand in rands]  # 掩膜
            if int(sum(mask)) == 0:  # 保证至少有一个传递资金
                mask[random.randint(0, len(accounts) - 1)] = 1
            masks.append(mask)  # 临时保存
        for i in range(0, len(masks[0])):  # 保证所有输出节点都有输入
            check = [x[i] for x in masks]  # 取每一列
            if int(sum(check)) == 0:  # 如果某一列为空
                insert_loc = random.randint(0, len(masks) - 1)  # 随机分配
                masks[insert_loc][i] = 1
        # masks = [item for sublist in masks for item in sublist] # 展平（两层循环，逐层打开）
        # print(masks)
        # 分配金额
        msks = masks.copy()
        amounts_mid = []
        for l_amount, msk in zip(l_amounts, msks):
            n_activated = int(sum(msk))
            amount_activated = split_float(l_amount, n_activated)
            amounts_mid.extend(amount_activated)
        # 分配时间
        steps_mid = []
        msks = [item for sublist in masks for item in sublist]
        for l_step in l_steps:
            for account in accounts:
                m = msks.pop(0)
                if m == 1:
                    steps_mid.append(l_step + random.randint(0, period))
        # 创建图
        msks = [item for sublist in masks for item in sublist]
        sub_g = nx.MultiDiGraph()
        sub_g.add_nodes_from(accounts, issar=True)
        for l_account in l_accounts:
            for account in accounts:
                m = msks.pop(0)
                if m == 1:
                    sub_g.add_edge(l_account, account, name=name, amount=amounts_mid.pop(0), step=steps_mid.pop(0),
                                   cotype=cotype, alertid=self.alertid, issar=True)
        # 统计资金、时间
        amounts = []
        steps = []
        for account in accounts:
            amounts.append(sum([c['amount'] for u, v, c in sub_g.edges.data() if v == account]) * self.margin_ratio)
            steps.append(max([c['step'] for u, v, c in sub_g.edges.data() if v == account]) + 1)
        # 合并
        self.g = merge_graph(self.g, sub_g)
        self.n_account += n
        self.components[name] = {'sub_g': sub_g, 'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                 'cotype': cotype}

    def _add_k_core(self):
        pass

    def _add_multi_mixed_layers(self):
        pass

    def _add_1_n_1(self):
        '''
        单输入，加入 n 条出口， 继续输出
        '''
        pass

    def _close_cycle(self, name, lname, sname, ratio):
        '''
        将最后一个环节的发散金额，抽取部分，汇入起点出的叶子节点，形成闭环
        '''
        pass

    def _connect_1_1(self):
        pass

    def _insert_1_1_1(self):
        pass

    def _update(self):
        pass

    def merge_components(self, name, lnames=[]):
        ''''
        将多个节点聚合成一个标识
        不引入新节点，当作修改引用
        '''
        cotype = 'merge_components'
        # 包含所有节点信息
        accounts = list()
        amounts = list()
        steps = list()
        for lname in lnames:
            _, _accounts, _amounts, _steps, _ = self.components[lname].values()
            accounts.extend(_accounts)
            amounts.extend([x * self.margin_ratio for x in _amounts])
            steps.extend(_steps)
        # 创建图
        sub_g = nx.MultiDiGraph()
        sub_g.add_nodes_from(accounts, issar=True)
        # 保存
        self.components[name] = {'sub_g': sub_g, 'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                 'cotype': cotype}

    def split_components(self, lname, n_accounts=[1, 1, 2], names=['a', 'b', 'c']):
        ''''
        将多个节点分割成多组标识
        '''
        cotype = 'split_components'
        _, _accounts, _amounts, _steps, _ = self.components[lname].values()
        if sum(n_accounts) != len(_accounts):
            print('数量不匹配');
            return -1
        for n, name in zip(n_accounts, names):
            accounts = _accounts[:n];
            _accounts = _accounts[n:]
            amounts = _amounts[:n];
            _amounts = _amounts[n:]
            steps = _steps[:n];
            _steps = _steps[n:]
            # 创建图
            sub_g = nx.MultiDiGraph()
            sub_g.add_nodes_from(accounts, issar=True)
            # 保存
            self.components[name] = {'sub_g': sub_g, 'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                     'cotype': cotype}


def end():
    pass


# %%
if __name__ == "__main__":
    # 【demo】
    # 单收集 - 单节点 - 单分散
    mlg = MLGraph()
    mlg.shuffle_ids()
    mlg.new_n_to_1(name='c1_1', new_n=30, start_step=0, new_period=1, min_amount=200, max_amount=400, period=7)
    mlg.add_1_to_1(name='c1_2', lname='c1_1', period=1)
    mlg.add_1_to_n(name='c1_3', lname='c1_2', n=5, period=7)
    g = mlg.get_graph()

    # plt显示
    from plt_plot import plot_graph_from_nx

    plot_graph_from_nx(g)

    # neo4j导入
    from neo4j_plot.autoloader import nx_to_neo4j

    nx_to_neo4j(g)

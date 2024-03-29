import random

import networkx as nx
import numpy

from tools import split_float
from my_networkx.common import merge_two_graphes

class MLGraph():
    '''
    os.getcwd()
    '''

    def __init__(self, id_start=1, id_end=250, latest_edge_id=0, margin_ratio=0.99, alertid=1):
        self.G = nx.MultiDiGraph()  # 交易图
        self.id_start = id_start  # 账户id范围起点
        self.id_end = id_end  # 账户id范围终点
        self.account_ids = [x for x in range(self.id_start, self.id_end)]  # 分配给新节点的id从这里取
        self.components = dict()  # name : [sub_g, name, cotype, accounts, amounts, steps]
        self.turnover = margin_ratio
        self.alertid = alertid
        self.latest_edge_id = latest_edge_id

        # 加入 latest_time 属性

    def shuffle_ids(self):
        random.shuffle(self.account_ids)

    def get_graph(self):
        return self.G

    def get_latest_edge_id(self):
        return self.latest_edge_id

    def get_components(self, component_name=None):
        if component_name == None:
            return self.components
        else:
            return self.components[component_name]

    def add_n(self, coname, n=5, min_amount=200, max_amount=400, start=1, period=0, target_ids=[], cotype='add_n'):
        '''
        向图中添加孤立的n个账户
        '''
        # 分配账户id
        if len(target_ids) == 0:
            accounts = self.account_ids[:n]
            self.account_ids = self.account_ids[n:]
        else:
            for node in target_ids:
                if node in self.G.nodes():
                    print(f'节点{node}已存在。')
                    exit(0)
                else:
                    self.account_ids.remove(node)
            accounts = target_ids

        # 分配账户金额
        amounts = [round(random.uniform(min_amount, max_amount), 1) for x in accounts]
        # 分配该账户的时间，后续连接需要不能小于这个数
        steps = [start + random.randint(0, period) for x in accounts]
        # 创建图
        sub_g = nx.MultiDiGraph()
        new_nodes = [(id, {'amounts': a, 'steps': s, 'cotype': cotype, 'coname': coname, 'issar': True}) for id, a, s in
                     zip(accounts, amounts, steps)]
        sub_g.add_nodes_from(new_nodes)
        # 合并
        self.G = merge_two_graphes(self.G, sub_g)
        # 记录
        self.components[coname] = {'sub_g': sub_g,
                                   'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                   'cotype': cotype, 'coname': coname, 'issar': True, 'alert_id': self.alertid}

    def add_n_to_1(self, coname, lname, period=0, target_id=-1, cotype='n_to_1'):
        '''
        将 n 输出资金分散到 1 个节点上
        '''
        if target_id == -1:
            self.add_n_to_n(coname=coname, lname=lname, n=1, period=period, target_ids=[], cotype=cotype)
        else:
            self.add_n_to_n(coname=coname, lname=lname, n=1, period=period, target_ids=[target_id], cotype=cotype)

    def add_1_to_1(self, coname, lname, period=0, target_id=-1, cotype='1_to_1'):  # 增加指定连接功能
        ''''
        将 1 个输出，连接到 1 节点
        '''
        if target_id == -1:
            self.add_n_to_n(coname=coname, lname=lname, n=1, period=period, target_ids=[], cotype=cotype)
        else:
            self.add_n_to_n(coname=coname, lname=lname, n=1, period=period, target_ids=[target_id], cotype=cotype)

    def add_1_to_n(self, coname, lname, n=5, period=0, target_ids=[], cotype='1_to_n'):
        ''''
        将 n 个节点的资金，汇总到 1 个节点，再分散发出
        '''
        self.add_n_to_n(coname=coname, lname=lname, n=n, period=period, target_ids=target_ids, cotype=cotype)

    def add_n_to_n(self, coname, lname, n=5, period=0, target_ids=[], cotype='n_to_n'):
        '''
        将 n 个节点的资金，各自随机分散到，另外相同的 n 个节点上
        '''
        self.add_n_to_n_prob(coname=coname, lname=lname, n=n, period=period, prob=1, target_ids=target_ids,
                             cotype=cotype)

    def add_n_to_n_prob(self, coname, lname, n=5, period=0, prob=0.5, target_ids=[], cotype='n_to_n_prob'):
        ''''
        n 个节点与另 n 个节点，以概率 p 连接， 保证节点至少有一条输入
        '''
        _, l_accounts, l_amounts, l_steps, _, _, _, _ = self.components[lname].values()
        # 指定后续 n 个节点的 id，指定的 target_ids 数量不能超过 n
        delta = n - len(target_ids)
        if delta > 0:
            # 需要补充 target_ids
            target_ids.extend(self.account_ids[:delta])
        # 计算后续节点，已有的资金和时间
        accounts = target_ids
        exist_amounts = list()
        exist_steps = list()
        for target_id in target_ids:
            if target_id in self.G.nodes():
                # 说明 target_id 之前被使用过
                exist_amounts.append(nx.get_node_attributes(self.G, 'amounts')[target_id])
                exist_steps.append(nx.get_node_attributes(self.G, 'steps')[target_id])
            else:
                # 第一次使用，后续不可以再用它分配新节点
                self.account_ids.remove(target_id)
                exist_amounts.append(0)
                exist_steps.append(0)

        # 生成掩膜
        masks = []  # 二维
        for _ in l_amounts:
            rands = [random.uniform(0, 1) for _ in accounts]  # 随机数
            mask = [1 if rand <= prob else 0 for rand in rands]  # 掩膜
            if int(sum(mask)) == 0:  # 保证至少有一个传递资金
                mask[random.randint(0, len(accounts) - 1)] = 1
            masks.append(mask)  # 临时保存

        for i in range(0, len(accounts)):  # 保证所有输出节点都有输入
            check_col = [x[i] for x in masks]  # 取每一列
            if int(sum(check_col)) == 0:  # 如果某一列为空
                insert_loc = random.randint(0, len(masks) - 1)  # 随机分配
                masks[insert_loc][i] = 1
        # masks = [item for sublist in masks for item in sublist] # 展平（两层循环，逐层打开）
        # print(masks)

        # 资金
        amounts_mid = []
        amounts = exist_amounts
        for l_amount, mask in zip(l_amounts, masks):
            n_active = int(sum(mask))  # 激活的节点数量
            _1_to_n = [round(x * self.turnover, 1) for x in split_float(l_amount, n_active)]  # 连边上的金额（拆分之前的资金）
            per_amounts_mid = list()
            for _mask in mask:
                if _mask == 1:
                    per_amounts_mid.append(_1_to_n.pop(0))
                else:
                    per_amounts_mid.append(0)  # 无效边资金为0表示不需要连接
            amounts_mid.append(per_amounts_mid)
            amounts = [round(a + b, 1) for a, b in zip(amounts, per_amounts_mid)]

        # 时间
        steps_mid = []
        steps = exist_steps
        for l_step, mask in zip(l_steps, masks):
            n_active = int(sum(mask))  # 激活的节点数量
            _1_to_n = [s + random.randint(0, period) for s in [l_step] * n_active]  # 连边上的时间，由 n_active 决定
            per_steps_mid = list()
            for _mask in mask:
                if _mask == 1:
                    per_steps_mid.append(_1_to_n.pop(0))
                else:
                    per_steps_mid.append(0)  # 无效边时间设为0不要紧
            steps_mid.append(per_steps_mid)
            steps = [max(a, b) for a, b in zip(steps, per_steps_mid)]

        # 创建图
        sub_g = nx.MultiDiGraph()
        new_nodes = [(id, {'amounts': a, 'steps': s, 'cotype': cotype, 'coname': coname, 'issar': True}) for
                     id, a, s in
                     zip(accounts, amounts, steps)]
        sub_g.add_nodes_from(new_nodes)
        for l_account, amounts_m, steps_m in zip(l_accounts, amounts_mid, steps_mid):
            for account, amount, step in zip(accounts, amounts_m, steps_m):
                # 是否掩膜跳过
                if amount != 0:
                    # 添加交易
                    sub_g.add_edge(l_account, account,
                                   id=self.latest_edge_id, amount=amount, step=step,
                                   coname=coname, cotype=cotype, alertid=self.alertid, issar=True)
                    self.latest_edge_id += 1
                    # 减去发出金额账户拥有的资金
                    self.G.nodes[l_account]['amounts'] = round((self.G.nodes[l_account]['amounts'] - amount), 1)
        # 合并
        self.G = merge_two_graphes(self.G, sub_g)
        # 记录
        self.components[coname] = {'sub_g': sub_g,
                                   'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                   'cotype': cotype, 'coname': coname, 'issar': True, 'alert_id': self.alertid}

    def merge_components(self, coname, lnames: list):
        ''''
        将多个节点聚合成一个标识
        不引入新节点，当作修改引用
        '''
        cotype = 'merge'
        # 包含所有节点信息
        accounts = list()
        amounts = list()
        steps = list()
        for lname in lnames:
            _, l_accounts, l_amounts, l_steps, _, _, _, _ = self.components[lname].values()
            accounts.extend(l_accounts)
            amounts.extend(l_amounts)
            steps.extend(l_steps)
        # 创建图
        sub_g = nx.MultiDiGraph()
        new_nodes = [(id, {'amounts': a, 'steps': s, 'cotype': cotype, 'coname': coname, 'issar': True}) for
                     id, a, s in
                     zip(accounts, amounts, steps)]
        sub_g.add_nodes_from(new_nodes)
        # 合并（更新信息）
        self.G = merge_two_graphes(self.G, sub_g)
        # 记录
        self.components[coname] = {'sub_g': sub_g,
                                   'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                   'cotype': cotype, 'coname': coname, 'issar': True, 'alert_id': self.alertid}

    def split_components(self, lname, n_accounts: list, conames: list):
        ''''
        将多个节点分割成多组标识
            n_accounts = [1, 1, 2]
                每一个组包含多少个账户
            conames = ['a', 'b', 'c']
                每一个组的coname叫什么
        '''
        cotype = 'split'
        _, l_accounts, l_amounts, l_steps, _, _, _, _ = self.components[lname].values()
        for n, coname in zip(n_accounts, conames):
            # 账户
            accounts = l_accounts[:n]
            l_accounts = l_accounts[n:]
            # 金额
            amounts = l_amounts[:n]
            l_amounts = l_amounts[n:]
            # 时间
            steps = l_steps[:n]
            l_steps = l_steps[n:]
            # 创建图
            sub_g = nx.MultiDiGraph()
            new_nodes = [(id, {'amounts': a, 'steps': s, 'cotype': cotype, 'coname': coname, 'issar': True}) for
                         id, a, s in
                         zip(accounts, amounts, steps)]
            sub_g.add_nodes_from(new_nodes)
            # 合并（更新信息）
            self.G = merge_two_graphes(self.G, sub_g)
            # 记录
            self.components[coname] = {'sub_g': sub_g,
                                       'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                       'cotype': cotype, 'coname': coname, 'issar': True, 'alert_id': self.alertid}

    def cvt_edge_to_edges(self):
        '''
        【临时简单的处理多重边的情况】
        检查图中的所有边，将单边转换为多边。
        '''
        # 单转多（每条边转为1-4条边的概率）
        func_n_edges_rand = lambda x=0: numpy.random.choice([1, 2, 3, 4], p=[0.1, 0.3, 0.5, 0.1])

        # 建立 G 的拷贝 GM
        GM = self.G.copy()

        # 遍历图G的所有边
        for src, dst, attr_dict in self.G.edges.data():
            # 将当前边拆分成多条边，边上的amount属性拆分成相同的金额，边上的step属性和其他属性拷贝一份就可以。生成的边的数量由func_n_edges_rand生成。
            n_multi_edges = func_n_edges_rand()
            new_ids = [self.latest_edge_id + i for i in range(n_multi_edges)]  # 拆分后的边的id
            new_amounts = split_float(attr_dict['amount'], n_multi_edges)  # 拆分后的金额
            new_amounts = [round(a, 1) for a in new_amounts]  # 保留一位小数

            # 更新 latest_edge_id
            self.latest_edge_id += n_multi_edges

            # 删除当前边
            GM.remove_edge(src, dst)

            # 添加新边
            for id, amount in zip(new_ids, new_amounts):
                new_attr_dict = attr_dict.copy()  # 拷贝属性
                new_attr_dict.update({'id': id})  # 更新id
                new_attr_dict.update({'amount': amount})  # 更新金额
                GM.add_edge(src, dst, **new_attr_dict)

        # 替换 self.G
        self.G = GM

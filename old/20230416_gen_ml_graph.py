class old():

    def add_n_to_1(self, coname, lname, period=0, target_id=-1, cotype='n_to_1'):
        '''
        将 n 输出资金分散到 1 个节点上
        ret = True 时，返回 1这个节点的 id
        nodeid = int 时，这个新节点将会用这个 id
        '''
        _, l_accounts, l_amounts, l_steps, _, _, _, _ = self.components[lname].values()
        # 选择继续使用后续节点，还是使用指定节点（需要在节点id允许的范围内）
        if target_id == -1:
            accounts = self.account_ids[:1]
            self.account_ids = self.account_ids[1:]
            exist_amounts = 0
            exist_steps = 0
        else:
            if target_id in self.G.nodes():
                accounts = [target_id]
                exist_amounts = nx.get_node_attributes(self.G, 'amounts')[target_id]  # 现有存款
                exist_steps = nx.get_node_attributes(self.G, 'steps')[target_id]  # 最近一次发生的时间
            else:
                accounts = [target_id]
                self.account_ids.remove(target_id)
                exist_amounts = 0
                exist_steps = 0

        # 金额
        amounts_mid = [round(x * self.turnover, 1) for x in l_amounts]  # 连边上的金额
        amounts = [round(exist_amounts + sum(amounts_mid), 1)]  # 汇入账户向后传递的金额
        # 时间
        steps_mid = [x + random.randint(0, period) for x in l_steps]  # 连边上的时间
        steps = [max(exist_steps, max(steps_mid))]  # 汇入账户的最终时间
        # 创建图（覆盖更新）
        sub_g = nx.MultiDiGraph()
        new_nodes = [(id, {'amounts': a, 'steps': s, 'cotype': cotype, 'coname': coname, 'issar': True}) for id, a, s in
                     zip(accounts, amounts, steps)]
        sub_g.add_nodes_from(new_nodes)
        for l_account, amount, step in zip(l_accounts, amounts_mid, steps_mid):
            # 添加交易
            sub_g.add_edge(l_account, accounts[0],
                           id=self.n_edges, amount=amount, step=step,
                           coname=coname, cotype=cotype, alertid=self.alertid, issar=True)
            self.n_edges += 1
            # 减去发出金额账户拥有的资金
            self.G.nodes[l_account]['amounts'] = round((self.G.nodes[l_account]['amounts'] - amount), 1)
        # 合并
        self.G = merge_graph(self.G, sub_g)
        # 记录
        self.components[coname] = {'sub_g': sub_g,
                                   'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                   'cotype': cotype, 'coname': coname, 'issar': True, 'alert_id': self.alertid}

    def add_1_to_1(self, coname, lname, period=0, target_id=-1, cotype='1_to_1'):  # 增加指定连接功能
        ''''
        将 1 个输出，连接到 1 节点
        '''
        self.add_n_to_1(coname, lname, period, target_id, cotype)

    def add_1_to_n(self, coname, lname, n=5, period=0, target_ids=[], cotype='1_to_n'):
        ''''
        将 n 个节点的资金，汇总到 1 个节点，再分散发出
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

        # 金额
        amounts_mid = [round(x * self.turnover, 1) for x in split_float(sum(l_amounts), n)]  # 连边上的金额
        amounts = [round(a + e, 1) for a, e in zip(amounts_mid, exist_amounts)]  # 汇入账户向后传递的金额（连边 + 已有）

        # 时间
        steps_mid = [s + random.randint(0, period) for s in l_steps * n]  # 连边上的时间，因为前一个只有一个，所以*n
        steps = [max(e, s) for s, e in zip(steps_mid, exist_steps)]  # 汇入账户的最终时间

        # 创建图（覆盖更新）
        sub_g = nx.MultiDiGraph()
        new_nodes = [(id, {'amounts': a, 'steps': s, 'cotype': cotype, 'coname': coname, 'issar': True}) for id, a, s in
                     zip(accounts, amounts, steps)]
        sub_g.add_nodes_from(new_nodes)
        for account, amount, step in zip(accounts, amounts_mid, steps_mid):
            # 添加交易
            sub_g.add_edge(l_accounts[0], account,
                           id=self.n_edges, amount=amount, step=step,
                           coname=coname, cotype=cotype, alertid=self.alertid, issar=True)
            self.n_edges += 1
            # 减去发出金额账户拥有的资金
            self.G.nodes[l_accounts[0]]['amounts'] = round((self.G.nodes[l_accounts[0]]['amounts'] - amount), 1)
        # 合并
        self.G = merge_graph(self.G, sub_g)
        # 记录
        self.components[coname] = {'sub_g': sub_g,
                                   'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                   'cotype': cotype, 'coname': coname, 'issar': True, 'alert_id': self.alertid}

    def add_n_to_n(self, coname, lname, n=5, period=0, target_ids=[], cotype='n_to_n'):
        '''
        ok，涵盖前3个
        将 n 个节点的资金，各自随机分散到，另外相同的 n 个节点上
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

        # 资金
        amounts_mid = []
        amounts = exist_amounts
        for l_amount in l_amounts:
            _1_to_n = [round(x * self.turnover, 1) for x in split_float(l_amount, n)]  # 连边上的金额
            amounts_mid.append(_1_to_n)
            amounts = [round(a + b, 1) for a, b in zip(amounts, _1_to_n)]
        # 时间
        steps_mid = []
        steps = exist_steps
        for l_step in l_steps:
            _1_to_n = [s + random.randint(0, period) for s in [l_step] * n]  # 连边上的时间，因为前一个只有一个，所以*n
            steps_mid.append(_1_to_n)
            steps = [max(a, b) for a, b in zip(steps, _1_to_n)]

        # 创建图
        sub_g = nx.MultiDiGraph()
        new_nodes = [(id, {'amounts': a, 'steps': s, 'cotype': cotype, 'coname': coname, 'issar': True}) for id, a, s in
                     zip(accounts, amounts, steps)]
        sub_g.add_nodes_from(new_nodes)
        for l_account, amounts_m, steps_m in zip(l_accounts, amounts_mid, steps_mid):
            for account, amount, step in zip(accounts, amounts_m, steps_m):
                # 添加交易
                sub_g.add_edge(l_account, account,
                               id=self.n_edges, amount=amount, step=step,
                               coname=coname, cotype=cotype, alertid=self.alertid, issar=True)
                self.n_edges += 1
                # 减去发出金额账户拥有的资金
                self.G.nodes[l_account]['amounts'] = round((self.G.nodes[l_account]['amounts'] - amount), 1)
        # 合并
        self.G = merge_graph(self.G, sub_g)
        # 记录
        self.components[coname] = {'sub_g': sub_g,
                                   'accounts': accounts, 'amounts': amounts, 'steps': steps,
                                   'cotype': cotype, 'coname': coname, 'issar': True, 'alert_id': self.alertid}
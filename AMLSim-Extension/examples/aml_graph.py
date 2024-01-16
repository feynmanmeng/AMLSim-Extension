from gen_ml_graph import MLGraph


def gen_SML(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=1):
    '''
    :param id_start: 起始node id
    :param id_end: 终止node id
    :param start: 起始时间
    :param alertid: 警报id
    '''
    NCNID = 10
    CNID = [id_end - NCNID + x for x in range(1, NCNID)]  # customized node id，自动分配占前面，手动分配占后100个
    g_name = 'm5'
    mlg = MLGraph(id_start, id_end, latest_edge_id, margin_ratio, alertid)
    # mlg.shuffle_ids()
    mlg.add_n(coname='c1', n=25, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c2', lname='c1', period=1, target_id=-1)
    mlg.add_1_to_n(coname='c3', lname='c2', n=8, period=1, target_ids=[])
    mlg.add_n_to_1(coname='c4', lname='c3', period=1, target_id=-1)
    mlg.add_1_to_n(coname='c5', lname='c4', n=8, period=1, target_ids=[])
    mlg.add_n_to_n_prob(coname='c6', lname='c5', n=6, period=1, prob=0.5, target_ids=[])
    mlg.add_n_to_n_prob(coname='c7', lname='c6', n=4, period=1, prob=0.5, target_ids=[])
    mlg.add_n_to_1(coname='c8', lname='c7', period=1, target_id=-1)
    mlg.add_1_to_n(coname='c9', lname='c8', n=5, period=1, target_ids=[])
    mlg.cvt_edge_to_edges()
    return mlg

def gen_SML_v2(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=1):
    NCNID = 10
    CNID = [id_end - NCNID + x for x in range(1, NCNID)]  # customized node id，自动分配占前面，手动分配占后100个
    g_name = 'SML_v2'
    mlg = MLGraph(id_start, id_end, latest_edge_id, margin_ratio, alertid)
    mlg.add_n(coname='c1', n=10, min_amount=6000, max_amount=9000, start=start, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c2', lname='c1', period=1, target_id=-1)
    mlg.add_n_to_n(coname='c3', lname='c2', n=6, period=1, target_ids=[])
    mlg.add_n_to_1(coname='c4', lname='c3', period=1, target_id=-1)
    mlg.add_1_to_n(coname='c5', lname='c4', n=4, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c6', lname='c5', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c7', lname='c6', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c14', lname='c7', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c15', lname='c14', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c16', lname='c15', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c17', lname='c16', n=4, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c18', lname='c17', n=2, period=1, target_ids=[])
    mlg.split_components(lname='c18', n_accounts=[1, 1], conames=['c19', 'c20'])
    mlg.add_1_to_n(coname='c21', lname='c19', n=3, period=1, target_ids=[])
    mlg.add_1_to_n(coname='c22', lname='c20', n=3, period=1, target_ids=[])
    mlg.cvt_edge_to_edges()
    return mlg


def gen_CML(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=1):
    NCNID = 10
    CNID = [id_end - NCNID + x for x in range(1, NCNID)]  # customized node id，自动分配占前面，手动分配占后100个
    g_name = 'm6'
    mlg = MLGraph(id_start, id_end, latest_edge_id, margin_ratio, alertid)
    # mlg.shuffle_ids()
    mlg.add_n(coname='c1', n=25, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c2', lname='c1', period=1, target_id=-1)
    mlg.add_n_to_n(coname='c3', lname='c2', n=4, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c4', lname='c3', n=6, period=1, target_ids=[])
    mlg.add_n_to_1(coname='c5', lname='c4', period=1, target_id=CNID[0])  # cycle_nodeid
    mlg.add_n_to_n(coname='c6', lname='c5', n=4, period=1, target_ids=[])
    mlg.add_1_to_n(coname='c7', lname='c6', n=8, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c8', lname='c7', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c9', lname='c8', n=8, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c10', lname='c9', n=4, period=1, target_ids=[])
    mlg.add_n_to_1(coname='c11', lname='c10', period=1, target_id=CNID[0])  # cycle_nodeid
    mlg.add_1_to_n(coname='c12', lname='c11', n=8, period=1, target_ids=[])
    mlg.cvt_edge_to_edges()
    return mlg

def gen_CML_v2(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=1):
    NCNID = 10
    CNID = [id_end - NCNID + x for x in range(1, NCNID)]  # customized node id，自动分配占前面，手动分配占后100个
    g_name = 'CML_v2'
    mlg = MLGraph(id_start, id_end, latest_edge_id, margin_ratio, alertid)
    mlg.add_n(coname='c1', n=1, min_amount=6000, max_amount=9000, start=start, period=0, target_ids=[CNID[0]])
    mlg.add_1_to_n(coname='c2', lname='c1', n=2, period=1, target_ids=[])
    mlg.add_n_to_1(coname='c3', lname='c2', period=1, target_id=-1)
    mlg.add_1_to_n(coname='c45', lname='c3', n=2, period=1, target_ids=[CNID[1], CNID[2]])
    mlg.split_components(lname='c45', n_accounts=[1, 1], conames=['c4', 'c5'])

    mlg.add_n(coname='nc1', n=5, min_amount=2000, max_amount=3000, start=3, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c44', lname='nc1', period=1, target_id=CNID[1])

    mlg.add_n(coname='nc2', n=5, min_amount=2000, max_amount=3000, start=3, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c55', lname='nc2', period=1, target_id=CNID[2])

    mlg.add_1_to_1(coname='c7', lname='c44', period=1, target_id=CNID[3])
    mlg.add_n(coname='nc3', n=5, min_amount=2000, max_amount=3000, start=4, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c77', lname='nc3', period=1, target_id=CNID[3])

    mlg.add_1_to_1(coname='c6', lname='c55', period=1, target_id=CNID[4])
    mlg.add_n(coname='nc4', n=5, min_amount=2000, max_amount=3000, start=4, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c66', lname='nc4', period=1, target_id=CNID[4])

    mlg.add_1_to_1(coname='c8', lname='c77', period=1, target_id=CNID[5])
    mlg.add_n(coname='nc5', n=5, min_amount=2000, max_amount=3000, start=5, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c88', lname='nc5', period=1, target_id=CNID[5])

    mlg.add_1_to_1(coname='c9', lname='c66', period=1, target_id=CNID[6])
    mlg.add_n(coname='nc6', n=5, min_amount=2000, max_amount=3000, start=5, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c99', lname='nc6', period=1, target_id=CNID[6])

    mlg.merge_components(coname='m8899', lnames=['c88', 'c99'])
    mlg.add_n_to_1(coname='c10', lname='m8899', period=1, target_id=CNID[0])

    mlg.add_1_to_n(coname='c11', lname='c10', n=4, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c12', lname='c11', n=4, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c13', lname='c12', n=2, period=1, target_ids=[])
    mlg.add_n_to_1(coname='c14', lname='c13', period=1, target_id=-1)
    mlg.add_1_to_n(coname='c15', lname='c14', n=6, period=1, target_ids=[])

    mlg.cvt_edge_to_edges()
    return mlg

def gen_TGS(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=1):
    NCNID = 10
    CNID = [id_end - NCNID + x for x in range(1, NCNID)]  # customized node id，自动分配占前面，手动分配占后100个
    g_name = 'm7'
    mlg = MLGraph(id_start, id_end, latest_edge_id, margin_ratio, alertid)
    # mlg.shuffle_ids()
    mlg.add_n(coname='c1', n=25, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c2', lname='c1', period=1, target_id=-1)
    mlg.add_n(coname='c3', n=25, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.merge_components(coname='c4', lnames=['c2', 'c3'])  # 第一次合并
    mlg.add_n_to_1(coname='c5', lname='c4', period=1, target_id=-1)
    mlg.add_n(coname='c6', n=25, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.merge_components(coname='c7', lnames=['c5', 'c6'])  # 第二次合并
    mlg.add_n_to_1(coname='c8', lname='c7', period=1, target_id=-1)
    mlg.add_1_to_n(coname='c9', lname='c8', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c10', lname='c9', n=5, period=1, target_ids=[])
    mlg.add_n_to_1(coname='c11', lname='c10', period=1, target_id=-1)
    mlg.add_1_to_n(coname='c12', lname='c11', n=2, period=1, target_ids=[])  # 第一层分叉
    mlg.split_components(lname='c12', n_accounts=[1, 1], conames=['s1', 's2'])
    mlg.add_1_to_n(coname='s1_1', lname='s1', n=2, period=1, target_ids=[])
    mlg.add_1_to_n(coname='s2_1', lname='s2', n=2, period=1, target_ids=[])
    mlg.split_components(lname='s1_1', n_accounts=[1, 1], conames=['ss1', 'ss2'])  # 第二层分支
    mlg.split_components(lname='s2_1', n_accounts=[1, 1], conames=['ss3', 'ss4'])
    mlg.add_1_to_n(coname='ss1_1', lname='ss1', n=8, period=1, target_ids=[])  # 第三层展开
    mlg.add_1_to_n(coname='ss2_1', lname='ss2', n=8, period=1, target_ids=[])
    mlg.add_1_to_n(coname='ss3_1', lname='ss3', n=8, period=1, target_ids=[])
    mlg.add_1_to_n(coname='ss4_1', lname='ss4', n=8, period=1, target_ids=[])
    mlg.cvt_edge_to_edges()
    return mlg

def gen_TGS_v2(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=1):
    NCNID = 10
    CNID = [id_end - NCNID + x for x in range(1, NCNID)]  # customized node id，自动分配占前面，手动分配占后100个
    g_name = 'TGS_v2'
    mlg = MLGraph(id_start, id_end, latest_edge_id, margin_ratio, alertid)
    mlg.add_n(coname='c1', n=4, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n(coname='c2', n=4, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n(coname='c3', n=4, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n(coname='c4', n=4, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n(coname='c5', n=4, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n(coname='c6', n=4, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n_to_1(coname='c7', lname='c1', period=1, target_id=-1)
    mlg.add_n_to_1(coname='c8', lname='c2', period=1, target_id=-1)
    mlg.add_n_to_1(coname='c9', lname='c3', period=1, target_id=-1)
    mlg.add_n_to_1(coname='c10', lname='c4', period=1, target_id=-1)
    mlg.add_n_to_1(coname='c11', lname='c5', period=1, target_id=-1)
    mlg.add_n_to_1(coname='c12', lname='c6', period=1, target_id=-1)
    mlg.merge_components(coname='m78', lnames=['c7', 'c8'])
    mlg.merge_components(coname='m910', lnames=['c9', 'c10'])
    mlg.merge_components(coname='m1112', lnames=['c11', 'c12'])
    mlg.add_n_to_1(coname='c13', lname='m78', period=1, target_id=-1)
    mlg.add_n_to_1(coname='c14', lname='m910', period=1, target_id=-1)
    mlg.add_n_to_1(coname='c15', lname='m1112', period=1, target_id=-1)
    mlg.merge_components(coname='m131415', lnames=['c13', 'c14', 'c15'])
    mlg.add_n_to_n_prob(coname='c16', lname='m131415', n=2, period=1, prob=0.5, target_ids=[])
    mlg.add_n_to_1(coname='c17', lname='c16', period=1, target_id=-1)
    mlg.add_1_to_n(coname='m1819', lname='c17', n=2, period=1, target_ids=[])
    mlg.split_components(lname='m1819', n_accounts=[1, 1], conames=['c18', 'c19'])
    mlg.add_1_to_n(coname='m2021', lname='c18', n=2, period=1, target_ids=[])
    mlg.split_components(lname='m2021', n_accounts=[1, 1], conames=['c20', 'c21'])
    mlg.add_1_to_n(coname='m2223', lname='c19', n=2, period=1, target_ids=[])
    mlg.split_components(lname='m2223', n_accounts=[1, 1], conames=['c22', 'c23'])
    mlg.add_1_to_n(coname='c24', lname='c20', n=2, period=1, target_ids=[])
    mlg.add_1_to_n(coname='c25', lname='c21', n=2, period=1, target_ids=[])
    mlg.add_1_to_n(coname='c26', lname='c22', n=2, period=1, target_ids=[])
    mlg.add_1_to_n(coname='c27', lname='c23', n=2, period=1, target_ids=[])

    mlg.cvt_edge_to_edges()
    return mlg


def gen_TSG(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=1):
    NCNID = 10
    CNID = [id_end - NCNID + x for x in range(1, NCNID)]  # customized node id，自动分配占前面，手动分配占后100个
    g_name = 'm8'
    mlg = MLGraph(id_start, id_end, latest_edge_id, margin_ratio, alertid)
    # mlg.shuffle_ids()
    mlg.add_n(coname='c1', n=25, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n_to_1(coname='s1', lname='c1', period=1, target_id=-1)
    mlg.add_n(coname='c2', n=25, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n_to_1(coname='s2', lname='c2', period=1, target_id=-1)
    mlg.add_n(coname='c3', n=25, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n_to_1(coname='s3', lname='c3', period=1, target_id=-1)
    mlg.add_n(coname='c4', n=25, min_amount=3000, max_amount=4000, start=start, period=0, target_ids=[])
    mlg.add_n_to_1(coname='s4', lname='c4', period=1, target_id=-1)
    mlg.merge_components(coname='m7', lnames=['s1', 's2'])
    mlg.add_n_to_1(coname='s5', lname='m7', period=1, target_id=-1)
    mlg.merge_components(coname='m8', lnames=['s3', 's4'])
    mlg.add_n_to_1(coname='s6', lname='m8', period=1, target_id=-1)
    mlg.add_1_to_n(coname='1', lname='s5', n=3, period=1, target_ids=[])
    mlg.split_components(lname='1', n_accounts=[1, 1, 1], conames=['2', '3', '4'])
    mlg.add_1_to_n(coname='5', lname='2', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='6', lname='5', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='7', lname='6', n=5, period=1, target_ids=[])
    mlg.add_1_to_1(coname='8', lname='3', period=1, target_id=-1)
    mlg.add_1_to_n(coname='9', lname='s6', n=3, period=1, target_ids=[])
    mlg.split_components(lname='9', n_accounts=[1, 1, 1], conames=['10', '11', '12'])
    mlg.merge_components(coname='m1', lnames=['4', '10'])
    mlg.add_n_to_1(coname='13', lname='m1', period=1, target_id=-1)
    mlg.merge_components(coname='m2', lnames=['8', '13'])
    mlg.add_n_to_1(coname='14', lname='m2', period=1, target_id=-1)
    mlg.merge_components(coname='m3', lnames=['7', '14'])
    mlg.add_n_to_1(coname='15', lname='m3', period=1, target_id=-1)
    mlg.add_1_to_n(coname='16', lname='12', n=2, period=1, target_ids=[])
    mlg.split_components(lname='16', n_accounts=[1, 1], conames=['17', '18'])
    mlg.merge_components(coname='m4', lnames=['11', '17'])
    mlg.add_n_to_1(coname='19', lname='m4', period=1, target_id=-1)
    mlg.add_1_to_n(coname='20', lname='18', n=4, period=1, target_ids=[])
    mlg.merge_components(coname='m5', lnames=['19', '20'])
    mlg.add_n_to_n(coname='21', lname='m5', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='22', lname='21', n=5, period=1, target_ids=[])
    mlg.merge_components(coname='m6', lnames=['15', '22'])
    mlg.add_n_to_1(coname='23', lname='m6', period=1, target_id=CNID[0])  # loop_index
    mlg.add_1_to_n(coname='24', lname='23', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='25', lname='24', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='26', lname='25', n=5, period=1, target_ids=[])
    mlg.add_n_to_1(coname='27', lname='26', period=1, target_id=-1)
    mlg.add_1_to_n(coname='28', lname='27', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='29', lname='28', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='30', lname='29', n=5, period=1, target_ids=[])
    mlg.add_n_to_1(coname='loop', lname='30', period=1, target_id=CNID[0])  # loop_index
    mlg.add_1_to_1(coname='sp', lname='loop', period=1, target_id=-1)
    mlg.add_1_to_1(coname='31', lname='sp', period=1, target_id=-1)
    mlg.add_1_to_n(coname='32', lname='31', n=8, period=1, target_ids=[])
    mlg.split_components(lname='32', n_accounts=[1, 4], conames=['33', '34'])
    mlg.add_1_to_n(coname='35', lname='33', n=8, period=1, target_ids=[])
    mlg.cvt_edge_to_edges()
    return mlg

def gen_TSG_v2(id_start=0, id_end=500, latest_edge_id=0, margin_ratio=0.999, alertid=1, start=1):
    NCNID = 10
    CNID = [id_end - NCNID + x for x in range(1, NCNID)]  # customized node id，自动分配占前面，手动分配占后100个
    g_name = 'TSG_v2'
    mlg = MLGraph(id_start, id_end, latest_edge_id, margin_ratio, alertid)
    mlg.add_n(coname='c1', n=10, min_amount=7000, max_amount=9000, start=start, period=0, target_ids=[])
    mlg.add_n_to_n(coname='c2', lname='c1', n=2, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c3', lname='c2', n=3, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c4', lname='c3', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c5', lname='c4', n=7, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c6', lname='c5', n=10, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c7', lname='c6', n=10, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c8', lname='c7', n=10, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c9', lname='c8', n=7, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c10', lname='c9', n=5, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c11', lname='c10', n=3, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c12', lname='c11', n=2, period=1, target_ids=[])
    mlg.add_n_to_n(coname='c13', lname='c12', n=6, period=1, target_ids=[])

    mlg.cvt_edge_to_edges()
    return mlg




def end():
    pass




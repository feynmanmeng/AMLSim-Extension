
def test_graph_1():
    mlg = MLGraph(id_start=0, id_end=250, margin_ratio=0.999, alertid=1)
    # mlg.shuffle_ids()
    mlg.add_n(coname='c1_1', n=30, min_amount=200, max_amount=400, start=0, period=7, target_ids=[])
    mlg.add_1_to_1(coname='c1_2', lname='c1_1', period=1, target_id=-1)
    mlg.add_1_to_n(coname='c1_3', lname='c1_2', n=5, period=7, target_ids=[])
    mlg.cvt_edge_to_edges()
    g = mlg.get_graph()
from examples.aml_graph import gen_SML, gen_CML, gen_TGS, gen_TSG, gen_SML_v2, gen_CML_v2, gen_TGS_v2, gen_TSG_v2
from examples.aml_graph_merged import AmlGraphMerged
from examples.other_graph import gen_cal_split_point_graph
from tools import plot_nx, nx_to_csv


def test_gen_cal_split_point_graph():
    mlg = gen_cal_split_point_graph()
    G = mlg.get_graph()
    plot_nx(G=G, use_plt=True, use_neo4j=False)


def test_gen_SML():
    mlg = gen_SML()
    G = mlg.get_graph()
    plot_nx(G=G, use_plt=True, use_neo4j=False)

def test_gen_SML_v2():
    mlg = gen_SML_v2()
    G = mlg.get_graph()
    plot_nx(G=G, use_plt=True, use_neo4j=False)

def test_gen_CML():
    mlg = gen_CML()
    G = mlg.get_graph()
    plot_nx(G=G, use_plt=True, use_neo4j=False)

def test_gen_CML_v2():
    mlg = gen_CML_v2()
    G = mlg.get_graph()
    plot_nx(G=G, use_plt=True, use_neo4j=False)

def test_gen_TGS():
    mlg = gen_TGS()
    G = mlg.get_graph()
    plot_nx(G=G, use_plt=True, use_neo4j=False)

def test_gen_TGS_v2():
    mlg = gen_TGS_v2()
    G = mlg.get_graph()
    plot_nx(G=G, use_plt=True, use_neo4j=False)

def test_gen_TSG():
    mlg = gen_TSG()
    G = mlg.get_graph()
    plot_nx(G=G, use_plt=True, use_neo4j=False)

def test_gen_TSG_v2():
    mlg = gen_TSG_v2()
    G = mlg.get_graph()
    plot_nx(G=G, use_plt=True, use_neo4j=False)

def test_generate_all_4_ml_graphes():
    agm = AmlGraphMerged()

    G = agm.combination_SML()
    nx_to_csv(G, path="./data/sar/SML/")

    G = agm.combination_CML()
    nx_to_csv(G, path="./data/sar/CML/")

    G = agm.combination_TGS()
    nx_to_csv(G, path="./data/sar/TGS/")

    G = agm.combination_TSG()
    nx_to_csv(G, path="./data/sar/TSG/")


def test_generate_all_4_ml_graph_v2():
    mlg = gen_SML_v2()
    G = mlg.get_graph()
    nx_to_csv(G, path="./data/sar/SML_v2/")

    mlg = gen_CML_v2()
    G = mlg.get_graph()
    nx_to_csv(G, path="./data/sar/CML_v2/")

    mlg = gen_TGS_v2()
    G = mlg.get_graph()
    nx_to_csv(G, path="./data/sar/TGS_v2/")

    mlg = gen_TSG_v2()
    G = mlg.get_graph()
    nx_to_csv(G, path="./data/sar/TSG_v2/")
















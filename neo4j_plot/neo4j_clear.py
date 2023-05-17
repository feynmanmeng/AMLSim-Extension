import json
import os
import neo4j
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher

class NeoClear():
    def __init__(self):
        # 1. 获取当前文件所在目录的绝对路径
        dir_path = os.path.dirname(os.path.abspath(__file__))

        # 2. 将neo4j.json文件路径和当前文件所在目录拼接
        self.neo4j_config = os.path.join(dir_path, 'db_connection.json')

        # 3. 读取数据库配置
        with open(self.neo4j_config, 'r', encoding='utf-8') as f:
            self.neo4j_args = json.load(f)

        self.username = self.neo4j_args["username"]
        self.password = self.neo4j_args["password"]
        self.database = self.neo4j_args["database"]
        self.port = self.neo4j_args["port"]

    def process(self,):
        # 连接数据库 【port 默认 7687】
        graph = Graph(f"neo4j://localhost:{self.port}/", auth=(self.username, self.password), name=self.database)
        # 清除neo4j里面的所有数据
        graph.delete_all()
        print("【已清空】")

def autorun_clear():
    nc = NeoClear()
    nc.process()

#%%
if __name__ == '__main__':
    autorun_clear()
    pass



import queue
import threading
import time
import pandas
import neo4j
import os

database = 'tmp'

class Py2Neo4j(threading.Thread):
    def __init__(self, name, q:queue.Queue):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        process(self.name, self.q)

def load_data():
    path = r'./data'

    fname = 'nodes.csv'
    addr = os.path.join(path, fname)
    nodes = pandas.read_csv(addr)

    fname = 'edges.csv'
    addr = os.path.join(path, fname)
    edges = pandas.read_csv(addr)


    return nodes, edges

def gen_data():
    nodes, edges = load_data()

    # Account
    lst_account_export = []

    for r in range(0, nodes.shape[0]):
        id = nodes['id'][r]
        issar = nodes['issar'][r]
        per = [id, issar]
        lst_account_export.append(per)

    # Transaction
    lst_tran_export = []

    return lst_account_export, lst_tran_export


def sep_data(data, queue_work:queue.Queue, batch_size=50, src=0):
    '''
    将数据集分割成小块，并交给queue
    '''
    n_samples = len(data)
    src = 0
    dst = src + batch_size
    n_samples_left = n_samples - src
    while n_samples_left > 0:
        sub_data = data[src:dst]
        queue_work.put(sub_data)
        # 更新
        src += batch_size
        dst += batch_size
        n_samples_left -= batch_size

    return queue_work

def create_account(tx, data):
    for id, issar in data:
        tx.run("create (:Account{id:$id, issar:$issar})",
               id=int(id), issar=bool(issar)
               )

def create_transaction(tx, data):
    for src, dst, name, amount, step, cotype, issar in data:
        tx.run("match (a1:Account{id:$src}), (a2:Account{id:$dst})"
               "create (a1)-[:TRANS{name:$name, amount:$amount, step:$step, cotype:$cotype, issar:$issar}]->(a2)",
               src=int(src), dst=int(dst), name=str(name), amount=float(amount), step=int(step),
               cotype=str(cotype), issar=bool(issar)
               )


def process(thread_name, q:queue.Queue):
    uri = "neo4j://localhost:7687"
    driver = neo4j.GraphDatabase.driver(uri, auth=("neo4j", "key"))

    while not exitFlag:
        with driver.session(database=database) as session:
            thread_lock.acquire()
            if not queue_work.empty():
                sub_data = q.get()
                thread_lock.release()
                print("thread: {} is processing... {} left".format(thread_name, queue_work.qsize()))
                session.write_transaction(create_account, sub_data)
                # session.write_transaction(create_transaction, sub_data)
            else:
                thread_lock.release()

    driver.close() # 关闭数据库连接

def run():
    pass

if __name__ == '__main__':

    exitFlag = False

    n_thread = 16
    thread_name_list = ['t'+str(i) for i in list(range(0,n_thread))]

    queue_work = queue.Queue()
    thread_lock = threading.Lock()
    threads = []

    # 启动线程，监视queue_work
    for thread_name in thread_name_list:
        thread = Py2Neo4j(thread_name, queue_work)
        thread.start()
        threads.append(thread)

    # 要导入的数据
    lst_account_export, lst_tran_export = gen_data()

    # 分割数据
    thread_lock.acquire()
    queue_work = sep_data(lst_account_export, queue_work, batch_size=100)
    # queue_work = sep_data(lst_tran_export, queue_work, batch_size=100)
    thread_lock.release()

    while not queue_work.empty():
        pass

    exitFlag = True

    # 等待所有线程完成
    for t in threads:
        t.join()
    print("退出主线程")











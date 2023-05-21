import pickle
import os


def save(faddr='', var=None):
    # 完整文件路径
    f = open(faddr, 'wb')
    pickle.dump(var, f)


def load(faddr=''):
    # 完整文件路径
    f = open(faddr, 'rb')
    var = pickle.load(f)
    return var


# 模型序列化，假设文件后缀都是pkl
def save_pkl(path='', file_name=None, var=None):
    if not os.path.exists(path):
        os.makedirs(path)
    file_name += '.pkl'
    full_file_addr = os.path.join(path, file_name)
    f = open(full_file_addr, 'wb')
    pickle.dump(var, f)


def load_pkl(path='', file_name=None):
    file_name += '.pkl'
    full_file_addr = os.path.join(path, file_name)
    f = open(full_file_addr, 'rb')
    var = pickle.load(f)
    return var

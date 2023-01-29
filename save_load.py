import pickle
import os


def save(path='', file_name=None, var=None):
    if not os.path.exists(path):
        os.makedirs(path)
    file_name += '.pkl'
    full_file_addr = os.path.join(path, file_name)
    f = open(full_file_addr, 'wb')
    pickle.dump(var, f)

def load(path='', file_name=None):
    file_name += '.pkl'
    full_file_addr = os.path.join(path, file_name)
    f = open(full_file_addr, 'rb')
    var = pickle.load(f)
    return var

def load_oldver(path='', file_name=None):
    file_name += '.pickle'
    full_file_addr = os.path.join(path, file_name)
    f = open(full_file_addr, 'rb')
    var = pickle.load(f, encoding='iso-8859-1')
    return var


import os
import yaml
import time
from datetime import timedelta
from tqdm import tqdm
import pickle as pkl

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def read_config(path):
    return AttrDict(yaml.load(open(path, 'r')))


def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))


def load_data(config, ues_word):
    '''
    创建数据集
    1. 划分训练集、验证集、测试集
    2. 从训练集中提取词汇表
    3. 返回数据
    '''
    return

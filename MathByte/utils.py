# coding: UTF-8
import os
import yaml
import time
import h5py
import pickle
from datetime import timedelta


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def read_config(path):
    return AttrDict(yaml.safe_load(open(path, 'r')))


def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))


def load_data(cache_file_h5py, cache_file_pickle):
    """
    load data from h5py and pickle cache files
    :param cache_file_h5py:
    :param cache_file_pickle:
    :return:
    """
    if not os.path.exists(cache_file_h5py) or not os.path.exists(cache_file_pickle):
        raise RuntimeError("############################ERROR##############################\n. "
                           "请先准备训练集、验证集、测试集")
    f_data = h5py.File(cache_file_h5py, 'r')
    train_X = f_data['train_X']  # np.array(
    train_Y = f_data['train_Y']  # np.array(
    vaild_X = f_data['vaild_X']  # np.array(
    valid_Y = f_data['valid_Y']  # np.array(
    test_X = f_data['test_X']  # np.array(
    test_Y = f_data['test_Y']  # np.array(

    word2index, label2index = None, None
    with open(cache_file_pickle, 'rb') as data_f_pickle:
        word2index, label2index = pickle.load(data_f_pickle)
    return word2index, label2index, train_X, train_Y, vaild_X, valid_Y, test_X, test_Y

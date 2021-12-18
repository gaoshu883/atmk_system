# coding: UTF-8
import time
import torch
import numpy as np
from train_eval import train, init_network
from importlib import import_module
import argparse
import logging

import utils

logging.basicConfig(
    level=logging.INFO,
    filename='train.log',
    filemode='a',
    format='%(asctime)s : %(levelname)s : %(message)s',
)

parser = argparse.ArgumentParser(description='ATMK')
parser.add_argument('--model', type=str, required=True,
                    help='choose a model: cnn, rnn, transformer, bert')
parser.add_argument('--word', default=False, type=bool,
                    help='True for word, False for char')
parser.add_argument('--use_att', default=False, type=bool,
                    help='True for use label attention, False for not')
parser.add_argument('--use_lcm', default=False, type=bool,
                    help='True for use label confusion model, False for not')
parser.add_argument('--config', default='config.yml', type=str,
                    help='config file')
args = parser.parse_args()


if __name__ == '__main__':
    model_name = args.model
    x = import_module('models.' + model_name)  # eg: import models.cnn
    config = utils.read_config(args.config)
    # NOTE 利用随机数种子使得程序可以复现
    # https://cloud.tencent.com/developer/article/1149041
    SEED = 1
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.deterministic = True  # 保证每次结果一样

    logging.info("Loading data...")
    start_time = time.time()
    vocab, train_data, dev_data, test_data = utils.load_data(
        config, args.word)
    train_iter = utils.build_iterator(train_data, config)
    dev_iter = utils.build_iterator(dev_data, config)
    test_iter = utils.build_iterator(test_data, config)
    time_dif = utils.get_time_dif(start_time)
    logging.info("Time usage:", time_dif)

    # train
    config.n_vocab = len(vocab)
    model = x.Model(config).to(config.device)
    if model_name != 'transformer':
        init_network(model)
    print(model.parameters)
    train(config, model, train_iter, dev_iter, test_iter)

# coding: UTF-8
import torch
import numpy as np
from importlib import import_module
import argparse
import logging

import utils
from train_eval import train, test

logging.basicConfig(
    level=logging.INFO,
    filename='train.log',
    filemode='a',
    format='%(asctime)s : %(levelname)s : %(message)s',
)

parser = argparse.ArgumentParser(description='ATMK')
parser.add_argument('--model', type=str, required=True,
                    help='choose a model: cnn, rnn, transformer')
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
    # 保证每次结果一样
    # https://cloud.tencent.com/developer/article/1149041
    SEED = 1
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.deterministic = True

    # 加载数据
    logging.info("Loading data...")
    word2index, label2index, trainX, trainY, vaildX, vaildY, testX, testY = utils.load_data(
        config.cache_file_h5py, config.cache_file_pickle)

    config.vocab_size = len(word2index)
    config.num_classes = len(label2index)
    num_examples, config.sentence_len = trainX.shape
    logging.info("model.vocab_size: %d; num_classes: %d; num_examples of training: %d; sentence_len: %d",
                 config.vocab_size, config.num_classes, num_examples, config.sentence_len)
    logging.info(config)

    # train
    model = x.Model(config, args.use_att)
    for epoch in range(config.epochs):
        logging.info('Epoch [{}/{}]'.format(epoch + 1, config.epochs))
        train(config, model, [trainX, trainY, vaildX, vaildY], args.use_lcm)

    test(config, model, testX, testY)

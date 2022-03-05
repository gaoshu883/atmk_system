# coding: UTF-8
import os
import numpy as np
import argparse
import logging
from datetime import datetime
import pytz
from sklearn.model_selection import KFold, StratifiedKFold

from models import trainer
import utils

logging.basicConfig(
    level=logging.INFO,
    # filename='train.log',
    # filemode='a',
    format='%(asctime)s : %(levelname)s : %(message)s',
)

parser = argparse.ArgumentParser(description='ATMK')
parser.add_argument('--use_att', default=False, type=bool,
                    help='True for use label attention')
parser.add_argument('--use_lcm', default=False, type=bool,
                    help='True for use label confusion model')
parser.add_argument('--config', default='config/config_waa1.yml', type=str,
                    help='config file')
parser.add_argument('--round', default=5, type=int,
                    help='round number')
args = parser.parse_args()

if __name__ == '__main__':
    # 加载配置文件
    logging.info("Loading config...")
    config = utils.read_config(args.config)
    logging.info(config)
    # 加载数据
    logging.info("Loading data...")
    word2index, label2index, X, y = utils.load_data(
        config.cache_file_h5py, config.cache_file_pickle)
    config.vocab_size = len(word2index)
    config.num_classes = len(label2index)
    # 加载预训练的向量
    logging.info("Loading embeddings...")
    embeddings_2dlist = utils.load_embed_data(config.embeddings)
    label_emb_2dlist = None
    if config.get('label_embeddings', None):
        label_emb_2dlist = utils.load_embed_data(config.label_embeddings)
    # 当前模型名称
    model_name = "b"
    if args.use_att & args.use_lcm:
        model_name = "labs"
    elif args.use_att:
        model_name = "lab"
    elif args.use_lcm:
        model_name = "lbs"
    logging.info("model name %s" % model_name)
    # ========== model training: ==========
    # shuffle, split,
    X = np.array(X)
    y = np.array(y)
    kf = KFold(shuffle=True)    # 默认5折
    n = 0
    t_k = utils.randomword(6)
    for train_index, test_index in kf.split(X):
        n += 1
        if n > args.round:
            break
        file_id = '%s-%s-%d-%s' % (t_k, model_name, n, datetime.now(pytz.timezone('Asia/Shanghai')
                                                                    ).strftime("%m%d-%H%M%S"))
        log_dir = os.path.join('logs', file_id)
        print("TRAIN:", train_index, len(train_index),
              "TEST:", test_index, len(test_index))
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        np.random.seed(n)  # 这样保证了每次试验的seed一致
        data_package = [X_train, y_train, X_test, y_test]
        '''
        初始化模拟标签数据（L_train,L_test）
        shape=(None,num_classes)
        [[  0   1   2 ... 424 425 426]
         [  0   1   2 ... 424 425 426]
         [  0   1   2 ... 424 425 426]
         ...
         [  0   1   2 ... 424 425 426]
         [  0   1   2 ... 424 425 426]
         [  0   1   2 ... 424 425 426]]
        '''
        L_train = np.array([np.array(range(config.num_classes))
                           for i in range(len(X_train))])
        L_test = np.array([np.array(range(config.num_classes))
                          for i in range(len(X_test))])
        initial_labels = [L_train, L_test]

        logging.info('--Round: %d', n)
        # labs_model = trainer.LABSModel(
        #     config, embeddings_2dlist, label_emb_matrix=label_emb_2dlist, use_att=args.use_att, use_lcm=args.use_lcm, log_dir=log_dir)
        # labs_model.train(data_package, initial_labels)
        logging.info('=======End=======')

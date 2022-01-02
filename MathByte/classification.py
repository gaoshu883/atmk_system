# coding: UTF-8
import datetime
import numpy as np
import argparse
import logging
from datetime import datetime

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
parser.add_argument('--config', default='config.yml', type=str,
                    help='config file')
args = parser.parse_args()

if __name__ == '__main__':
    # 加载配置文件
    logging.info("Loading config...")
    config = utils.read_config(args.config)
    # 加载数据
    logging.info("Loading data...")
    word2index, label2index, trainX, trainY, vaildX, vaildY, testX, testY = utils.load_data(
        config.cache_file_h5py, config.cache_file_pickle)
    config.vocab_size = len(word2index)
    config.num_classes = len(label2index)
    # 加载预训练的向量
    logging.info("Loading embeddings...")
    embeddings_2dlist = utils.load_embed_data(config.embeddings)

    # ========== model traing: ==========
    N = 1  # TODO 暂时只做一次
    for n in range(N):
        np.random.seed(n)  # 这样保证了每次试验的seed一致
        log_dir = "logs\\fit\\" + datetime.now().strftime("%Y%m%d-%H%M%S")
        data_package = [trainX, trainY, vaildX, vaildY, testX, testY]
        '''
        初始化模拟标签数据（L_train,L_val,L_test）
        [[  0   1   2 ... 424 425 426]
         [  0   1   2 ... 424 425 426]
         [  0   1   2 ... 424 425 426]
         ...
         [  0   1   2 ... 424 425 426]
         [  0   1   2 ... 424 425 426]
         [  0   1   2 ... 424 425 426]]
        '''
        L_train = np.array([np.array(range(config.num_classes))
                           for i in range(len(trainX))])
        L_val = np.array([np.array(range(config.num_classes))
                         for i in range(len(vaildX))])
        L_test = np.array([np.array(range(config.num_classes))
                          for i in range(len(testX))])
        initial_labels = [L_train, L_val, L_test]

        logging.info('--Round: %d', n+1)
        dy_lcm_model = trainer.LSTM_LCM_dynamic(
            config, embeddings_2dlist, use_att=args.use_att, use_lcm=args.use_lcm, log_dir=log_dir)
        dy_lcm_model.train_val(data_package, config.epochs, initial_labels)
        logging.info('=======End=======')

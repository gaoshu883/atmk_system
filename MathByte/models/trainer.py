# checked at 2020.9.14
import numpy as np
import keras
import logging

from .lstm import Classifier
from .lcm import LabelConfusionModel
from .evaluation_metrics import my_evaluator


class LSTM_LCM_dynamic:
    """
    1.可以设置early stop，即设置在某一个epoch就停止LCM的作用
    2.若early stop设置为0，则退化为 basic model
    """

    def __init__(self, config, text_embedding_matrix=None, use_att=False, use_lcm=False, log_dir=None):
        self.num_classes = config.num_classes
        self.batch_size = config.batch_size
        self.lcm_stop = 0  # 默认不加 lcm
        self.basic_model, hid = Classifier.build(
            config, text_embedding_matrix, use_att)
        if use_lcm:
            self.lcm_stop = config.lcm_stop
            self.model = LabelConfusionModel.build(
                config, self.basic_model, hid)
        # 设置训练过程中的回调函数
        tensorboard = keras.callbacks.TensorBoard(
            log_dir=log_dir)
        self.callbacks = [tensorboard]

    def train_val(self, data_package, epochs, initial_labels):
        """实验说明：
        每一轮train完，在val上测试，同时在test上测试
        """
        for i in range(epochs):
            logging.info("Epoch %d starting...", i+1)
            if i < self.lcm_stop:
                self.__lcm_train(data_package, initial_labels, i)
            else:
                self.__basic_train(data_package, initial_labels, i)
        return None

    def __basic_train(self, data_package, label_data, epoch_idx):
        X_train, y_train, X_val, y_val, X_test, y_test = data_package
        L_train, L_val, L_test = label_data
        # 训练阶段会自动记录每batch指标数据
        self.basic_model.fit([X_train, L_train], y_train,
                             batch_size=self.batch_size, verbose=1, epochs=1, callbacks=self.callbacks)  # verbose=1 log 进度条
        # 验证集上实验
        # (样本数量, num_classes)
        pred_probs = self.basic_model.predict([X_val, L_val])
        logging.info('(Orig)Epoch %d | Validate', epoch_idx+1)
        my_evaluator(y_val, pred_probs)

        # 测试集上实验
        pred_probs = self.basic_model.predict([X_test, L_test])
        logging.info('(Orig)Epoch %d | Test', epoch_idx+1)
        my_evaluator(y_test, pred_probs)

    def __lcm_train(self, data_package, label_data, epoch_idx):
        '''
        利用label-confusion-matrix训练模型
        '''
        X_train, y_train, X_val, y_val, X_test, y_test = data_package
        L_train, L_val, L_test = label_data
        self.model.fit([X_train, L_train], y_train,
                       batch_size=self.batch_size, verbose=1, epochs=1, callbacks=self.callbacks)
        # 验证集
        pred_probs = self.model.predict([X_val, L_val])[
            :, :self.num_classes]
        logging.info('(LCM)Epoch %d | Validate', epoch_idx+1)
        my_evaluator(y_val, pred_probs)
        # 测试集
        pred_probs = self.model.predict([X_test, L_test])[
            :, :self.num_classes]
        logging.info('(LCM)Epoch %d | Test', epoch_idx+1)
        my_evaluator(y_test, pred_probs)

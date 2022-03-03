import numpy as np
import keras
from keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from keras.models import load_model
import logging
from matplotlib import pyplot
import keras.backend as K


from .lstm import Classifier
from .lcm import LabelConfusionModel
from .evaluation_metrics import precision_1k, precision_3k, precision_5k, recall_1k, recall_3k, recall_5k, F1_1k, F1_3k, F1_5k, lcm_metrics


class LABSModel:

    def __init__(self, config, text_embedding_matrix=None, label_emb_matrix=None, use_att=False, use_lcm=False, log_dir=None):
        self.epochs = config.epochs
        self.alpha = config.alpha
        self.num_classes = config.num_classes
        self.batch_size = config.batch_size
        self.model_b_h5py = config.model_b_h5py
        self.model_lab_h5py = config.model_lab_h5py
        self.model_lbs_h5py = config.model_lbs_h5py
        self.model_labs_h5py = config.model_labs_h5py
        self.use_att = use_att
        self.use_lcm = use_lcm
        self.model_name = self.__get_saved_model_name()

        self.basic_model, hid, label_emb = Classifier.build(
            config, text_embedding_matrix, use_att, label_emb_matrix, [
                precision_1k, precision_3k, recall_1k, recall_3k, F1_1k, F1_3k])
        es_monitor = "val_loss"
        mc_monitor = "val_precision_1k"

        if use_lcm:
            loss, metrics = lcm_metrics(self.num_classes, self.alpha)
            self.model = LabelConfusionModel.build(
                config, self.basic_model, hid, label_emb, loss, metrics)
            es_monitor = "val_lcm_loss"
            mc_monitor = "val_lcm_precision_1k"
        # 设置训练过程中的回调函数
        tb = TensorBoard(log_dir=log_dir)
        # 设置 early stop
        es = EarlyStopping(monitor=es_monitor, mode='min',
                           verbose=1, patience=200)
        mc = ModelCheckpoint(self.model_name, monitor=mc_monitor,
                             mode='max', verbose=1, save_best_only=True)
        self.callbacks = [tb, mc]

    def train(self, data_package, label_data):
        X_train, y_train, X_val, y_val, X_test, y_test = data_package
        L_train, L_val, L_test = label_data
        model = self.model if self.use_lcm else self.basic_model
        history = model.fit([X_train, L_train], y_train,
                            batch_size=self.batch_size, verbose=1, epochs=self.epochs, validation_data=([X_val, L_val], y_val), callbacks=self.callbacks)
        # 在最好的模型上验证
        loss, metrics = lcm_metrics(self.num_classes, self.alpha)
        saved_model = load_model(self.model_name, custom_objects={
            "K": K,
            "precision_1k": precision_1k,
            "precision_3k": precision_3k,
            "recall_1k": recall_1k,
            "recall_3k": recall_3k,
            "F1_1k": F1_1k,
            "F1_3k": F1_3k,
            "lcm_loss": loss,
            "lcm_precision_1k": metrics[0],
            "lcm_precision_3k": metrics[1],
            "lcm_recall_1k": metrics[2],
            "lcm_recall_3k": metrics[3],
            "lcm_f1_1k": metrics[4],
            "lcm_f1_3k": metrics[5],
        })
        train_result = saved_model.evaluate([X_train, L_train], y_train)
        val_result = saved_model.evaluate([X_val, L_val], y_val)
        test_result = saved_model.evaluate([X_test, L_test], y_test)
        print("Best model evaluate=======>")
        print("train: ", train_result)
        print("val: ", val_result)
        print("test: ", test_result)
        pyplot.plot(history.history['loss'], label='train')
        pyplot.plot(history.history['val_loss'], label='test')
        pyplot.legend()
        pyplot

    def __get_saved_model_name(self, ):
        if self.use_lcm and self.use_att:
            return self.model_labs_h5py
        elif self.use_lcm:
            return self.model_lbs_h5py
        elif self.use_att:
            return self.model_lab_h5py
        else:
            return self.model_b_h5py

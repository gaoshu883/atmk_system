import numpy as np
import os
import keras
from keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint


from .lstm import Classifier
from .lcm import LabelConfusionModel
from .evaluation_metrics import precision_1k, precision_3k, precision_5k, recall_1k, recall_3k, recall_5k, F1_1k, F1_3k, F1_5k, lcm_metrics


class LABSModel:

    def __init__(self, config, text_embedding_matrix=None, label_emb_matrix=None, use_att=False, use_lcm=False, log_dir=None):
        self.epochs = config.epochs
        self.alpha = config.alpha
        self.num_classes = config.num_classes
        self.batch_size = config.batch_size
        self.use_att = use_att
        self.use_lcm = use_lcm
        self.model_filepath = os.path.join(
            log_dir, "model", self.__get_saved_model_name())

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
        tb = TensorBoard(log_dir=os.path.join(log_dir, "fit"))
        # 设置 early stop
        es = EarlyStopping(monitor=es_monitor, mode='min',
                           verbose=1, patience=200)
        mc = ModelCheckpoint(self.model_filepath, monitor=mc_monitor,
                             mode='max', verbose=1, save_best_only=True)
        self.callbacks = [tb, mc]

    def train(self, data_package, label_data):
        X_train, y_train, X_test, y_test = data_package
        L_train, L_test = label_data
        model = self.model if self.use_lcm else self.basic_model
        model.fit([X_train, L_train], y_train,
                  batch_size=self.batch_size, verbose=1, epochs=self.epochs, validation_data=([X_test, L_test], y_test), callbacks=self.callbacks)

    def __get_saved_model_name(self, ):
        if self.use_lcm and self.use_att:
            return "checkpoint_labs-{epoch:02d}-{val_lcm_precision_1k:.2f}.h5"
        elif self.use_lcm:
            return "checkpoint_lbs-{epoch:02d}-{val_lcm_precision_1k:.2f}.h5"
        elif self.use_att:
            return "checkpoint_lab-{epoch:02d}-{val_precision_1k:.2f}.h5"
        else:
            return "checkpoint_b-{epoch:02d}-{val_precision_1k:.2f}.h5"

import keras
from keras.models import Model
from keras.layers import Input, Dense, LSTM, Embedding
from keras.layers import Flatten, Dropout, Concatenate, Lambda, Multiply, Reshape, Dot, Bidirectional
import keras.backend as K

from .multi_label_loss import MyLoss
from .evaluation_metrics import precision_1k, precision_3k, precision_5k, Ndcg_1k, Ndcg_3k, Ndcg_5k


class LabelConfusionModel(object):
    """
    分类器
    """
    @classmethod
    def build(self, config, basic_model, text_h_state):
        maxlen = config.maxlen
        alpha = config.alpha
        wvdim = config.emb_size
        hidden_size = config.hidden_size
        num_classes = config.num_classes

        def lcm_loss(y_true, y_pred, alpha=alpha):
            pred_probs = y_pred[:, :num_classes]
            label_sim_dist = y_pred[:, num_classes:]
            simulated_y_true = K.softmax(label_sim_dist+alpha*y_true)
            loss1 = - \
                K.categorical_crossentropy(simulated_y_true, simulated_y_true)
            loss2 = K.categorical_crossentropy(simulated_y_true, pred_probs)
            return loss1+loss2

        def lcm_precision_1k(y_true, y_pred):
            pred_probs = y_pred[:, :num_classes]
            return precision_1k(y_true, pred_probs)

        def lcm_precision_3k(y_true, y_pred):
            pred_probs = y_pred[:, :num_classes]
            return precision_3k(y_true, pred_probs)

        def lcm_precision_5k(y_true, y_pred):
            pred_probs = y_pred[:, :num_classes]
            return precision_5k(y_true, pred_probs)

        def lcm_Ndcg_1k(y_true, y_pred):
            pred_probs = y_pred[:, :num_classes]
            return Ndcg_1k(y_true, pred_probs)

        def lcm_Ndcg_3k(y_true, y_pred):
            pred_probs = y_pred[:, :num_classes]
            return Ndcg_3k(y_true, pred_probs)

        def lcm_Ndcg_5k(y_true, y_pred):
            pred_probs = y_pred[:, :num_classes]
            return Ndcg_5k(y_true, pred_probs)

        label_input = Input(shape=(num_classes,), name='label_input')
        label_emb = Embedding(num_classes, wvdim, input_length=num_classes, name='label_emb1')(
            label_input)  # shape=(None, num_classes, wvdim)
        # 乘2是因为text用的BiLSTM
        label_emb = Dense(hidden_size*2, activation='tanh',
                          name='label_emb2')(label_emb)  # shape=(None, num_classes, hidden_size*2)
        # similarity part:
        # (num_classes,hidden_size*2) dot (hidden_size*2,1) --> (num_classes,1)
        text_h_state = basic_model.layers[-1].input  # 取text最后一层的输入
        doc_product = Dot(axes=(2, 1))(
            [label_emb, text_h_state])  # shape=(None, num_classes)
        # 标签模拟分布
        label_sim_dict = Dense(
            num_classes, activation='softmax', name='label_sim_dict')(doc_product)
        # concat output:
        # shape=(None, text_d+label_d)
        concat_output = Concatenate()([basic_model.outputs[0], label_sim_dict])
        # compile；
        model = Model(
            inputs=[basic_model.inputs[0], label_input], outputs=concat_output)
        model.compile(loss=lcm_loss, optimizer='adam', metrics=[
            lcm_precision_1k, lcm_precision_3k, lcm_precision_5k, lcm_Ndcg_1k, lcm_Ndcg_3k, lcm_Ndcg_5k])
        model._get_distribution_strategy = lambda: None
        return model

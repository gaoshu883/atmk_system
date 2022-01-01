import keras
from keras.models import Model
from keras.layers import Input, Dense, LSTM, Embedding
from keras.layers import Flatten,  Bidirectional

from .label_attention import attention_3d_block
from .multi_label_loss import MyLoss
from .evaluation_metrics import precision_1k, precision_3k, precision_5k, Ndcg_1k, Ndcg_3k, Ndcg_5k


class Classifier(object):
    """
    分类器
    """
    @classmethod
    def build(self, config, embedding_matrix=None, use_att=False):

        maxlen = config.maxlen
        vocab_size = config.vocab_size
        wvdim = config.emb_size
        hidden_size = config.hidden_size
        num_classes = config.num_classes

        text_input = Input(shape=(maxlen,), name='text_input')
        if embedding_matrix is None:
            input_emb = Embedding(
                vocab_size, wvdim, input_length=maxlen, name='text_emb')(text_input)  # (V,wvdim)
        else:
            input_emb = Embedding(vocab_size, wvdim, input_length=maxlen, weights=[
                                  embedding_matrix], trainable=False, name='text_emb')(text_input)  # (V,wvdim)
        hidden_state = Bidirectional(LSTM(hidden_size))(
            input_emb)  # shape=(None, hidden_size * 2)
        if use_att:
            hidden_state = attention_3d_block(hidden_state)
            hidden_state = Flatten()(hidden_state)
        pred_probs = Dense(num_classes, activation='softmax',
                           name='pred_probs')(hidden_state)
        model = Model(inputs=text_input, outputs=pred_probs)
        # 每一批次评估一次
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[
                           precision_1k, precision_3k, precision_5k, Ndcg_1k, Ndcg_3k, Ndcg_5k])  # 自定义评价函数
        model._get_distribution_strategy = lambda: None  # fix bug for tensorboard

        return model, hidden_state

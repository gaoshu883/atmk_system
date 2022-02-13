import numpy as np
import tensorflow as tf
import logging

# how to convert tensor to numpy
# using tf.py_function


def precision_1k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: precision_k(y_true, y_pred, 0), inp=[y_true, y_pred], Tout=tf.float32)


def precision_3k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: precision_k(y_true, y_pred, 2), inp=[y_true, y_pred], Tout=tf.float32)


def precision_5k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: precision_k(y_true, y_pred, 4), inp=[y_true, y_pred], Tout=tf.float32)


def recall_1k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: recall_k(y_true, y_pred, 0), inp=[y_true, y_pred], Tout=tf.float32)


def recall_3k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: recall_k(y_true, y_pred, 2), inp=[y_true, y_pred], Tout=tf.float32)


def recall_5k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: recall_k(y_true, y_pred, 4), inp=[y_true, y_pred], Tout=tf.float32)


def F1_1k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: F1_k(y_true, y_pred, 0), inp=[y_true, y_pred], Tout=tf.float32)


def F1_3k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: F1_k(y_true, y_pred, 2), inp=[y_true, y_pred], Tout=tf.float32)


def F1_5k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: F1_k(y_true, y_pred, 4), inp=[y_true, y_pred], Tout=tf.float32)


def Ndcg_1k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: Ndcg_k(y_true, y_pred, 0), inp=[y_true, y_pred], Tout=tf.float32)


def Ndcg_3k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: Ndcg_k(y_true, y_pred, 2), inp=[y_true, y_pred], Tout=tf.float32)


def Ndcg_5k(y_true, y_pred):
    return tf.py_function(func=lambda y_true, y_pred: Ndcg_k(y_true, y_pred, 4), inp=[y_true, y_pred], Tout=tf.float32)


def my_evaluator(y_true, y_pred):
    logging.info("precision@1 : %.4f , precision@3 : %.4f , precision@5 : %.4f " %
                 (precision_1k(y_true, y_pred), precision_3k(y_true, y_pred), precision_5k(y_true, y_pred)))
    logging.info("recall@1 : %.4f , f1@3 : %.4f , f1@5 : %.4f " %
                 (recall_1k(y_true, y_pred), recall_3k(y_true, y_pred), recall_5k(y_true, y_pred)))
    logging.info("f1@1 : %.4f ,f1@3 : %.4f , f1@5 : %.4f " %
                 (F1_1k(y_true, y_pred), F1_3k(y_true, y_pred), F1_5k(y_true, y_pred)))
    logging.info("ndcg@1 : %.4f , ndcg@3 : %.4f , ndcg@5 : %.4f " %
                 (Ndcg_1k(y_true, y_pred), Ndcg_3k(y_true, y_pred), Ndcg_5k(y_true, y_pred)))


def precision_k(y_true, y_pred, k):
    '''
    Precision@k
    @param: y_true: shape=(None, None)
    @param: y_pred: shape=(None, num_classes)
    @return: (5, 1)
    '''
    top_k = 5
    # CAST YOUR TENSOR & CONVERT IT TO NUMPY ARRAY
    y_true = y_true.numpy()
    y_pred = y_pred.numpy()

    p = np.zeros((top_k, 1))
    rank_mat = np.argsort(y_pred)
    backup = np.copy(y_pred)
    for m in range(top_k):
        y_pred = np.copy(backup)
        for i in range(rank_mat.shape[0]):
            y_pred[i][rank_mat[i, :-(m + 1)]] = 0
        y_pred = np.ceil(y_pred)
        mat = np.multiply(y_pred, y_true)
        num = np.sum(mat, axis=1)
        p[m] = np.mean(num / (m + 1))
    return np.around(p, decimals=4)[k]


def recall_k(y_true, y_pred, k):
    '''
    Recall@k
    @param: y_true: shape=(None, None)
    @param: y_pred: shape=(None, num_classes)
    @return: (5, 1)
    '''
    top_k = 5
    # CAST YOUR TENSOR & CONVERT IT TO NUMPY ARRAY
    y_true = y_true.numpy()
    y_pred = y_pred.numpy()

    p = np.zeros((top_k, 1))
    rank_mat = np.argsort(y_pred)
    backup = np.copy(y_pred)
    all_num = np.sum(y_true, axis=1)  # 所有的正类
    for m in range(top_k):
        y_pred = np.copy(backup)
        for i in range(rank_mat.shape[0]):
            y_pred[i][rank_mat[i, :-(m + 1)]] = 0
        y_pred = np.ceil(y_pred)
        mat = np.multiply(y_pred, y_true)
        num = np.sum(mat, axis=1)
        p[m] = np.mean(num / all_num)
    return np.around(p, decimals=4)[k]


def F1_k(y_true, y_pred, k):
    '''
    F1@k
    @param: y_true: shape=(None, None)
    @param: y_pred: shape=(None, num_classes)
    @return: (5, 1)
    '''
    p_k = precision_k(y_true, y_pred, k)
    r_k = recall_k(y_true, y_pred, k)
    return (2 * p_k * r_k) / (p_k + r_k)


def Ndcg_k(y_true, y_pred, k):
    '''
    自定义评价指标
    @param: y_true: shape=(None, None)
    @param: y_pred: shape=(None, num_classes)
    @return: (5, 1)
    '''
    top_k = 5
    # CAST YOUR TENSOR & CONVERT IT TO NUMPY ARRAY
    y_true = y_true.numpy()
    y_pred = y_pred.numpy()

    res = np.zeros((top_k, 1))
    rank_mat = np.argsort(y_pred)
    label_count = np.sum(y_true, axis=1)

    for m in range(top_k):
        y_mat = np.copy(y_true)
        for i in range(rank_mat.shape[0]):
            y_mat[i][rank_mat[i, :-(m + 1)]] = 0
            for j in range(m + 1):
                y_mat[i][rank_mat[i, -(j + 1)]] /= np.log(j + 1 + 1)

        dcg = np.sum(y_mat, axis=1)
        factor = get_factor(label_count, m + 1)
        ndcg = np.mean(dcg / factor)
        res[m] = ndcg
    return np.around(res, decimals=4)[k]


def get_factor(label_count, k):
    res = []
    for i in range(len(label_count)):
        n = int(min(label_count[i], k))
        f = 0.0
        for j in range(1, n+1):
            f += 1/np.log(j+1)
        res.append(f)
    return np.array(res)

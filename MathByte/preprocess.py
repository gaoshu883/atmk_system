import pickle
import h5py
import random
import numpy as np


class DataPreprocess:
    def __init__(self, token_type, dataset_path, cache_path_h5py, cache_path_pickle) -> None:
        data_f_pickle = open(dataset_path, 'rb')
        self.data_object = pickle.load(data_f_pickle)
        data_f_pickle.close()
        self.token_type = token_type
        self.cache_path_h5py = cache_path_h5py
        self.cache_path_pickle = cache_path_pickle
        self.word2index, self.label2index = self.create_vocab_label2index()
        self.label_size = len(self.label2index)
        self.max_sentence_length = 100

        # step 1: get (X,y)
        X, Y = self.get_X_Y()
        # step 2. shuffle, split,
        xy = list(zip(X, Y))
        random.shuffle(xy)
        X, Y = zip(*xy)
        X = np.array(X)
        Y = np.array(Y)
        num_examples = len(X)
        num_train = int(num_examples*0.6)
        num_valid = int(num_examples*0.15)
        train_X, train_Y = X[0:num_train], Y[0:num_train]
        vaild_X, valid_Y = X[num_train:num_train +
                             num_valid], Y[num_train:num_train+num_valid]
        test_X, test_Y = X[num_train+num_valid:], Y[num_train+num_valid:]

        # step 3: save to file system
        self.save_data(train_X, train_Y, vaild_X, valid_Y, test_X, test_Y)

    def create_vocab_label2index(self, ):
        '''
        从数据集中创建词表、标签表
        '''
        word2index = {}
        label2index = {}  # 实际上是 label_id to index
        vocab_list = []
        vocab_list.extend(['PAD', 'UNK'])
        label_set = set()
        for u in self.data_object:
            if self.token_type == 'char':
                vocab_list.extend(u['char_list'])
            else:
                vocab_list.extend(u['word_list'])
            vocab_list.extend(u['formulas'].values())
            label_set.update(u['label_list'])

        for i, item in enumerate(set(vocab_list)):
            word2index[item] = i
        for i, item in enumerate(label_set):
            label2index[item] = i
        return word2index, label2index

    def transform_multilabel_as_multihot(self, label_list, ):
        """
        convert to multi-hot style
        :param label_list: e.g.[0,1,4], here 4 means in the 4th position it is true value(as indicate by'1')
        :return:e.g.[1,1,0,1,0,0,........]
        """
        result = np.zeros(self.label_size)
        # set those location as 1, all else place as 0.
        result[label_list] = 1
        return result

    def get_X_Y(self, ):
        """
        get X and Y given input and labels
        """
        X = []
        Y = []
        PAD_ID = self.word2index.get('PAD')
        UNK_ID = self.word2index.get('UNK')
        pad_size = self.max_sentence_length

        for u in self.data_object:
            if self.token_type == 'char':
                token_list = u['char_formula_list']
            else:
                token_list = u['word_formula_list']
            formulas = u['formulas']
            content_id_list = []
            for x in token_list:
                vocab = x
                if x in formulas:
                    vocab = formulas[x]  # mathml
                content_id_list.append(self.word2index.get(
                    vocab, UNK_ID))
            # pad and truncate X to a max_sequence_length
            if len(content_id_list) < pad_size:
                content_id_list.extend(
                    [PAD_ID] * (pad_size - len(content_id_list)))
            else:
                content_id_list = content_id_list[:pad_size]
            X.append(content_id_list)

            label_list_dense = [self.label2index[l]
                                for l in u['label_list']]
            label_list_sparse = self.transform_multilabel_as_multihot(
                label_list_dense)
            Y.append(label_list_sparse)
        return X, Y

    def save_data(self, train_X, train_Y, vaild_X, valid_Y, test_X, test_Y):
        # train/valid/test data using h5py
        f = h5py.File(self.cache_path_h5py, 'w')
        f['train_X'] = train_X
        f['train_Y'] = train_Y
        f['vaild_X'] = vaild_X
        f['valid_Y'] = valid_Y
        f['test_X'] = test_X
        f['test_Y'] = test_Y
        f.close()
        # save word2index, label2index
        with open(self.cache_path_pickle, 'wb') as target_file:
            pickle.dump((self.word2index, self.label2index), target_file)

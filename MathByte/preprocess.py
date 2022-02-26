import pickle
import h5py
import random
import numpy as np

from .embeddings import Embeddings


class DataPreprocess:
    def __init__(self, token_type='char', text_version='atmk', formula_version='atmk', dataset_path=None, cache_file_h5py=None, cache_file_pickle=None, cache_embedding_file=None) -> None:
        self.cache_file_h5py = cache_file_h5py  # 数据存储路径
        self.cache_file_pickle = cache_file_pickle  # 词典存储路径
        self.cache_embedding_file = cache_embedding_file  # 预训练向量存储路径
        self.token_type = token_type
        self.text_version = text_version
        self.formula_version = formula_version

        # 读取原始数据
        data_f_pickle = open(dataset_path, 'rb')
        self.data_object = pickle.load(data_f_pickle)
        data_f_pickle.close()

    def run_task(self, ):
        '''处理全流程'''
        self.word2index, self.label2index, _ = self.create_vocab_label2index()
        self.embeddings = self.create_embeddings()
        self.label_size = len(self.label2index)
        self.max_sentence_length = 100

        # step 1: get (X,y)
        X, Y = self.get_X_Y()
        # step 2. shuffle, split,
        xy = list(zip(X, Y))
        random.Random(10000).shuffle(xy)
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
        word2index = {'<pad>': 0, '<unk>': 1}
        label2index = {}  # 实际上是 label_id to index {120:1}
        labels = []
        vocab_list = []
        for u in self.data_object:
            vocab_list.extend(
                u['char_list'] if self.token_type == 'char' else u['word_list'])
            vocab_list.extend(list(map(self.__stringify_formula_tuples,
                                       u['formula_tuples'].values())))
            labels.extend(u['label_list'])

        target_object = open(
            'create_vocab_label.log', 'a', encoding='utf-8')
        i = 2

        for word, count in self.word_count(vocab_list).items():
            # !!仅统计词频大于1的词
            if count > 1:
                if word not in word2index:
                    word2index[word] = i
                    target_object.write(word + '\n')
                    i += 1
        j = 0
        for label_id in labels:
            if label_id not in label2index:
                label2index[label_id] = j
                target_object.write(str(label_id) + '\n')
                j += 1
        target_object.close()

        return word2index, label2index, vocab_list

    def word_count(self, vocab_list):
        '''统计词频'''
        counts_word_dict = dict()
        for v in vocab_list:
            if v not in counts_word_dict:
                counts_word_dict[v] = 1
            else:
                counts_word_dict[v] += 1
        return counts_word_dict

    def create_embeddings(self, ):
        '''
        创建预训练向量
        根据词表进行创建，并且与词表一一对应
        找不到的词向量就随机初始化
        '''
        emb_size = 300
        vocab_size = len(self.word2index)
        system = Embeddings()
        word_ret = {}
        formula_ret = {}
        for vocab, i in self.word2index.items():
            if self.__is_formula(vocab):
                formula_ret[i] = self.__parse_formula_tuples(vocab)
            else:
                word_ret[i] = vocab

        index2vec_dict = {}
        index2vec_dict.update(system.batch_read_text_vec(
            word_ret, self.token_type, self.text_version))
        index2vec_dict.update(
            system.batch_read_formula_vec(formula_ret, self.formula_version))
        word_embedding_2dlist = [[]] * vocab_size
        word_embedding_2dlist[0] = np.zeros(emb_size)  # '<pad>'
        bound = np.sqrt(6.0) / np.sqrt(vocab_size)
        for idx, emb in index2vec_dict.items():
            if idx != 0:  # not <pad>
                word_embedding_2dlist[idx] = emb if emb is not None else np.random.uniform(
                    -bound, bound, emb_size)
        word_embedding_final = np.array(word_embedding_2dlist)
        target_object = open(
            'create_vocab_label.log', 'a', encoding='utf-8')
        target_object.write(str(word_embedding_final) + '\n')
        target_object.close()
        return word_embedding_final

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
        PAD_ID = self.word2index.get('<pad>')
        UNK_ID = self.word2index.get('<unk>')
        pad_size = self.max_sentence_length

        for u in self.data_object:
            token_list = u['char_formula_list'] if self.token_type == 'char' else u['word_formula_list']
            formulas = u['formula_tuples']
            content_id_list = []
            for x in token_list:
                vocab = x if x not in formulas else self.__stringify_formula_tuples(
                    formulas[x])
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
        f = h5py.File(self.cache_file_h5py, 'w')
        f['train_X'] = train_X
        f['train_Y'] = train_Y
        f['vaild_X'] = vaild_X
        f['valid_Y'] = valid_Y
        f['test_X'] = test_X
        f['test_Y'] = test_Y
        f.close()
        # save word2index, label2index
        with open(self.cache_file_pickle, 'wb') as target_file:
            pickle.dump((self.word2index, self.label2index), target_file)
        # save embeddings
        with open(self.cache_embedding_file, 'wb') as target_file:
            pickle.dump(self.embeddings, target_file)

    def __is_formula(self, vocab):
        '''是否为公式词汇'''
        return vocab.startswith('[F]')

    def __stringify_formula_tuples(self, formulas: list):
        '''把formula tuples列表格式化为字符串'''
        return '[F]' + '⌘'.join(formulas)

    def __parse_formula_tuples(self, f_str):
        '''把stringify格式化后的字符串解析成formula tuples列表'''
        return f_str[3:].split('⌘')

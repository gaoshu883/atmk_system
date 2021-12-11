from gensim.models import Word2Vec, KeyedVectors

from formula_embedding.tangent_cft_back_end import TangentCFTBackEnd

import logging
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Embeddings:
    def __init__(self, ) -> None:
        pass

    def read_text_vec(self, type_id, query, version='atmk'):
        '''
        获取字or词的向量
        :param type_id: 向量类型 char | word
        :param query: 字符或词语
        :param version: 使用的中文词向量版本 atmk | baidu
        :return: 向量
        '''
        if version == 'baidu':
            model_file_path = 'file_data/sgns.target.word-character.char1-2.dynwin5.thr10.neg5.dim300.iter5'
            print('start load model...')
            math_word2vec_model = KeyedVectors.load_word2vec_format(
                model_file_path, binary=False)
            text_vec = math_word2vec_model.wv[query]
            return text_vec
        else:
            model_file_path = 'file_data/math_text_char.model'
            if type_id == 'word':
                model_file_path = 'file_data/math_text_word.model'
            math_word2vec_model = Word2Vec.load(model_file_path)
            text_vec = math_word2vec_model.wv[query]
            return text_vec

    def read_formula_vec(self, query_formula, version='atmk'):
        '''
        获取公式向量
        :param query_formula: 公式
        :param version: 使用的词向量版本 atmk | wiki
        :return: 公式向量
        '''
        model_file_path = 'file_data/da-20k/slt_model'  # Model file path
        map_file_path = 'file_data/da-20k/slt_encoder.tsv'
        if version == 'wiki':
            model_file_path = 'file_data/wiki-590k/slt_model'
            map_file_path = 'file_data/wiki-590k/slt_encoder.tsv'

        key = 'hello_world'
        query_formulas = [{
            'key': key,
            'content': query_formula
        }]
        print(model_file_path, map_file_path)
        system = TangentCFTBackEnd(
            config_file=None, data_set=None, query_formulas=query_formulas)
        system.load_model(map_file_path=map_file_path,
                          model_file_path=model_file_path)
        formula_vec = system.get_collection_query_vectors()[key]
        return formula_vec

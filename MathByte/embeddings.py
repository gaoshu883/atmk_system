from gensim.models import Word2Vec

from formula_embedding.tangent_cft_back_end import TangentCFTBackEnd


class Embeddings:
    def __init__(self, ) -> None:
        pass

    def read_char_vec(self, query_char):
        math_word2vec_char_model = Word2Vec.load(
            'file_data/math_text_char.model')
        char_vec = math_word2vec_char_model.wv[query_char]
        return char_vec

    def read_formula_vec(self, query_formula):
        model_file_path = 'file_data/da-20k/slt_model'  # Model file path
        map_file_path = 'file_data/da-20k/slt_encoder.tsv'
        key = 'hello_world'
        query_formulas = [{
            'key': key,
            'content': query_formula
        }]
        system = TangentCFTBackEnd(
            config_file=None, data_set=None, query_formulas=query_formulas)
        system.load_model(map_file_path=map_file_path,
                          model_file_path=model_file_path)
        formula_vec = system.get_collection_query_vectors()[key]
        return formula_vec

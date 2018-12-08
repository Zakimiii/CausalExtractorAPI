# -*- coding: utf-8 -*-
import gensim
import MeCab
import numpy as np


class WordEmbeddings(object):

    def __init__(self):
        self._model = None

    def train_word_embeddings(self, sentences, save_path, **params):  # paramsが空だとエラーが起きるっぽい
        model = gensim.models.Word2Vec(sentences, **params)
        model.save(save_path)
        self._model = model

    def load_word_embeddings(self, path):
        model = gensim.models.word2vec.Word2Vec.load(path)
        self._model = model

    def get_word_vector(self, term):
        try:
            vector = self._model.wv[term]
        except KeyError:
            raise KeyError("Term doesn't exists.")
        return vector

    # テキストのベクトルを計算
    def get_vector(self, text):
        mt = MeCab.Tagger('')
        mt.parse('')
        sum_vec = np.zeros(9999)
        word_count = 0
        node = mt.parseToNode(text)
        while node:
            fields = node.feature.split(",")
            # 限定
            if fields[0] == '名詞' or fields[0] == '動詞' or fields[0] == '形容詞' or fields[0] == '助詞' or fields[0] == '助動詞':
                sum_vec += self._model.wv[node.surface]
                word_count += 1
            node = node.next

        return sum_vec / word_count

    # cos類似度を計算
    def cos_sim(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

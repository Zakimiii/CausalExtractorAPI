import math
import numpy as np
import collections


class causal_rank:
    def lex_rank(self, sentences, n=0, t=0):
        if sentences == None or sentences == []:
            return None
        n = len(sentences) if n == 0 else n
        """
        LexRankで文章を要約する．
        @param  sentences: list
            文章([[w1,w2,w3],[w1,w3,w4,w5],..]のような文リスト)
        @param  n: int
            文章に含まれる文の数
        @param  t: float
            コサイン類似度の閾値(default 0.1)
        @return : list
            LexRank
        """
        cosine_matrix = numpy.zeros((n, n))
        degrees = numpy.zeros((n,))
        l = []

        # 1. 隣接行列の作成
        for i in range(n):
            for j in range(n):
                cosine_matrix[i][j] = self.idf_modified_cosine(sentences, sentences[i], sentences[j])
                if cosine_matrix[i][j] > t:
                    cosine_matrix[i][j] = 1
                    degrees[i] += 1
                else:
                    cosine_matrix[i][j] = 0

        # 2.LexRank計算
        for i in range(n):
            for j in range(n):
                cosine_matrix[i][j] = cosine_matrix[i][j] / degrees[i]

        ratings = self.power_method(cosine_matrix, n)
        print(sentences, ratings)
        return zip(sentences, ratings)

    def idf_modified_cosine(self, sentences, sentence1, sentence2):
        """
        2文間のコサイン類似度を計算
        @param  sentence1: list
            文1([w1,w2,w3]のような単語リスト)
        @param  sentence2: list
            文2([w1,w2,w3]のような単語リスト)
        @param  sentences: list
            文章([[w1,w2,w3],[w1,w3,w4,w5],..]のような単語リスト)
        @return : float
            コサイン類似度
        """
        tf1 = self.compute_tf(sentence1)
        tf2 = self.compute_tf(sentence2)
        idf_metrics = self.compute_idf(sentences)
        return self.cosine_similarity(sentence1, sentence2, tf1, tf2, idf_metrics)

    def compute_tf(self, sentence):
        """
        TFを計算
        @param  sentence: list
            文([w1,w2,w3]のような単語リスト)
        @return : list
            TFリスト
        """
        tf_values = collections.Counter(sentence)
        tf_metrics = {}

        max_tf = self.find_tf_max(tf_values)

        for term, tf in tf_values.items():
            tf_metrics[term] = tf / max_tf

        return tf_metrics

    def find_tf_max(self, terms):
        """
        単語の最大出現頻度を探索
        @param  terms: list
            単語の出現頻度
        @return : int
            単語の最大出現頻度
        """
        return max(terms.values()) if terms else 1

    def compute_idf(self, sentences):
        """
        文章中の単語のIDF値を計算
        @param sentences: list
            文章([[w1,w2,w3],[w1,w3,w4,w5],..]のような単語リスト)
        @return: list
            IDFリスト
        """
        idf_metrics = {}
        sentences_count = len(sentences)

        for sentence in sentences:
            for term in sentence:
                if term not in idf_metrics:
                    n_j = sum(1 for s in sentences if term in s)
                    idf_metrics[term] = math.log(sentences_count / (1 + n_j))

        return idf_metrics

    def cosine_similarity(self, sentence1, sentence2, tf1, tf2, idf_metrics):
        """
        コサイン類似度を計算
        @param  sentence1: list
            文1([w1,w2,w3]のような単語リスト)
        @param  sentence2: list
            文2([w1,w2,w3]のような単語リスト)
        @param  tf1: list
            文1のTFリスト
        @param  tf2: list
            文2のTFリスト
        @param  idf_metrics: list
            文章のIDFリスト
        @return : float
            コサイン類似度
        """
        unique_words1 = set(sentence1)
        unique_words2 = set(sentence2)
        common_words = unique_words1 & unique_words2

        numerator = sum((tf1[t] * tf2[t] * idf_metrics[t] ** 2) for t in common_words)
        denominator1 = sum((tf1[t] * idf_metrics[t]) ** 2 for t in unique_words1)
        denominator2 = sum((tf2[t] * idf_metrics[t]) ** 2 for t in unique_words2)

        if denominator1 > 0 and denominator2 > 0:
            return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))
        else:
            return 0.0

    def power_method(self, cosine_matrix, n, e=0.1):
        """
        べき乗法を行なう
        @param  scosine_matrix: list
            確率行列
        @param  n: int
            文章中の文の数
        @param  e: float
            許容誤差ε
        @return: list
            LexRank
        """
        transposed_matrix = cosine_matrix.T
        sentences_count = n

        p_vector = numpy.array([1.0 / sentences_count] * sentences_count)

        lambda_val = 1.0

        while lambda_val > e:
            next_p = numpy.dot(transposed_matrix, p_vector)
            lambda_val = numpy.linalg.norm(numpy.subtract(next_p, p_vector))
            p_vector = next_p

        return p_vector

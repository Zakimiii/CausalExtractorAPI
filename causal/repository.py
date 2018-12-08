import re
import MeCab
import numpy as np
from data.ja.word_vector import WordEmbeddings
from data.scraping import googleScraping
from cabocha.analyzer import CaboChaAnalyzer
from cabocha.analyzer import EndOfLinkException
from .models import Causal, Goal, Step, PrunedUser, Smart, Relation, Pattern, Crawler
from causal.causal_rank import causal_rank
import pandas as pd
from data.ja.word_vector import WordEmbeddings
import MeCab
from gensim.models import word2vec
import numpy as np
import re
import csv
import pandas as pd
from data.scraping import googleScraping
import termextract.mecab
import termextract.core
import collections
import asyncio
import tornado.ioloop
from tornado.iostream import IOStream


class causal_repository:

    def __init__(self):
        self.save_path = "Util/causal.model"
        self.keyword = ""
        self.searcher = googleScraping.google_search
        self.scraper = googleScraping.getMainJAText

    def routineCrawle(self, init_keyword, limit=3, per_limit=20):
        keywords = []
        for i in range(limit):
            print("Epoch:" + str(i + 1))
            if i == 0:
                print("Epoch of search: init" + "\n" + "Keyword: " + init_keyword)
                crawlers = self.syncCrawle(init_keyword, limit=per_limit)
            else:
                crawlers = []
                ex_crawlers = crawlers.extend
                for index, keyword in enumerate(keywords):
                    print("Epoch of search: " + str(index + 1) + " / " + str(
                        len(keywords)) + "\n" + "Keyword: " + keyword)
                    gcrawlers = self.syncCrawle(keyword)
                    self.setCrawlerData(gcrawlers)
                    ex_crawlers(gcrawlers)
            self.setCrawlerData(crawlers)
            print("Saved " + str(len(crawlers)) + " of crawlers")
            loop = asyncio.new_event_loop()
            keywords = loop.run_until_complete(self.generateKeyword(crawlers))
            print("Generated " + str(len(keywords)) + " of keywords")
            loop.close()

    def causalToVector(self, sentences, causals, keyword):
        wordEmbedding = WordEmbeddings()
        preTexts = "".join(self.wakati(sentence) for sentence in sentences)
        preTexts = re.sub(r'\n', "", preTexts)
        texts = preTexts.split(" ")
        print(texts)
        wordEmbedding.train_word_embeddings(texts, self.save_path, sg=0, size=9999, min_count=1, max_vocab_size=None,
                                            trim_rule=None, sample=0)
        wordEmbedding.load_word_embeddings(self.save_path)

        causalSubjVecs = [wordEmbedding.get_vector(causal.subj) for causal in causals]
        causalBasisVecs = [wordEmbedding.get_vector(causal.basis) for causal in causals]
        causalResultVecs = [wordEmbedding.get_vector(causal.result) for causal in causals]
        causalClueVecs = [wordEmbedding.get_vector(causal.clue) for causal in causals]
        causalSentenceVecs = [wordEmbedding.get_vector(causal.sentence) for causal in causals]

        causalPatternVecs = [causal.pattern.toOneHot() for causal in causals]

        try:
            keywordVec = wordEmbedding.get_vector(keyword)
        except:
            keywordVec = np.zeros

        causalSubjCosSims = [wordEmbedding.cos_sim(keywordVec, subj) for subj in causalSubjVecs]
        causalBasisCosSims = [wordEmbedding.cos_sim(keywordVec, basis) for basis in causalBasisVecs]
        causalResultCosSims = [wordEmbedding.cos_sim(keywordVec, result) for result in causalResultVecs]
        causalClueCosSims = [wordEmbedding.cos_sim(keywordVec, clue) for clue in causalClueVecs]
        causalSentenceCosSims = [wordEmbedding.cos_sim(keywordVec, sentence) for sentence in causalSentenceVecs]

        [print(subj) for subj in causalSubjVecs]
        return causalSubjVecs, causalBasisVecs, causalResultVecs, causalClueVecs, causalSentenceVecs, causalPatternVecs, causalSubjCosSims, causalBasisCosSims, causalResultCosSims, causalClueCosSims, causalSentenceCosSims

    def lexRankCausal(self, causals):
        cr = causal_rank()

        #         causalSubjRanks = cr.lex_rank([self.wakatiArray(causal.subj) for causal in causals])
        causalBasisRanks = cr.lex_rank([self.wakatiArray(causal.basis) for causal in causals if causal.noneCheck()])
        causalResultRanks = cr.lex_rank([self.wakatiArray(causal.result) for causal in causals if causal.noneCheck()])
        causalClueRanks = cr.lex_rank([self.wakatiArray(causal.clue) for causal in causals if causal.noneCheck()])
        #         causalSentenceRanks = cr.lex_rank([self.wakatiArray(causal.sentence) for causal in causals if causal.noneCheck()])

        #         causalPatternRanks = [causal.pattern.toOneHot() for causal in causals if causal.noneCheck()]

        return causalBasisRanks, causalResultRanks, causalClueRanks

    def wakati(self, sentence):
        mecab = MeCab.Tagger("-Owakati")
        return mecab.parse(sentence)

    def wakatiArray(self, sentence):
        return [re.sub('\n', "", prune_sentence) for prune_sentence in self.wakati(sentence).split(" ")]

    def tokenizes(self, sentences):
        return [self.wakati(sentence) for sentence in sentences]

    def tokenize(self, sentence):
        return self.wakati(sentence)

    def syncCrawle(self, keyword, limit=10):
        crawlers = []
        ex_crawlers = crawlers.extend
        loop = asyncio.new_event_loop()
        gcrawlers = loop.run_until_complete(self.routeCrawle(keyword, limit=limit))
        loop.close()
        ex_crawlers(gcrawlers)
        return crawlers

    @asyncio.coroutine
    async def generateCrawlerFromURL(self, url, keyword):
        await asyncio.sleep(1)
        text = self.scraper(url)
        crawler = Crawler()
        crawler.keyword = keyword
        crawler.url = url
        crawler.article = text
        print(url, "\n", text)
        return crawler

    @asyncio.coroutine
    async def routeCrawle(self, keyword, limit=10):
        try:
            await asyncio.sleep(1)
            urls = self.searcher(keyword)
        except:
            pass
        tasks = [self.generateCrawlerFromURL(url, keyword) for url in urls if url != ""]
        return await asyncio.gather(*tasks)

    def scraping(self, keyword):
        self.keyword = keyword
        crawlers = []
        try:
            urls = self.searcher(keyword)
        except:
            pass
        for url in urls:
            if url == "":
                break
            try:
                text = self.scraper(url)
                crawler = Crawler()
                crawler.keyword = keyword
                crawler.url = url
                crawler.article = text
                print(url, "\n", text)
                crawlers.append(crawler)
            except:
                return crawlers
        return crawlers

    def generateTerm(self, crawler, limit=5):
        parser = MeCab.Tagger()
        join = "".join
        sentence = join(article for i, article in enumerate(crawler.article) if i < 100)
        analyzed = parser.parse(sentence)
        frequency = termextract.mecab.cmp_noun_dict(analyzed)
        LR = termextract.core.score_lr(frequency,
                                       ignore_words=termextract.mecab.IGNORE_WORDS,
                                       lr_mode=1, average_rate=1
                                       )
        term_imp = termextract.core.term_importance(frequency, LR)
        data_collection = collections.Counter(term_imp)
        #         for cmp_noun, value in data_collection.most_common():
        #             print(termextract.core.modify_agglutinative_lang(cmp_noun), value, sep="\t")
        return [termextract.core.modify_agglutinative_lang(cmp_noun) for cmp_noun, value in
                data_collection.most_common()][:limit]

    def termExtract(self, crawlers):
        values = []
        [values.extend(self.generateTerm(crawler)) for crawler in crawlers]
        return values

    @asyncio.coroutine
    async def generateKeyword(self, crawlers):
        save_keywords = pd.read_csv('Util/crawlers_data.csv')['Keyword']
        await asyncio.sleep(1)
        values = list(set(self.termExtract(crawlers)))
        keywords = []
        for value in values:
            keywords.append(value + " " + Relation.cause.toJaKeyword())
            keywords.append(value + " " + Relation.goal.toJaKeyword())
            keywords.append(value + " " + Relation.equal.toJaKeyword())
        return list(set(keywords) - (set(keywords) & set(save_keywords)))

    def setListUid(self, proparties):
        uidList = ""
        for proparty in proparties:
            uidList += proparty.uid + "," if proparty != proparties[-1] else proparty.uid
        return uidList

    def setCrawlerData(self, crawlers):
        df = pd.read_csv('Util/crawlers_data.csv')
        for crawler in crawlers:
            try:
                df = df.drop(df[df['Article'] == "".join(article + "。" for article in crawler.article)].index.tolist(),
                             axis=0)
                df = df.append(pd.Series(
                    [crawler.uid, crawler.keyword, crawler.url, "".join(article + "。" for article in crawler.article),
                     self.setListUid(crawler.causals), crawler.createdAt, crawler.updatedAt], index=df.columns),
                               ignore_index=True)
            except:
                df = df.append(pd.Series(
                    [crawler.uid, crawler.keyword, crawler.url, crawler.article, self.setListUid(crawler.causals),
                     crawler.createdAt, crawler.updatedAt], index=df.columns), ignore_index=True)
        df.to_csv('Util/crawlers_data.csv', index=None)

    def setCausalData(self, causals, crawlers):
        df = pd.read_csv('Util/causal_train_data.csv')
        self.setCrawlerData(crawlers)
        for causal in causals:
            if causal.noneCheck():
                try:
                    df = df.drop(df[df['Uid'] == causal.uid].index.tolist(), axis=0)
                    df = df.append(pd.Series(
                        [causal.uid, 1, causal.basis, causal.result, causal.subj, causal.pattern.toJson(), causal.clue,
                         causal.filePath, causal.line, causal.causalId, causal.sentence, causal.relation.toJson(),
                         causal.createdAt, causal.updatedAt, self.keyword], index=df.columns), ignore_index=True)
                except:
                    df = df.append(pd.Series(
                        [causal.uid, 1, causal.basis, causal.result, causal.subj, causal.pattern.toJson(), causal.clue,
                         causal.filePath, causal.line, causal.causalId, causal.sentence, causal.relation.toJson(),
                         causal.createdAt, causal.updatedAt, self.keyword], index=df.columns), ignore_index=True)
        df.to_csv('Util/causal_train_data2.csv', index=None)

    def analyzeCausals(self, causals):
        analyzer = CaboChaAnalyzer()
        num = np.zeros(len(causals))
        numB = np.zeros(len(causals))
        numR = np.zeros(len(causals))
        for i, causal in enumerate(causals):
            num[i] = analyzer.parse(causal.sentence).chunk_size
            numB[i] = analyzer.parse(causal.basis).chunk_size
            numR[i] = analyzer.parse(causal.result).chunk_size
        print(
        "sentence_avarage", np.average(num), "basis_avarage", np.average(numB), "result_avarage", np.average(numR))

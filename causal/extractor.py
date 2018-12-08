import re
from .models import Causal, Goal, Step, PrunedUser, Smart, Relation, Pattern, Crawler
from cabocha.analyzer import CaboChaAnalyzer
from cabocha.analyzer import EndOfLinkException
from enum import Enum
from datetime import datetime
import pandas as pd
import collections
import asyncio
import tornado.ioloop
from tornado.iostream import IOStream


class extractor:
    pMeasurableKakujosi = re.compile('から$|より$')

    clueList = []

    eclueList = []

    gclueList = []

    geclueList = []

    eqclueList = []

    eqeclueList = []

    demonList = []

    skipList = []

    clueBFilterList = []

    eclueBFilterList = []

    gclueBFilterList = []

    geclueBFilterList = []

    eqclueBFilterList = []

    eqeclueBFilterList = []

    clueRFilterList = []

    eclueRFilterList = []

    gclueRFilterList = []

    geclueRFilterList = []

    eqclueRFilterList = []

    eqeclueRFilterList = []

    cluePosList = []

    gcluePosList = []

    eqcluePosList = []

    cluePos1List = []

    gcluePos1List = []

    eqcluePos1List = []

    skipList = []

    @staticmethod
    def getTextFromChunks(tree):
        text = ""
        for chunk in tree:
            text += chunk.surface
        return text

    @staticmethod
    def getTextFromTokens(chunk):
        text = ""
        for token in chunk:
            text += token.surface
        return text

    @staticmethod
    def causalUniqueSentence(causals):
        duplicatedIndex = []
        df = pd.DataFrame()
        df['sentence'] = [causal.sentence for causal in causals if causal.noneCheck()]
        df['causal'] = [causal for causal in causals if causal.noneCheck()]
        [duplicatedIndex.append(df[df['sentence'] == causal.sentence].index.tolist()) for causal in causals if
         causal.noneCheck()]
        for indexes in duplicatedIndex:
            for i, index in enumerate(indexes):
                if i > 0:
                    try:
                        df = df.drop(index, axis=0)
                    except:
                        break
        return [item['causal'] for index, item in df.iterrows()]

    def __init__(self):
        self.utilSet()

    def utilSet(self):

        self.skipList = pd.read_csv("Util/ja_skip_list.csv").dropna(subset=['clue'])['clue']

        self.clueList = pd.read_csv("Util/ja_clue_list.csv").dropna(subset=['clue'])['clue']
        self.eclueList = pd.read_csv("Util/ja_eclue_list.csv").dropna(subset=['clue'])['clue']
        self.gclueList = pd.read_csv("Util/ja_goal_clue_list.csv").dropna(subset=['clue'])['clue']
        self.geclueList = pd.read_csv("Util/ja_goal_eclue_list.csv").dropna(subset=['clue'])['clue']
        self.eqclueList = pd.read_csv("Util/ja_equal_clue_list.csv").dropna(subset=['clue'])['clue']
        self.eqeclueList = pd.read_csv("Util/ja_equal_eclue_list.csv").dropna(subset=['clue'])['clue']

        self.cluePosList = pd.read_csv("Util/ja_clue_list.csv").dropna(subset=['clue'])["clue_pos"]
        self.gcluePosList = pd.read_csv("Util/ja_goal_clue_list.csv").dropna(subset=['clue'])["clue_pos"]
        self.eqcluePosList = pd.read_csv("Util/ja_equal_clue_list.csv").dropna(subset=['clue'])["clue_pos"]
        self.cluePos1List = pd.read_csv("Util/ja_clue_list.csv").dropna(subset=['clue'])["clue_pos1"]
        self.gcluePos1List = pd.read_csv("Util/ja_goal_clue_list.csv").dropna(subset=['clue'])["clue_pos1"]
        self.eqcluePos1List = pd.read_csv("Util/ja_equal_clue_list.csv").dropna(subset=['clue'])["clue_pos1"]

        self.clueBFilterList = pd.read_csv("Util/ja_clue_list.csv").dropna(subset=['clue'])['basis_pos']
        #         self.eclueBFilterList = pd.read_csv("Util/ja_eclue_list.csv").dropna(subset=['clue'])['basis_pos']
        self.gclueBFilterList = pd.read_csv("Util/ja_goal_clue_list.csv").dropna(subset=['clue'])['basis_pos']
        #         self.geclueBFilterList = pd.read_csv("Util/ja_goal_eclue_list.csv").dropna(subset=['clue'])['basis_pos']
        self.eqclueBFilterList = pd.read_csv("Util/ja_equal_clue_list.csv").dropna(subset=['clue'])['basis_pos']

    #         self.eqeclueBFilterList = pd.read_csv("Util/ja_equal_eclue_list.csv").dropna(subset=['clue'])['basis_pos']

    #         self.clueRFilterList = pd.read_csv("Util/ja_clue_list.csv").dropna(subset=['clue'])['result_pos']
    # #         self.eclueRFilterList = pd.read_csv("Util/ja_eclue_list.csv").dropna(subset=['clue'])['result_pos']
    #         self.gclueRFilterList = pd.read_csv("Util/ja_goal_clue_list.csv").dropna(subset=['clue'])['result_pos']
    # #         self.geclueRFilterList = pd.read_csv("Util/ja_goal_eclue_list.csv").dropna(subset=['clue'])['result_pos']
    #         self.eqclueRFilterList = pd.read_csv("Util/ja_equal_clue_list.csv").dropna(subset=['clue'])['result_pos']
    # #         self.eqeclueRFilterList = pd.read_csv("Util/ja_equal_eclue_list.csv").dropna(subset=['clue'])['result_pos']

    def checkSkip(self, causal, skipList):
        return any([skip in causal.sentence for skip in skipList])

    def checkResult(self, causals):
        [causals.remove(causal) for causal in causals if causal == None]
        reslutCausals = []
        try:
            [[reslutCausals.append(causal2) for causal2 in causals if all(
                [causal1.sentence == causal2.sentence,
                 causal2.clue.pattern == Pattern.A or causal2.clue.pattern == Pattern.B,
                 causal1.clue.pattern == Pattern.C or causal1.clue.pattern == Pattern.D])] for causal1 in causals]
        except AttributeError:
            pass
        return reslutCausals

    # todo:以上以下とかもここでやる
    def checkPronoun(self, causal):
        analyzer = CaboChaAnalyzer()
        basis_tree = analyzer.parse(re.sub("、", "", causal.basis))
        for chunk in basis_tree:
            for token in chunk:
                if token.pos == "名詞" and token.pos1 == "代名詞":
                    return True
                elif token.pos == "連体詞" and re.match(r'こ|そ|あ|ど', token.surface):
                    return True
                elif token.pos == "副詞" and token.pos1 == "助詞類接続" and re.match(r'^こ|そ|あ|ど', token.surface):
                    return True
                elif token.surface == "これ" or token.surface == "それ" or token.surface == "あれ" or token.surface == "どれ" or token.surface == "こう" or token.surface == "そう" or token.surface == "そちら" or token.surface == "こちら" or token.surface == "あちら":
                    return True
        return False

    def checkCausalSize(self, causal, avarage=14):
        analyzer = CaboChaAnalyzer()
        return any([analyzer.parse(causal.sentence).chunk_size > avarage,
                    analyzer.parse(causal.basis).chunk_size > avarage / 2,
                    analyzer.parse(causal.result).chunk_size > avarage / 2])

    def checkECausalSize(self, causal, avarage=14):
        analyzer = CaboChaAnalyzer()
        return any([analyzer.parse(causal.basis).chunk_size > avarage / 2,
                    analyzer.parse(causal.result).chunk_size > avarage / 2])

    def causalUnique(self, causals):
        causals = list(set(causals))
        [causals.remove(causal) for causal in causals if causal == None]
        try:
            [[causals.remove(causal2) for causal2 in causals if
              all([causal1.sentence == causal2.sentence, causal2.clue in causal1.clue, causal2.clue != causal1.clue])]
             for causal1 in causals]
        except AttributeError:
            pass
        return causals

    def causalFilter(self, causals, basis_list, result_list):
        analyzer = CaboChaAnalyzer()
        newCausals = []
        for causal in causals:
            if causal.pattern != Pattern.E:
                tree = analyzer.parse(re.sub("、", "", causal.basis))
                try:
                    chunk = tree[tree.chunk_size - 1] if tree.chunk_size > 0 else tree[0]
                    if any([chunk[chunk.token_size - 1].pos == str(basis_list[causal.causalId]) and str(
                            basis_list[causal.causalId]) != "nan",
                            str(basis_list[causal.causalId]) == "nan"]) and not self.checkPronoun(
                            causal) and not self.checkCausalSize(
                            causal) and tree.chunk_size > 2:  # and not re.search(r'www|html|http|jpg|png|jpeg|com', causal.sentence) and not re.search(r'www|html|http|jpg|png|jpeg|com', causal.basis):
                        newCausals.append(causal)
                except IndexError:
                    pass
            if causal.pattern == Pattern.E and not self.checkPronoun(causal) and not self.checkECausalSize(
                    causal):  # and not re.search(r'www|html|http|jpg|png|jpeg|com', causal.sentence) and not re.search(r'www|html|http|jpg|png|jpeg|com', causal.basis):
                newCausals.append(causal)
        return newCausals

    def checkCorePos(self, causal, cluePosList, cluePos1List):
        if causal.pattern == Pattern.E:
            return True
        if str(cluePosList[causal.causalId]) == "nan":
            return True
        if str(cluePos1List[causal.causalId]) == "nan":
            clue_pos1 = []
        clue_pos = str(cluePosList[causal.causalId]).split(",")
        clue_pos1 = str(cluePos1List[causal.causalId]).split(",")
        analyzer = CaboChaAnalyzer()
        tree = analyzer.parse(causal.sentence)
        check_token = []
        for chunk in tree:
            if causal.clue in chunk.surface:
                [check_token.append(token) for token in chunk if token.surface in causal.clue]
                if "".join(token.surface for token in check_token) == causal.clue:
                    break
        for index, token in enumerate(check_token):
            if token.pos == clue_pos[index]:
                if clue_pos1 == []:
                    return True
                elif clue_pos1[index] == "" or clue_pos1[index] == None:
                    break
                elif token.pos1 == clue_pos1[index]:
                    return True
                else:
                    return False
            else:
                return False

    def checkKindSentence(self, separateChunks, skipChunk=None):
        subj = ""
        text = ""
        for chunks in separateChunks:
            lastChunk = chunks[len(chunks) - 1]
            lastToken = lastChunk[lastChunk.token_size - 1]
            if skipChunk != None and skipChunk in chunks:
                break
            if lastToken.pos == "記号":
                lastToken = lastChunk[lastChunk.token_size - 2]
            # 逆説
            if lastToken.pos == "助詞" and lastToken.pos1 == "接続助詞" and lastToken.surface == "が":
                separateChunks.remove(chunks)
            # 主節
            elif lastToken.pos == "助詞" and lastToken.pos1 == "格助詞":
                subj = extractor.getTextFromChunks(chunks)
            elif lastToken.pos == "助詞" and lastToken.pos1 == "係助詞" and lastToken.surface == "も":
                separateChunks.remove(chunks)
        #             elif lastToken.pos == "助動詞":
        #                 separateChunks.remove(chunks)
        for chunks in separateChunks:
            text += extractor.getTextFromChunks(chunks)
        return text, subj

    def getCoreIds(self, tree, clue):
        ids = []
        [ids.append(chunk.id) for chunk in tree if clue in chunk.surface or clue in chunk.surface + "。"]
        return ids

    def replaceCoreChunk(self, coreChunk, clue):
        return coreChunk.surface.strip(clue)

    def getSeparateChunk(self, tree):
        ids = []
        chunks = []
        [ids.append(chunk.id) for chunk in tree[tree.chunk_size - 1].prev_links]
        ids.sort()
        for index, chunkId in enumerate(ids):
            if chunkId == min(ids):
                chunks.append(tree[:chunkId + 1])
            elif chunkId == max(ids):
                chunks.append(tree[ids[index - 1] + 1:chunkId + 1])
            else:
                chunks.append(tree[ids[index - 1] + 1: chunkId + 1])
        chunks.append([tree[tree.chunk_size - 1]])
        return chunks

    def getResult(self, chunks):
        text = extractor.getTextFromTokens(chunks)
        text = re.sub(r'^といって', "", text)
        text = re.sub(r'^ため', "", text)
        text = re.sub(r'^だこそ', "", text)
        text = re.sub(r'^こそ', "", text)
        text = re.sub(r'^ですの', "", text)
        text = re.sub(r'^です', "", text)
        text = re.sub(r'^だ', "", text)
        text = re.sub(r'^の', "", text)
        if not re.match("なん", text):
            text = re.sub(r'^な', "", text)
        text = re.sub(r'^、', "", text)
        return text

    def getBasis(self, chunks, clue_basis=""):
        remover = ""
        try:
            for token in chunks[0]:
                if token.surface != "少し" or token.pos == "接続詞" or all(
                        [token.pos == "副詞", token.pos1 == "助詞類接続"]) or all([token.pos == "名詞", token.pos1 == "数"]):
                    remover += token.surface
                elif chunks[0].surface == "逆に" or chunks[0].surface == "逆に、" or chunks[0].surface == "反対に" or chunks[
                    0].surface == "反対に、" or chunks[0].surface == "ぜひ、" or chunks[0].surface == "ぜひ" or chunks[
                    0].surface == "是非、" or chunks[0].surface == "是非" or chunks[0].surface == "具体的" or chunks[
                    0].surface == "もちろん":
                    remover = chunks[0].surface
        except:
            pass
        text = extractor.getTextFromTokens(chunks) + clue_basis if not clue_basis in extractor.getTextFromTokens(
            chunks) else extractor.getTextFromTokens(chunks)
        text = re.sub(remover, "", text)
        text = re.sub(r'^、', "", text)
        text = re.sub(r'、$', "", text)
        return text

    def getResultFromText(self, text):
        text = re.sub(r'^といって', "", text)
        text = re.sub(r'^だこそ', "", text)
        text = re.sub(r'^こそ', "", text)
        text = re.sub(r'^ですの', "", text)
        text = re.sub(r'^です', "", text)
        text = re.sub(r'^だ', "", text)
        text = re.sub(r'^の', "", text)
        text = re.sub(r'^な', "", text)
        text = re.sub(r'^、', "", text)
        return text

    def getBasisFromText(self, text, clue_basis=""):
        analyzer = CaboChaAnalyzer()
        chunks = analyzer.parse(text)
        remover = ""
        try:
            for token in chunks[0]:
                if token.pos == "接続詞" or all([token.pos == "副詞", token.pos1 == "助詞類接続"]) or all(
                        [token.pos == "名詞", token.pos1 == "数"]):
                    remover += token.surface
                elif chunks[0].surface == "逆に" or chunks[0].surface == "逆に、" or chunks[0].surface == "反対に" or chunks[
                    0].surface == "反対に、" or chunks[0].surface == "ぜひ、" or chunks[0].surface == "ぜひ" or chunks[
                    0].surface == "是非、" or chunks[0].surface == "是非" or chunks[0].surface == "具体的" or chunks[
                    0].surface == "もちろん":
                    remover = chunks[0].surface
        except:
            pass
        text = extractor.getTextFromTokens(chunks) + clue_basis
        text = re.sub(remover, "", text)
        text = re.sub(r'^、', "", text)
        return text

    def getCausalExpression(self, tree, clue, coreId, sentence, beforeSentence, eclueList, causalId, line, relation):
        causal = Causal()
        coreChunk = tree[coreId]
        sentence, subj = self.checkKindSentence(self.getSeparateChunk(tree))
        analyzer = CaboChaAnalyzer()
        tree = analyzer.parse(sentence)
        causal.subj = subj
        causal.sentence = sentence
        causal.line = line
        causal.causalId = causalId
        causal.relation = relation
        for eclue in eclueList:
            if re.match(str(eclue), coreChunk.surface):
                causal.pattern = Pattern.E
                causal.result = self.getResultFromText(sentence.replace(clue, ""))
                causal.basis = self.getBasisFromText(beforeSentence)
                causal.sentence = beforeSentence + "。" + sentence
                causal.clue = eclue
                return causal if causal.noneCheck else None
        if not clue.endswith("。") and not coreChunk.surface.endswith(clue + "。"):
            causal.basis = self.getBasis(tree[: coreId], clue_basis=self.replaceCoreChunk(coreChunk, clue))
            causal.result = self.getResult(tree[coreId + 1: tree.chunk_size])
            causal.clue = clue
            causal.pattern = Pattern.A if causal.subj == "" else Pattern.B
            return causal if causal.noneCheck else None
        elif (coreChunk.surface + "。").endswith(clue) or all(
                [coreChunk.surface.endswith(clue), coreChunk.surface.endswith("。")]):
            if causal.subj == "":
                causal.pattern = Pattern.D
                causal.result = self.getResult(tree[:coreId])
                causal.basis = beforeSentence
                causal.sentence = beforeSentence + "。" + sentence  # todo: is it  need ??
                causal.clue = clue
            else:
                causal.pattern = Pattern.C
                chunkId = 0
                for chunk in tree:
                    if subj in chunk.surface:
                        chunkId = chunk.id
                causal.result = self.getResult(tree[chunkId + 1:coreId])
                causal.basis = subj
                causal.clue = clue
            return causal if causal.noneCheck else None
        else:
            return None

    def getInga(self, texts):
        causals = []
        for line, text in enumerate(texts):
            analyzer = CaboChaAnalyzer()
            tree = analyzer.parse(text)
            if tree.chunk_size == 0:
                break
            beforeSentence = texts[line - 1] if line > 0 else ""
            for index, clue in enumerate(self.clueList):
                causals.extend([self.getCausalExpression(tree, clue, coreId, text, beforeSentence, self.eclueList,
                                                         index, line, Relation.cause) for coreId in
                                self.getCoreIds(tree, clue)])
        [print("Before", "subj", causal.subj, "basis", causal.basis, "reslut", causal.result, causal.clue,
               causal.causalId, causal.pattern.toJson()) for causal in causals]
        causals = self.causalUnique(causals)
        causals = self.causalFilter(causals, self.clueBFilterList, self.clueRFilterList)
        causals = [causal for causal in causals if self.checkCorePos(causal, self.cluePosList, self.cluePos1List)]
        return causals

    def getGoal(self, texts):
        causals = []
        for line, text in enumerate(texts):
            analyzer = CaboChaAnalyzer()
            tree = analyzer.parse(text)
            if tree.chunk_size == 0:
                break
            beforeSentence = texts[line - 1] if line > 0 else ""
            for index, clue in enumerate(self.gclueList):
                causals.extend(
                    [self.getCausalExpression(tree, clue, coreId, text, beforeSentence, self.geclueList, index, line,
                                              Relation.goal)
                     for coreId in self.getCoreIds(tree, clue)])
        [print("Before", "subj", causal.subj, "basis", causal.basis, "reslut", causal.result, causal.clue,
               causal.causalId, causal.pattern.toJson()) for causal in causals]
        causals = self.causalUnique(causals)
        causals = self.causalFilter(causals, self.gclueBFilterList, self.gclueRFilterList)
        causals = [causal for causal in causals if self.checkCorePos(causal, self.gcluePosList, self.gcluePos1List)]
        return causals

    def getEqual(self, texts):
        causals = []
        for line, text in enumerate(texts):
            analyzer = CaboChaAnalyzer()
            tree = analyzer.parse(text)
            if tree.chunk_size == 0:
                break
            beforeSentence = texts[line - 1] if line > 0 else ""
            for index, clue in enumerate(self.eqclueList):
                causals.extend(
                    [self.getCausalExpression(tree, clue, coreId, text, beforeSentence, self.eqeclueList, index, line,
                                              Relation.equal)
                     for coreId in self.getCoreIds(tree, clue)])
        [print("Before", "subj", causal.subj, "basis", causal.basis, "reslut", causal.result, causal.clue,
               causal.causalId, causal.pattern.toJson()) for causal in causals]
        causals = self.causalUnique(causals)
        causals = self.causalFilter(causals, self.eqclueBFilterList, self.eqclueRFilterList)
        causals = [causal for causal in causals if self.checkCorePos(causal, self.eqcluePosList, self.eqcluePos1List)]
        #         causals = self.checkResult(causals)
        return causals

    @asyncio.coroutine
    async def coroutineGetInga(self, texts):
        await asyncio.sleep(1)
        try:
            causals = []
            for line, text in enumerate(texts):
                analyzer = CaboChaAnalyzer()
                tree = analyzer.parse(text)
                if tree.chunk_size == 0:
                    break
                beforeSentence = texts[line - 1] if line > 0 else ""
                for index, clue in enumerate(self.clueList):
                    causals.extend([self.getCausalExpression(tree, clue, coreId, text, beforeSentence, self.eclueList,
                                                             index, line, Relation.cause) for coreId in
                                    self.getCoreIds(tree, clue)])
            [print("Before", "subj", causal.subj, "basis", causal.basis, "reslut", causal.result, causal.clue,
                   causal.causalId, causal.pattern.toJson()) for causal in causals]
            causals = self.causalUnique(causals)
            causals = self.causalFilter(causals, self.clueBFilterList, self.clueRFilterList)
            causals = [causal for causal in causals if self.checkCorePos(causal, self.cluePosList, self.cluePos1List)]
            return causals
        except:
            return []

    @asyncio.coroutine
    async def coroutineGetGoal(self, texts):
        await asyncio.sleep(1)
        causals = []
        for line, text in enumerate(texts):
            analyzer = CaboChaAnalyzer()
            tree = analyzer.parse(text)
            if tree.chunk_size == 0:
                break
            beforeSentence = texts[line - 1] if line > 0 else ""
            for index, clue in enumerate(self.gclueList):
                causals.extend(
                    [self.getCausalExpression(tree, clue, coreId, text, beforeSentence, self.geclueList, index, line,
                                              Relation.goal)
                     for coreId in self.getCoreIds(tree, clue)])
        [print("Before", "subj", causal.subj, "basis", causal.basis, "reslut", causal.result, causal.clue,
               causal.causalId, causal.pattern.toJson()) for causal in causals]
        causals = self.causalUnique(causals)
        causals = self.causalFilter(causals, self.gclueBFilterList, self.gclueRFilterList)
        causals = [causal for causal in causals if self.checkCorePos(causal, self.gcluePosList, self.gcluePos1List)]
        return causals

    @asyncio.coroutine
    async def coroutineGetEqual(self, texts):
        await asyncio.sleep(1)
        causals = []
        for line, text in enumerate(texts):
            analyzer = CaboChaAnalyzer()
            tree = analyzer.parse(text)
            if tree.chunk_size == 0:
                break
            beforeSentence = texts[line - 1] if line > 0 else ""
            for index, clue in enumerate(self.eqclueList):
                causals.extend(
                    [self.getCausalExpression(tree, clue, coreId, text, beforeSentence, self.eqeclueList, index, line,
                                              Relation.equal)
                     for coreId in self.getCoreIds(tree, clue)])
        [print("Before", "subj", causal.subj, "basis", causal.basis, "reslut", causal.result, causal.clue,
               causal.causalId, causal.pattern.toJson()) for causal in causals]
        causals = self.causalUnique(causals)
        causals = self.causalFilter(causals, self.eqclueBFilterList, self.eqclueRFilterList)
        causals = [causal for causal in causals if self.checkCorePos(causal, self.eqcluePosList, self.eqcluePos1List)]
        #         causals = self.checkResult(causals)
        return causals

    @asyncio.coroutine
    async def coroutine(self, crawlers, relation):
        await asyncio.sleep(1)
        if relation == Relation.cause:
            tasks = [self.coroutineGetInga(crawler.article) for crawler in crawlers]
        elif relation == Relation.goal:
            tasks = [self.coroutineGetGoal(crawler.article) for crawler in crawlers]
        elif relation == Relation.equal:
            tasks = [self.coroutineGetEqual(crawler.article) for crawler in crawlers]
        return await asyncio.gather(*tasks)

    def extract(self, crawlers, relation):
        causals = []
        for crawler in crawlers:
            if relation == Relation.cause:
                ingas = self.getInga(crawler.article)
                ingas = extractor.causalUniqueSentence(ingas)
                ingas = [inga for inga in ingas if not self.checkSkip(inga, self.skipList)]
                crawler.causals = ingas
                causals.extend(ingas)
            elif relation == Relation.goal:
                goals = self.getGoal(crawler.article)
                goals = extractor.causalUniqueSentence(goals)
                goals = [goal for goal in goals if not self.checkSkip(goal, self.skipList)]
                crawler.causals = goals
                causals.extend(goals)
            elif relation == Relation.equal:
                equals = self.getEqual(crawler.article)
                equals = extractor.causalUniqueSentence(equals)
                equals = [equal for equal in equals if not self.checkSkip(equal, self.skipList)]
                crawler.causals = equals
                causals.extend(equals)
        causals = extractor.causalUniqueSentence(causals)
        [print("after", "subj", causal.subj, "basis", causal.basis, "reslut", causal.result, causal.clue,
               causal.causalId, causal.pattern.toJson()) for causal in causals]
        return causals, crawlers

#     def extract(self, crawlers, relation):
#         causals = []
#         ex_causals = causals.extend
#         loop = asyncio.new_event_loop()
#         gcausals = loop.run_until_complete(self.coroutine(crawlers, relation))
#         loop.close()
#         gcausals = extractor.causalUniqueSentence(gcausals)
#         gcausals = [gcausal for gcausal in gcausals if not self.checkSkip(gcausal, self.skipList)]
#         crawler.causals = gcausals
#         ex_causals(gcausals)
#         causals = extractor.causalUniqueSentence(causals)
#         [print("after", "subj", causal.subj, "basis", causal.basis, "reslut", causal.result, causal.clue, causal.causalId, causal.pattern.toJson()) for causal in causals]
#         return causals, crawlers
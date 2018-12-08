import re
from .models import Causal, Goal, Step, PrunedUser, Smart, Relation, Pattern, Crawler, ResultExpression, ClueExpression
from cabocha.analyzer import CaboChaAnalyzer
from cabocha.analyzer import EndOfLinkException
from enum import Enum
from datetime import datetime
import pandas as pd


class cross_bootstrap:
    clueList = []

    eclueList = []

    gclueList = []

    geclueList = []

    eqclueList = []

    eqeclueList = []

    rclueList = []

    grclueList = []

    eqrclueList = []

    reclueList = []

    greclueList = []

    eqreclueList = []

    skipList = []

    def __init__(self):
        self.utilSet()

    def utilSet(self):

        self.skipList = pd.read_csv("Util/ja_skip_list.csv").dropna(subset=['clue'])['clue']

        self.clueList = pd.read_csv("Util/ja_clue_list.csv").dropna(subset=['clue'])
        self.eclueList = pd.read_csv("Util/ja_eclue_list.csv").dropna(subset=['clue'])
        self.gclueList = pd.read_csv("Util/ja_goal_clue_list.csv").dropna(subset=['clue'])
        self.geclueList = pd.read_csv("Util/ja_goal_eclue_list.csv").dropna(subset=['clue'])
        self.eqclueList = pd.read_csv("Util/ja_equal_clue_list.csv").dropna(subset=['clue'])
        self.eqeclueList = pd.read_csv("Util/ja_equal_eclue_list.csv").dropna(subset=['clue'])

        self.rclueList = []
        self.grclueList = []
        self.eqrclueList = []

    #         self.rclueList = pd.read_csv("Util/ja_result_list.csv").dropna(subset=['clue'])['clue']
    #         self.grclueList =pd.read_csv("Util/ja_skip_list.csv").dropna(subset=['clue'])['clue']
    #         self.eqrclueList = pd.read_csv("Util/ja_skip_list.csv").dropna(subset=['clue'])['clue']

    def checkResult(self, resultChunk):
        pos = resultChunk[resultChunk.token_size - 1].pos
        pos1 = resultChunk[resultChunk.token_size - 1].pos1
        if pos == "助詞":
            return False
        else:
            return True

    def getEndResult(self, texts):
        analyzer = CaboChaAnalyzer()
        results = []
        for text in texts:
            tree = analyzer.parse(text)
            lastChunk = tree[tree.chunk_size - 1]
            if self.checkResult(lastChunk):
                results.append(lastChunk)
        return results

    def getResultFromCausal(self, causal):
        results = []
        if causal.pattern == Pattern.A or Pattern.B:
            results = self.getEndResult(causal.sentence.split(causal.clue))
        elif causal.pattern == Pattern.C:
            results = self.getEndResult(causal.sentence.split(causal.clue))
        elif causal.pattern == Pattern.D:
            results = self.getEndResult(causal.sentence.split(causal.clue))
        elif causal.pattern == Pattern.E:
            results = self.getEndResult(causal.sentence.split("。"))
        return results

    def getClueFromSentence(self, sentence):
        analyzer = CaboChaAnalyzer()
        tree = analyzer.parse(sentence)
        for result in self.rclueList:
            if sentence.endswith(result):
                pass  # TODO: E pattern
            elif str(result) in sentence:
                matcher = sentence.split(result)[1]
                return analyzer.parse(matcher)[0]
            else:
                return None

    def getResultExpression(self, causals):
        results = []
        results.extend([self.getResultFromCausal(causal) for causal in causals])
        return results

    def getClueExpression(self, sentences):
        clues = []
        clues.extend([self.getClueFromSentence(sentence) for sentence in sentences])
        return clues
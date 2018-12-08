from enum import Enum
from datetime import datetime
import numpy as np
import json
import uuid
from collections import OrderedDict

class Crawler:
    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.keyword = ""
        self.url = ""
        self.article = ""
        self.causals = []
        self.createdAt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.updatedAt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")


class Relation(Enum):
    cause = 0
    goal = 1
    equal = 2
    specific = 3
    abstract = 4

    def toJson(self):
        if self == Relation.cause:
            return "cause"
        elif self == Relation.goal:
            return "goal"
        elif self == Relation.equal:
            return "equal"
        elif self == Relation.specific:
            return "specific"
        elif self == Relation.abstract:
            return "abstract"

    def toJaKeyword(self):
        if self == Relation.cause:
            return "なぜ"
        elif self == Relation.goal:
            return "どうやって"
        elif self == Relation.equal:
            return "とは"
        elif self == Relation.specific:
            return ""
        elif self == Relation.abstract:
            return ""


class Pattern(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4

    def toJson(self):
        if self == Pattern.A:
            return "A"
        elif self == Pattern.B:
            return "B"
        elif self == Pattern.C:
            return "C"
        elif self == Pattern.D:
            return "D"
        elif self == Pattern.E:
            return "E"

    def toOneHot(self):
        zeros = np.zeros(5)
        if self == Pattern.A:
            zeros[0] = 1
            return zeros
        elif self == Pattern.B:
            zeros[1] = 1
            return zeros
        elif self == Pattern.C:
            zeros[2] = 1
            return zeros
        elif self == Pattern.D:
            zeros[3] = 1
            return zeros
        elif self == Pattern.E:
            zeros[4] = 1
            return zeros


class Causal:
    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.basis = ""
        self.result = ""
        self.subj = ""
        self.pattern = ""
        self.clue = ""
        self.filePath = ""
        self.line = 0
        self.causalId = 0
        self.sentence = ""
        self.relation = Relation.cause
        self.createdAt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.updatedAt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # def __init__(self):

    # def __init__(self,basis,result,subj,pattern):
    #     self.basis = basis
    #     self.result = result
    #     self.subj = subj
    #     self.pattern = pattern

    def toJson(self):
        causal_dict = OrderedDict([
            ('uid', self.uid),
            ('basis', self.basis),
            ('result', self.result),
            ('subj', self.subj),
            ('clue', self.clue),
            ('filePath', self.filePath),
            ('line', self.line),
            ('sentence', self.sentence),
            ('relation', self.relation.toJson()),
            ('pattern', self.pattern.toJson()),
            ('createdAt', self.createdAt),
            ('updatedAt', self.updatedAt)
        ])
        return causal_dict

    def noneCheck(self):
        return all([self.basis != "", self.result != "", self.clue != "", self.sentence != "", self.basis != None,
                    self.result != None, self.clue != None, self.sentence != None])


class ResultExpression:
    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.result = ""
        self.pos = ""
        self.pos1 = ""
        self.causal = Causal()
        self.relation = Relation.cause
        self.createdAt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.updatedAt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")


class ClueExpression:
    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.clue = ""
        self.pos = ""
        self.pos1 = ""
        self.basis_pos = ""
        self.basis_pos1 = ""
        self.causal = Causal()
        self.relation = Relation.cause
        self.createdAt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.updatedAt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")


class Goal:
    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.text = ""
        self.credit = 0
        self.smart = Smart()
        self.steps = []
        self.owner = PrunedUser()
        self.private = False
        self.createdAt = ""
        self.updatedAt = ""


class Step:
    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.text = ""
        self.credit = 0
        self.smart = Smart()
        # self.tasks                   = []
        self.owner = PrunedUser()
        self.private = False
        self.createdAt = ""
        self.updatedAt = ""


class Smart:
    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.specificSubject = ""
        self.specificVerb = ""
        self.timeBound = ""
        self.measurable = ""
        self.credit = 0
        self.owner = PrunedUser()
        self.private = False
        self.createdAt = ""
        self.updatedAt = ""

    def getJaText(self):
        return self.specificSubject + self.timeBound + self.measurable + self.specificVerb


class PrunedUser:
    def __init__(self):
        self.uid = str(uuid.uuid4())
        self.credit = 0
        self.sumCredit = 0
        self.displayName = ""
        self.profileImage = ""
        self.backgroundImage = ""
        self.registrationConfirmed = ""
        self.permissions = False
        self.private = False
        self.createdAt = ""
        self.updatedAt = ""
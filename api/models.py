from django.db import models
from datetime import datetime
from enum import Enum
import numpy as np

class Relation(Enum):
    cause = 0
    goal = 1
    equal = 2
    specific = 3
    abstract = 4

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


#sqliteではなくFirebase連携でやります。
class Causal:
    def __init__(self):
        self.basis = ""
        self.result = ""
        self.subj = ""
        self.pattern = Pattern.A
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
        json = "{"
        json += "\"clue\": " + "\"" + self.clue + "\", "
        json += "\"basis\": " + "\"" + self.basis + "\", "
        json += "\"result\": " + "\"" + self.result + "\", "
        json += "\"subj\": " + "\"" + self.subj + "\", "
        json += "\"pattern\": " + "\"" +self.pattern + "\", "
        json += "\"filePath\": " + "\"" + self.filePath + "\", "
        json += "\"line\": " + self.line
        json += "}"
        return json

# class Causal(models.Model):
#     def __init__(self):
#         self.basis = ""
#         self.result = ""
#         self.subj = ""
#         self.pattern = ""
#         self.clue = ""
#         self.filePath = ""
#         self.line = 0
#         self.sentence = ""
#
#     # def __init__(self):
#
#     # def __init__(self,basis,result,subj,pattern):
#     #     self.basis = basis
#     #     self.result = result
#     #     self.subj = subj
#     #     self.pattern = pattern
#
#     def toJson(self):
#         json = "{"
#         json += "\"clue\": " + "\"" + self.clue + "\", "
#         json += "\"basis\": " + "\"" + self.basis + "\", "
#         json += "\"result\": " + "\"" + self.result + "\", "
#         json += "\"subj\": " + "\"" + self.subj + "\", "
#         json += "\"pattern\": " + "\"" +self.pattern + "\", "
#         json += "\"filePath\": " + "\"" + self.filePath + "\", "
#         json += "\"line\": " + self.line
#         json += "}"
#         return json
#
# class Morph(models.Model):
#     def __init__(self):
#         self.face = ""
#         self.base = ""
#         self.pos = ""
#         self.posd = ""
#
# class Pos(models.Model):
#     def __init__(self):
#         self.id = 0
#         self.chunk = 0
#         self.str = []
#         self.morph = []

class Goal:
    def __init__(self):
        self.uid                     = ""
        self.text                    = ""
        self.credit                  = 0
        self.smart                   = Smart()
        self.steps                   = []
        self.owner                   = PrunedUser()
        self.private                 = False
        self.createdAt               = ""
        self.updatedAt               = ""

class Step:
    def __init__(self):
        self.uid                     = ""
        self.text                    = ""
        self.credit                  = 0
        self.smart                   = Smart()
        # self.tasks                   = []
        self.owner                   = PrunedUser()
        self.private                 = False
        self.createdAt               = ""
        self.updatedAt               = ""

# class Task:
#     def __init__(self):
#         self.uid                     = ""
#         self.text                    = ""
#         self.credit                  = 0
#         self.smart                   = Smart()
#         self.owner                   = PrunedUser()
#         self.private                 = False
#         self.createdAt               = ""
#         self.updatedAt               = ""

class Smart:
    def __init__(self):
        self.uid                     = ""
        self.specificSubject         = ""
        self.specificVerb            = ""
        self.timeBound               = ""
        self.measurable              = ""
        self.credit                  = 0
        self.owner                   = PrunedUser()
        self.private                 = False
        self.createdAt               = ""
        self.updatedAt               = ""

    def getJaText(self):
        return self.specificSubject + self.timeBound + self.measurable + self.specificVerb

class PrunedUser:
    def __init__(self):
        self.uid                     = ""
        self.credit                  = 0
        self.sumCredit               = 0
        self.displayName             = ""
        self.profileImage            = ""
        self.backgroundImage         = ""
        self.registrationConfirmed   = ""
        self.permissions             = False
        self.private                 = False
        self.createdAt               = ""
        self.updatedAt               = ""

# class Causal(models.Model):
#     basis = models.TextField(
#         verbose_name='basis',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#     result = models.TextField(
#         verbose_name='result',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#     subj = models.TextField(
#         verbose_name='subj',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#     pattern = models.TextField(
#         verbose_name='pattern',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#     clue = models.TextField(
#         verbose_name='clue',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#     filePath = models.TextField(
#         verbose_name='filePath',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#     line = models.IntegerField(
#         verbose_name='line',
#         blank=True,
#         null=True,
#         default=0
#     )
#     sentence = models.TextField(
#         verbose_name='sentence',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#
#     # def __init__(self,basis,result,subj,pattern):
#     #     self.basis = basis
#     #     self.result = result
#     #     self.subj = subj
#     #     self.pattern = pattern
#
#     def toJson(self):
#         json = "{"
#         json += "\"clue\": " + "\"" + self.clue + "\", "
#         json += "\"basis\": " + "\"" + self.basis + "\", "
#         json += "\"result\": " + "\"" + self.result + "\", "
#         json += "\"subj\": " + "\"" + self.subj + "\", "
#         json += "\"pattern\": " + "\"" +self.pattern + "\", "
#         json += "\"filePath\": " + "\"" + self.filePath + "\", "
#         json += "\"line\": " + self.line
#         json += "}"
#         return json
#
# class Morph(models.Model):
#     face = models.TextField(
#         verbose_name='face',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#     base = models.TextField(
#         verbose_name='base',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#     pos = models.TextField(
#         verbose_name='pos',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#     posd = models.TextField(
#         verbose_name='posd',
#         blank=True,
#         null=True,
#         max_length=...
#     )
#
# class Pos(models.Model):
#     uid = models.AutoField(
#         primary_key=True,
#         default=0
#     )
#     id = models.IntegerField(
#         verbose_name='id',
#         blank=True,
#         null=True,
#         default=0
#     )
#     chunk = models.IntegerField(
#         verbose_name='chunk',
#         blank=True,
#         null=True,
#         default=0
#     )
#     str = []
#     #["", "", "", "", ""]
#     morph = []
#     #[Morph(),Morph(),Morph(),Morph(),Morph()]

from django.test import TestCase
import unittest
import re
from cabocha.analyzer import CaboChaAnalyzer
from .models import Causal, Morph, Pos
import CausalParser.CausalParser
import CausalExtraction.CausalExtraction

class TestCausalExtraction(unittest.TestCase):

    def makeIncludingCluse(self):
        value1 = ["を背景に", "を背景に、 "]
        expected = {'を背景に': ['を背景に、 '], 'を背景に、 ': []}
        causalExtraction = CausalExtraction()
        causalExtraction.clueList = value1
        actual = causalExtraction.makeIncludingCluse()
        self.assertEqual(expected, actual)

    def removePattern(self):
        value1 = ["主な要因は", "売上高の増加要因は", "増減要因は"]
        value2 = "主な要因はhogehogeである"
        expected = "hogehogeである"
        causalExtraction = CausalExtraction()
        causalExtraction.prefixPatternList = value1
        actual = causalExtraction.removePattern(value2)
        self.assertEqual(expected, actual)

    def havePattern(self):
        value1 = ["主な要因は", "売上高の増加要因は", "増減要因は"]
        value2 = "主な要因はhogehogeである"
        expected = True
        causalExtraction = CausalExtraction()
        causalExtraction.prefixPatternList = value1
        actual = causalExtraction.havePattern(value2)
        self.assertEqual(expected, actual)

    def removeKoto(self):
        value1 = re.compile('こと$|など$|等$|の$')
        value2 = "主な要因はhogehogeであること"
        expected = "主な要因はhogehogeである"
        causalExtraction = CausalExtraction()
        causalExtraction.pKoto = value1
        actual = causalExtraction.removeKoto(value2)
        self.assertEqual(expected, actual)


    #def includeDemon(self):

    #def getCoreIds(self):

    #def removeParticle(self):

    #def getResultVP(self):  not confirm

    #def getResultNP(self): not confirm

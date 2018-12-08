import re
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt
import MeCab
import random
from statistics import mean, median,variance,stdev
from cabocha.analyzer import CaboChaAnalyzer

def check_npjp(text):
    npjp = pd.read_csv('Util/pn_ja.dic.txt',sep=':', encoding='cp932',names=('Tango','Yomi','Hinshi', 'Score'))
    tango_retu = npjp['Tango']
    score_retu = npjp['Score']
    npjp_dic   = dict(zip(tango_retu, score_retu))
    analyzer = CaboChaAnalyzer()
    tree = analyzer.parse(text)
    score = []
    for chunk in tree:
        for token in chunk:
            try:
                score.append(npjp_dic[token.surface])
            except:
                pass
    return mean(score)

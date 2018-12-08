# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup


def clean_text(text):
    replaced_text = '\n'.join(s.strip() for s in text.splitlines()[2:] if s != '')  # skip header by [2:]
    replaced_text = replaced_text.lower()
    replaced_text = re.sub(r'[【】]', ' ', replaced_text)       # 【】の除去
    replaced_text = re.sub(r'[（）()]', ' ', replaced_text)     # （）の除去
    replaced_text = re.sub(r'[［］\[\]]', ' ', replaced_text)   # ［］の除去
    replaced_text = re.sub(r'[@＠]\w+', '', replaced_text)  # メンションの除去
    replaced_text = re.sub(r'https?:\/\/.*?[\r\n ]', '', replaced_text)  # URLの除去
    replaced_text = re.sub(r'　', ' ', replaced_text)  # 全角空白の除去
    return replaced_text


def clean_html_tags(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    cleaned_text = soup.get_text()
    cleaned_text = ''.join(cleaned_text.splitlines())
    return cleaned_text


def clean_html_and_js_tags(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    [x.extract() for x in soup.findAll(['script', 'style'])]
    cleaned_text = soup.get_text()
    cleaned_text = ''.join(cleaned_text.splitlines())
    return cleaned_text


def clean_url(html_text):
    """
    \S+ matches all non-whitespace characters (the end of the url)
    :param html_text:
    :return:
    """
    clean_text = re.sub(r'http\S+', '', html_text)
    return clean_text


def clean_code(html_text):
    """Qiitaのコードを取り除きます
    :param html_text:
    :return:
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    [x.extract() for x in soup.findAll(class_="code-frame")]
    cleaned_text = soup.get_text()
    cleaned_text = ''.join(cleaned_text.splitlines())
    return cleaned_text

def clean_symbol(text):
    text = re.sub(r'http\S+', '', text)
    # text=re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "" ,text)
    #     # text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub('RT', "", text)
    text=re.sub('お気に入り', "", text)
    text=re.sub('まとめ', "", text)
    # text=re.sub(r'[!-~]{10}', "", text)#半角記号,数字,英字
    text=re.sub(r'[!-/:-@[-`{-~]', "", text)
    text=re.sub(r'[︰-＠]', "", text)#全角記号
#     text=re.sub('\n', " ", text)#改行文字

    text = re.sub("▼|「|」|→|↓|←|↑|・|⇓|『|』|◎|○|■|●|×|☆|〇|△|★|◇|ゞ|'|〟|〝|©|※|◆|⚪|━|̄□|̄━|▽|♪|“|”︎︎|□|⇒︎︎|▲|《|》|▷", "", text)  # Todo: 特殊記号  全部網羅できていない

    f = open("Util/escape_sign.txt")
    data1 = f.read()
    f.close()
    data1 = re.sub(r'\"| |\\|\(|\(|\(|>>|\)', "", data1)
    datum = data1.split(',')
    for data in datum:
        try:
            text = re.sub(str(data), "", text)
        except:
            break

    text=re.sub("。","\n",text)
    text=re.sub("^[!-~]", "", text)
    return text


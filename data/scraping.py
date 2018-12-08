# set up
import getopt
import html2text
import urllib.request, urllib.error
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from readability.readability import Document
from googlesearch import search
from googlesearch import get_random_user_agent
#from summpy.lexrank import summarize
import http.client
from selenium import webdriver
import sys, io
import re
from urllib.parse import urlparse
from .ja.cleaning import clean_text
from .ja.cleaning import clean_symbol
from .ja.stopwords import skip_stopWord_sentence
from .ja.normalization import normalize_unicode

class googleScraping:
    encoding = 'utf-8'
    headers = {'User-Agent': str(get_random_user_agent())}
    googleUrl = "https://www.google.co.jp/search?q="
    baseGoogleUrl = "https://www.google.co.jp"
    baseKeyword = ""
    baseUrl = ""

    @staticmethod
    def google_search(query, limit=10, lang="jp"):
        return search(query, lang=lang, stop=limit, user_agent=get_random_user_agent())

    @staticmethod
    def getMainJAText(url):
        # try:
        #     html = urllib.request.urlopen(url).read()
        # except IncompleteRead as e:
        #     html = :e.partial
        try:
            html = urllib.request.urlopen(url).read()
            readable_article = Document(html).summary()
            readable_title = Document(html).short_title()
            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            text = str(h.handle(readable_article))
            return clean_text(clean_symbol(normalize_unicode(text))).split('\n')
        except:
            return ['']

    def __init__(self):
        self.baseKeyword = ""
        self.baseUrl = self.googleUrl

    def __init__(self, keyword):
        self.baseKeyword = urllib.parse.quote(keyword)
        self.baseUrl = self.googleUrl + urllib.parse.quote(keyword)

    def getResultUrl(self):
        print(self.baseUrl)
        baseRequest = urllib.request.Request(self.baseUrl, headers=self.headers)
        baseResponse = urllib.request.urlopen(baseRequest)
        baseResult = BeautifulSoup(baseResponse, "html.parser")
        baseCites = baseResult.find_all("cite")
        urls = []
        for cite in baseCites:
            if cite.string:
                urls.append(cite.string)
                print(cite.string)
        return urls

    def getNextUrls(self):
        baseRequest = urllib.request.Request(self.baseUrl, headers=self.headers)
        baseResponse = urllib.request.urlopen(baseRequest)
        baseResult = BeautifulSoup(baseResponse, "html.parser")
        baseAtags = baseResult.find_all("a", class_ = "fl")
        urls = []
        for a in baseAtags:
            a.renderContents()
            urls.append(self.baseGoogleUrl + a['href'])
            print(self.baseGoogleUrl + a['href'])
        return urls

    def eachResultUrls(self, urls):
        for url in urls:
            baseRequest = urllib.request.Request(url, headers=self.headers)
            baseResponse = urllib.request.urlopen(baseRequest)
            baseResult = BeautifulSoup(baseResponse, "html.parser")
            baseCites = baseResult.find_all("cite")
            resultUrls = []
            for cite in baseCites:
                if cite.string:
                    resultUrls.append(cite.string)
                    print(cite.string)
        return resultUrls

    def decomposeHTML(self, url):
        if (len(urlparse(url).scheme) > 0):
            baseRequest = urllib.request.Request(url, headers=self.headers)
            baseResponse = urllib.request.urlopen(baseRequest)
            soup = BeautifulSoup(baseResponse, 'html.parser')
            for s in soup(['script', 'style']):
                s.decompose()
            text = ' '.join(soup.stripped_strings)
            return text

#         only python3
#     def summarizeText(self, text):
#         sentences, debug_info = summarize(
#         text, sent_limit=3, debug=True
#     )
#         for sent in sentences:
#             print(sent.strip().encode(self.encoding))

    def setKeywordText(self, text, searchText):
        lines = text.split('。')
        lines_strip = [line.strip() for line in lines]
        return [line for line in lines_strip if line.find(searchText) >= 0]

    def getMainText(self, url):
        html = urllib.request.urlopen(url).read()
        readable_article = Document(html).summary()
        readable_title = Document(html).short_title()
        text = str(html2text.html2text(readable_article))
        return clean_text(clean_symbol(normalize_unicode(text))).split('\n')

    def getEachResultURL(self):
        urls = []
        urls.extend(self.getResultUrl())
        urls.extend(self.eachResultUrls(self.getNextUrls()))
        return urls

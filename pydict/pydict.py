__author__ = 'lenovo'
import re
import time
import urllib2
import pyperclip


class Pydict:
    def __init__(self, dictionary='my_dict.txt',visible=False,record=False):
        self.dictionary = dictionary
        self.visible = visible
        self.record = record

    def usage(self):
        print 'usage: must be english word'

    @staticmethod
    def crawl_html(queryword):
        assert isinstance(queryword, str)
        req = u'http://m.dict.cn/' + queryword
        html = urllib2.urlopen(url=req, timeout=10).read()
        assert isinstance(html, str)
        return html

    def add(self, words):
        myword = open(self.dictionary, 'a')
        #print type(words)
        if type(words) == list:
            for word in words:
                myword.write(word+'\n')
        if type(words) == str:
            myword.write(words+'\n')
        myword.close()

    @staticmethod
    def clean(src):
        words = re.findall('[A-Za-z]+', src)
        return words

    @staticmethod
    def print_page(html):
        pattern0 = re.compile('<li><span>.*</span><strong>.*</strong></li>')
        pattern1 = re.compile('<li><strong>.*</strong>')
        result0 = pattern0.findall(html)
        result1 = pattern1.findall(html)
        for each in result0:
            each = re.sub('</*\w*>', '', each)
            each = each.decode('utf-8')
            print each
        for each in result1:
            each = re.sub('</*\w*>', '', each)
            each = each.decode('utf-8')
            print each
            print '############################################################################################'

    def search(words):
        """
        search  words
        :rtype : str
        """
        if type(words) == list:
            for word in words:
                return Pydict.crawl_html(word)
        if type(words) == str:
            return Pydict.crawl_html(words)


    def show(words):
        if type(words) == list:
            for word in words:
                print(Pydict.search(word))
        if type(words) == str:
            print words
            print(Pydict.search(words))
            

    @staticmethod
    def input():
        prompt = u'Word:'
        prompt = prompt.encode('utf-8')
        while True:
            try:
                return raw_input(prompt)
            except EOFError, e:
                print str(e)

    def monitor(self):
        tmp = ''
        while True:
            try:
                src = pyperclip.paste()
                if isinstance(src, unicode) and src != tmp:
                    tmp = src
                    words = self.clean(src)
                    if self.visible:
                        self.show(words)
                    if self.record:
                        self.add(words)
            except ValueError:
                pass
            time.sleep(1)
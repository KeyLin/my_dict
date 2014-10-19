__author__ = 'lenovo'
import re
import time
import urllib2
import pyperclip


class Pydict:
    def __init__(self, dictionary='my_dict.txt'):
        self.dictionary = dictionary

    def usage(self):
        print 'usage: must be english word'

    @staticmethod
    def crawl_html(queryword):
        assert isinstance(queryword, str)
        req = u'http://m.dict.cn/' + queryword
        html = urllib2.urlopen(url=req, timeout=10).read()
        assert isinstance(html, str)
        return html

    def add(self, word):
        myword = open(self.mywords, 'a')
        myword.write(word+'\n')
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

    def search(self, src):
        """
        search  words
        :rtype : str
        """
        words = self.clean()
        for word in words:
            print word
            Pydict.add(word)
            return Pydict.crawl_html()

    @staticmethod
    def input():
        prompt = u'单词:'
        prompt = prompt.encode('utf-8')
        while True:
            try:
                return raw_input(prompt)
            except EOFError, e:
                print str(e)

    @staticmethod
    def monitor():
        tmp = ''
        while True:
            try:
                src = pyperclip.paste()
                if isinstance(src, unicode) and src != tmp:
                    tmp = src
                    return src
            except ValueError:
                pass
            time.sleep(1)
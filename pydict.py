__author__ = 'lenovo'
import re
import time
import urllib2
import pyperclip
from multiprocessing import Process,Queue


class Pydict:
    def __init__(self, dictionary='my_dict.txt',visible=False,record=False,queue=Queue()):
        self.dictionary = dictionary
        self.visible = visible
        self.record = record
        self.q = queue

    def usage(self):
        print 'usage: must be english word'

    def crawl_html(self, queryword):
        assert isinstance(queryword, str)
        req = u'http://m.dict.cn/' + queryword
        html = urllib2.urlopen(url=req, timeout=10).read()
        assert isinstance(html, str)
        return html

    def addToTXT(self, words):
        myword = open(self.dictionary, 'a')
        #print type(words)
        if type(words) == list:
            for word in words:
                myword.write(word+'\n')
        if type(words) == str:
            myword.write(words+'\n')
        myword.close()


    def clean(self,src):
        #print src
        words = re.findall('[A-Za-z]+', src)
        for word in words:
            self.q.put(word)


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
        print '################################################################################'


    def resolve(self):
        while True:
            word = self.q.get(True)
            if ~isinstance(word, str):
                word = str(word)
            #print type(word)
            print word
            if self.visible:
                self.print_page(self.crawl_html(word))
            if self.record:
                self.addToTXT(word)
            

    def input(self):
        prompt = u'Input:'
        prompt = prompt.encode('utf-8')
        while True:
            try:
                src = raw_input(prompt)
                print '\n'
                if isinstance(src, str):
                    self.clean(src)
            except EOFError, e:
                print str(e)
            time.sleep(1)


    def monitorClip(self):
        tmp = ''
        while True:
            try:
                src = pyperclip.paste()
                #print src
                if isinstance(src, unicode) and src != tmp:
                    tmp = src
                    self.clean(src)
            except ValueError:
                pass 
            time.sleep(3)
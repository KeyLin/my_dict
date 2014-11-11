__author__ = 'lenovo'
import re
import tkMessageBox
import Tkinter
import time
import urllib2
import pyperclip
from multiprocessing import Process,Queue


class Pydict:
    def __init__(self, dictionary='my_dict.txt',visible=False,gui=False):
        self.dictionary = dictionary
        self.visible = visible
        self.q = Queue()
        if gui:
            self.r = Tkinter.Tk()

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

    @staticmethod
    def clean_page(html):
        pattern0 = re.compile('<li><span>.*</span><strong>.*</strong></li>')
        pattern1 = re.compile('<li><strong>.*</strong>')
        result0 = pattern0.findall(html)
        result1 = pattern1.findall(html)
        result = ''
        for each in result0:
            each = re.sub('</*\w*>', '', each)
            result = result + each+'\n'
        for each in result1:
            each = re.sub('</*\w*>', '', each)
            result = result + each+'\n'
        result = result.decode('utf-8')
        return result


    def resolve(self):
        while True:
            word = self.q.get(True)
            if ~isinstance(word, str):
                word = str(word)
            #print type(word)
            print word
            if self.visible:
                result = self.clean_page(self.crawl_html(word))
                flag = tkMessageBox.askquestion(word, '%s' % result )
                print flag
                if flag == 'yes':
                    self.addToTXT(word)


    def gui_resolve(self):
        count = self.q.qsize()
        #print count
        for i in range(count):
            word = self.q.get(True)
            if ~isinstance(word, str):
                word = str(word)
            print word
            if self.visible:
                result = self.clean_page(self.crawl_html(word))
                flag = tkMessageBox.askquestion(word, '%s' % result )
                print flag
                if flag == 'yes':
                    self.addToTXT(word)
            

    def cmd_input(self):
        prompt = u'Input:'
        prompt = prompt.encode('utf-8')
        while True:
            try:
                #print '2B'
                src = raw_input(prompt)
                print '\n'
                #print type(src)+'sb'
                if isinstance(src, str):
                    self.clean(src)
            except EOFError, e:
                print str(e)
            time.sleep(1)


    def get_word(self):
        word = self.r.nameInput.get() or 'sb'
        #print word
        self.clean(word)
        self.gui_resolve()


    def gui_input(self):
        self.r.title('Dictionary')
        self.r.nameInput = Tkinter.Entry(self.r)
        self.r.nameInput.pack()
        self.r.alertButton = Tkinter.Button(self.r, text='Search', command=self.get_word)
        self.r.alertButton.pack()
        self.r.mainloop()


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
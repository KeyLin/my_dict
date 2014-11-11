#! /usr/bin/python
# -*-  coding=utf8  -*-
import tkMessageBox
import re
import Tkinter
import time
import urllib
import urllib2
import pyperclip
import sys
import multiprocessing
import os
import string
import gzip, cStringIO, zlib


def crawl_html(queryword):
    # req = urllib2.Request('http://m.dict.cn/good',
    # headers = {"Accept-Encoding":"gzip",})
    # print queryword
    req = u'http://m.dict.cn/' + queryword
    return urllib2.urlopen(url=req, timeout=10).read()


def usage():
    print "usage: must be english word"


def word_add(word):
    myword = open('my_word.txt', 'a')
    myword.write(word+'\n')
    myword.close()


def word_clean(src):
    words = re.findall('[A-Za-z]+', src)
    for each in words:
        word_search(each)


def print_page(html):
    #print '################################################################################'
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

def page_clean(html):
    pattern0 = re.compile('<li><span>.*</span><strong>.*</strong></li>')
    pattern1 = re.compile('<li><strong>.*</strong>')
    result0 = pattern0.findall(html)
    result1 = pattern1.findall(html)
    result = ''
    #print type(result0)
    for each in result0:
        each = re.sub('</*\w*>', '', each)
        #each = each.decode('utf-8')
        #print each
        #print type(each)
        result = result + each+'\n'
    for each in result1:
        each = re.sub('</*\w*>', '', each)
        #each = each.decode('utf-8')
        #print each
        result = result + each+'\n'
    result = result.decode('utf-8')
    #print result
    #print '################################################################################'
    return result

def word_search(word):
    word_add(word)
    if len(word) <= 0:
        usage()
    else:
        html = crawl_html(word)
        html = page_clean(html)
        print word
        #print_page(html)
        return html


def word_input():
    prompt = u'单词：'
    prompt = prompt.encode('GBK')
    while True:
        try:
            argv = raw_input(prompt)
            word_clean(argv)
        except EOFError, e:
            print str(e)


def monitor():
    tmp = ''
    while True:
        try:
            src = pyperclip.paste()
            if isinstance(src, unicode) and src != tmp:
                tmp = src
                word_clean(src)
        except ValueError:
            pass
        time.sleep(1)


def say_hello():
    word = root.nameInput.get() or 'world'
    print word
    html = word_search(word)
    tkMessageBox.showinfo(word, '%s' % html )



def gui():
    global root 
    root = Tkinter.Tk()
    #root.pack()
    root.nameInput = Tkinter.Entry(root)
    root.nameInput.pack()
    root.alertButton = Tkinter.Button(root, text='Hello', command=say_hello)
    root.alertButton.pack()
    #tkMessageBox.showinfo('Message', 'Hello, %s' % name)
    root.mainloop()


if __name__ == "__main__":
    #p1 = multiprocessing.Process(name='clipboard', target=monitor)
    #p2 = multiprocessing.Process(name='dict', target=word_input)
    #p1.start()
    #p2.start()
    gui()
    #monitor()
    word_input()

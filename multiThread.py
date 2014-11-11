import pydict
import time
import threading

if __name__ == '__main__':
    name = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    dic = pydict.Pydict(name+'.txt',True,True)
    p1 = threading.Thread(target=dic.monitorClip)
    #p2 = threading.Thread(target=dic.resolve)
    p1.start()
    #p2.start()
    dic.gui_input()
    p1.join()
    #p2.join()
    print 'Thread end.'
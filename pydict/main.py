import pydict
import time
from multiprocessing import Process,Queue

if __name__ == '__main__':
	name = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	dic = pydict.Pydict(name+'.txt',True,True)
	p1 = Process(target=dic.monitorClip)
	p2 = Process(target=dic.resolve)
	p1.start()
	p2.start()
	dic.input()
	p1.join()
	p2.join()
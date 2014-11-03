import pydict
import time

if __name__ == '__main__':
	save = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	dic = pydict.Pydict(save+'.txt',False,True)
	dic.monitor()
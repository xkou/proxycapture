#! coding: utf-8

# 得到 proxy 列表

import urllib
import socket,re, threading, time

def get1(url):
	# http://www.cnproxy.com/proxy8.html
	f = urllib.urlopen(url)
	buf = f.read()
	f.close()
	print buf
	ma = re.findall("<tr bgcolor=\"#ffffff\" class=\"text\" height=10>\n+<td>(.+)</td>\n+<td>(\d+)</td>", buf)
	return ma
	
	
def get2(url, pat):
	f = urllib.urlopen(url)
	buf = f.read()
	f.close()
	
	ma = re.findall(pat, buf)
	return ma

class TestProxy:

	def __init__(self):
		self.proxys=[]
		self.threadids=[]

	def test(self, server, port):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			sock.connect((server,port))
			self.proxys.append((server,port))
		except:
			pass
		sock.close()
		
	def newtest(self, server,port):
		T = threading.Thread(target = self.test, args = (server,port))
		T.start()
		self.threadids.append(T)
		
	def save(self, fn = "proxylist"):
		F = open(fn,"wb")
		for e in self.proxys:
			F.write("%s:%d\r\n" % (e[0],e[1]))
		F.close()
		print "保存到:",fn
		
		
	def wait(self):
		print "wait"
		n=len(self.threadids)
		for e in self.threadids:
			e.join()
			n-=1
			print "Threadnum:",n
			
	
			
		

if __name__ == "__main__":
	F = open("proxypage")
	l = F.readlines()
	F.close()
	
	tp = TestProxy()
	
	for e in l:
		if e.find("||||") == -1: continue
		page,regx = e.split("||||")
		
		page = page.strip()
		print page
		regx = regx.strip()
		plist = get2(page, regx)
		for p in plist:
			print p
			tp.newtest(p[0], int(p[1]))
			time.sleep(0.1)
			
			
	tp.wait()
	tp.save()
	
	

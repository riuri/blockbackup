#!/usr/bin/env python3

from datetime import datetime
import os
import re

class timestamp_model(object):
	'''Class for file backup naming conventions'''
	def __init__(self, blockstring, timestring):
		self.blockstring = blockstring
		self.timestring = timestring
	def __repr__(self):
		return 'Block %s at time %s'%(self.blockstring, self.timestring)
	def __str__(self):
		return __repr__(self)
	def filename(self):
		'''Intended to return the mapped file'''
		pass
	def listallcandidates(self, dir='.'):
		'''Intended to return block backup candidates'''
		pass
	def listblockcandidates(self, blockstring):
		'''Return all candidates for a given blockstring'''
		pass
	def listtimecandidates(self, timestring):
		'''Return all candidates for a given timestring'''

class tsdir_model(timestamp_model):
	def __init__(self, blockstring, timestring):
		timestamp_model.__init__(self, blockstring, timestring)
		self.timematch = re.compile(r'^[0-9]{8}$')
		self.blockmatch = re.compile(r'^[0-9a-f]{16}\.blk$')
	def filename(self):
		return '%s/%s'%(self.timestring, self.blockstring)
	def listallcandidates(self, dir='.'):
		for i in os.listdir(dir):
			if self.timematch.match(i) and os.path.isdir(os.path.join(dir, i)):
				timedir = os.path.join(dir, i)
				for j in os.listdir(timedir):
					f = os.path.join(timedir, j)
					if self.blockmatch.match(j) and os.path.isfile(f):
						yield f
	def filename(self):
		return '%s/%s.blk'
	def listblockcandidates(self, dir = '.'):
		thisblockmatch = re.compile(r'[0-9]{8}/%s\.blk$'%self.blockstring)
		return filter(thisblockmatch.match, self.listallcandidates(dir))


def timestring():
	return datetime.utcnow().strftime('%Y%m%d%H%M%S')

def aread(filename):
	with open(filename, 'rb') as i:
		count = 0
		b1 = i.read(512)
		while(b1):
			outfilename = "%016x.blk"%count
			with open(outfilename, 'wb') as of:
				of.write(b1)
			count += 1
			b1 = i.read(512)

def osdir():
	return [i for i in os.listdir() if i[-4:] == '.blk']

if __name__ == '__main__':
	print('Hello')
	a = tsdir_model('20160417', '0'*16)
	for i in a.listallcandidates('test'):
		print(i)

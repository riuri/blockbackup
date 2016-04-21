#!/usr/bin/env python3

from datetime import datetime
import os
import re

blocksize = 4096

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
	def __init__(self, blockstring, timestring, dire = '.'):
		timestamp_model.__init__(self, blockstring, timestring)
		self.dir = dire
		self.timematch = re.compile(r'^[0-9]{14}$')
		self.blockmatch = re.compile(r'^[0-9a-f]{16}\.blk$')
	def filename(self): # used
		return os.path.join(self.dir, self.timestring, "%s.blk"%self.blockstring)
	def listallcandidates(self):
		for i in os.listdir(self.dir):
			if self.timematch.match(i) and os.path.isdir(os.path.join(self.dir, i)):
				timedir = os.path.join(self.dir, i)
				for j in os.listdir(timedir):
					f = os.path.join(timedir, j)
					if self.blockmatch.match(j) and os.path.isfile(f):
						yield f
	def filename(self):
		return '%s/%s/%s.blk'%(self.dir, self.timestring, self.blockstring)
	def listblockcandidates(self):
		thisblockmatch = re.compile(r'%s/[0-9]{14}/%s\.blk$'%(self.dir, self.blockstring))
		return filter(thisblockmatch.match, self.listallcandidates())
	def getblockbackup(self,): # used
		return max(self.listblockcandidates())


def timestring():
	return datetime.utcnow().strftime('%Y%m%d%H%M%S')

def create_backup(filename, dir = '.'):
	'''Creates a backup from a filename on dir'''
	with open(filename, 'rb') as i:
		count = 0
		b1 = i.read(blocksize)
		ts = timestring()
		os.makedirs(os.path.join(dir, ts), exist_ok = True)
		while(b1):
			model = tsdir_model("%016x"%count, ts, dir)
			dirty = True
			# Try to find the other block
			try:
				beforefilename = model.getblockbackup()
				with open(beforefilename, 'rb') as bf:
					b2 = bf.read(blocksize)
					if b1 == b2:
						dirty = False
			except(ValueError): pass
			if dirty:
				outfilename = model.filename()
				with open(outfilename, 'wb') as of:
					of.write(b1)
			count += 1
			b1 = i.read(blocksize)

def retrieve_backup(filename, dir = '.'):
	'''Retrieves a backup from a dir onto a filename'''
	with open(filename, 'wb') as f:
		for blkid in range(2**(16*4)):
			model = tsdir_model("%016x"%blkid, '', dir)
			try:
				blockfile = model.getblockbackup()
			except(ValueError):
				break
			with open(blockfile, 'rb') as bf:
				b1 = bf.read(blocksize)
				f.write(b1)


def osdir():
	return [i for i in os.listdir() if i[-4:] == '.blk']

if __name__ == '__main__':
	print('Hello')
	create_backup('block', 'test')
	retrieve_backup('block2', 'test')

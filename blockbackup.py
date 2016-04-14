#!/usr/bin/env python3

from datetime import datetime
import os

def timestring():
	return datetime.utcnow().strftime('%Y%m%d%H%M%S')

def aread(filename):
	with open(filename, 'rb') as i:
		count = 0
		b1 = i.read(512)
		while(b1):
			outfilename = "%08x.blk"%count
			with open(outfilename, 'wb') as of:
				of.write(b1)
			count += 1
			b1 = i.read(512)

def osdir():
	return [i for i in os.listdir() if i[-4:] == '.blk']

if __name__ == '__main__':
	print('Hello')
	print(osdir())

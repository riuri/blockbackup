#!/usr/bin/env python3

def aread(filename):
	with open(filename, 'rb') as i:
		count = 0
		b1 = i.read(512)
		while(b1):
			print("%08x"%count)
			print(b1)
			count += 1
			b1 = i.read(512)

if __name__ == '__main__':
	print('Hello')
	aread('block')

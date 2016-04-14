#!/usr/bin/env python3

def aread():
	with open('block', 'rb') as i:
		b1 = i.read(512)
		print(b1)

if __name__ == '__main__':
	print('Hello')
	aread()
